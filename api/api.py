import os
import cherrypy
import json
import hashlib
import sqlite3 as sql
import time
from api.image_processing  import image_processing

# The absolute path to this file's base directory
baseDir = os.path.abspath(os.path.dirname(__file__))


class API:

    # Register user
	@cherrypy.expose
	def register(self, username, password, flag="false"):
		db = sql.connect('database.db')

		result = db.execute("SELECT id FROM users WHERE username=?", (username,))
		if result.fetchone() is not None and flag=="false":
			return "Username already exists."

		# Hash the password
		hashed_password = hashlib.sha256(password.encode()).hexdigest()

		# Insert the user into the database
		db.execute("INSERT INTO users (username, password, sessionID) VALUES (?, ?, ?)", (username, hashed_password, cherrypy.session.id))
		db.commit()
			#cherrypy.response.cookie["login_status"] = "true"
			#cherrypy.response.cookie["login_status"]["max-age"] = cherrypy.session.timeout
		db.close()
		if (flag=="false"):
			return "Registration successful."
		return "Password Changed!"
	



    # Login user
	@cherrypy.expose
	def login(self, username, password):
		db = sql.connect('database.db')
		hashed_password = hashlib.sha256(password.encode()).hexdigest()

		result = db.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
		db.commit()

		if result.fetchone() is not None:
			db.execute("UPDATE users SET sessionID=? WHERE username=? AND password=?", (cherrypy.session.id,username,hashed_password))
			db.commit()
			db.close()
			return "Login successful."
		else:
			db.close()
			return "Invalid username or password."




	# Logout user
	@cherrypy.expose
	def logout(self):
		cherrypy.lib.sessions.expire()
		cherrypy.response.cookie["login_status"] = "false"
		db = sql.connect("database.db")
		userID = db.execute("SELECT id FROM users WHERE sessionID=?",(cherrypy.session.id,))
		for each in userID.fetchall():
			for n in each:
				db.execute("UPDATE users SET sessionID=? WHERE id=?",('null',n,))
				db.commit()
		db.close()
		return

	@cherrypy.expose
	def topimage(self):
		try:
			db = sql.connect('database.db')
			cursor = db.cursor()

			cursor.execute("SELECT path FROM images ORDER BY ups DESC LIMIT 3")
			rows = cursor.fetchall()
			db.close()

			count = 1
			images = {}
			for row in rows:
				images[f"image{count}"] = row[0]
				count += 1
			print(images)
			cherrypy.response.headers["Content-Type"] = "application/json"
			return json.dumps({"top_images": images}).encode("utf-8")
		except Exception as e:
					return "Error: " + str(e)

    # UpLoad image
	@cherrypy.expose
	def upload(self, myFile, nameImg, authorImg ):
		try:
			h = hashlib.sha256()
			filename = os.path.join(baseDir,"..", "uploads", myFile.filename)
			fileout = open(filename, "wb")
			while True:
				data = myFile.file.read(8192)
				if not data or data==None:
					break
				fileout.write(data)
				h.update(data)
			fileout.close()

			ext = myFile.filename.split(".")[-1]
			path = "uploads/" + h.hexdigest() + "." + ext
			os.rename(filename, path)

			datetime = time.strftime('%d-%m-%Y %H:%M:%S')

			db = sql.connect('database.db')
			db.execute("INSERT INTO images (name, path, datetime, author, ups, dwn) VALUES (?, ?, ?, ?, 0, 0)",
						(nameImg, path, datetime, authorImg))
			db.commit()
		except Exception as e:
			cherrypy.log.error(f"An error occurred during upload: {str(e)}")
			cherrypy.response.status = 500
			return "Internal Server Error"


    # List requested images
	@cherrypy.expose
	def list(self, id):
		db = sql.connect('database.db')
		if (id == "all"):
			result = db.execute("SELECT * FROM images")
			# Query correta para selecionar todas as imagens
		else:
			result = db.execute("SELECT * FROM images WHERE author = ?", (id,))
			# Query correta para selecionar todas as imagens do autor id
		rows = result.fetchall()
		db.close()

		result = []
		for row in rows:
			image = {
				"id": row[0],
				"name": row[1],
				"path": row[2],
				"datetime": row[3],
				"author": row[4],	
			}
			result.append(image)
		#print(len(result))
		result.sort(key=lambda x: x['name'])
		cherrypy.response.headers["Content-Type"] = "application/json"
		return json.dumps({"images": result}).encode("utf-8")
	



	# Gets User Like Status
	@cherrypy.expose
	def getUserLike(self, idimg):
		try:
			sessionID = cherrypy.request.cookie.get("session_id").value
			db = sql.connect("database.db")
			
			userID = db.execute("SELECT id FROM users WHERE sessionID=?",(sessionID,))
			userID = userID.fetchone()
			userID = userID[0]

			result = db.execute("SELECT vote FROM votes WHERE idimg=? AND idusr=?", (idimg,userID,))
			result = result.fetchone()
			if result:
				result = result[0]
			else:
				result = None

			return result
		except Exception as e:
					return "Error: " + str(e)



 	# List comments
	@cherrypy.expose
	def comments(self, idimg):
		db = sql.connect('database.db')
		# Query to retrieve image information
		result = db.execute("SELECT * FROM images WHERE id=?", (idimg,))
		image_row = result.fetchone()

		# Generate output dictionary with image information
		if image_row is not None:
			imageinfo = {
			"id": image_row[0],
			"name": image_row[1],
			"path": image_row[2],
			"datetime": image_row[3],
			"author": image_row[4]
			
		}
		else:
			imageinfo ={}
		
		# Query to retrieve comments of the image
		result = db.execute("SELECT * FROM comments WHERE idimg = ?", (idimg,))
		rows = result.fetchall()

		# Generate output dictionary with image comments list
		comments = []
		for row in rows:
			comment = {
				"id":      row[0],
				"user":    row[2],
				"comment": row[3],
				"datetime":row[4]
			}
			comments.append(comment)

		# Query to retrieve votes of the image
		result = db.execute("SELECT ups, dwn FROM images WHERE id = ?", (idimg,))
		votes = result.fetchone()
		db.close()
		# Generate output dictionary with image votes
		
		if votes is not None:
			imagevotes = {
				"thumbs_up": 0 + votes[0],
				"thumbs_down": 0 + votes[1]
			}
		else:
			imagevotes = {
				"thumbs_up": 0,
				"thumbs_down": 0
			}

		cherrypy.response.headers["Content-Type"] = "application/json"
		return json.dumps({"image": imageinfo, "comments": comments, "votes": imagevotes}).encode("utf-8")
	



    # UpLoad comment
	@cherrypy.expose
	def newcomment(self, idimg, newcomment):
			try:
				db = sql.connect('database.db')
				username = self.get_username()
				# Insert new comment into the database
				db.execute("INSERT INTO comments (user, comment, datetime, idimg) VALUES (?, ?, ?, ?)",
						(username, newcomment, time.strftime('%d-%m-%Y %H:%M:%S'), idimg,))
				db.commit()
				db.close()
			except Exception as e:
				return "Error: " + str(e)




	# Increment Up votes
	@cherrypy.expose
	def upvote(self, idimg):
		try:
			sessionID = cherrypy.request.cookie.get("session_id").value

			db = sql.connect('database.db')

			userID = db.execute("SELECT id FROM users WHERE sessionID=?",(sessionID,))
			userID = userID.fetchone()[0]

			value = db.execute("SELECT id FROM votes WHERE idimg=? AND idusr=?", (idimg,userID,))
			value = value.fetchone()
			if (value==None):
				db.execute("INSERT INTO votes (idimg,idusr,vote) VALUES (?,?,?)",(idimg,userID,"None"))
				db.commit()

			value = db.execute("SELECT vote FROM votes WHERE idimg=? AND idusr=?", (idimg,userID,))
			value = value.fetchone()[0]

			if (value=="true"):
				return
			elif (value=="false"):
				db.execute("UPDATE images SET dwn = dwn - 1 WHERE id=?",(idimg,))
				db.commit()
			# Update thumbs_up count in votes table 
			db.execute("UPDATE votes SET vote = ? WHERE idimg=? AND idusr=?", ("true",idimg,userID,))
			db.commit()
			db.execute("UPDATE images SET ups = ups + 1 WHERE id=?", (idimg,))
			db.commit()
			db.close()
		except Exception as e:
				return "Error: " + str(e)




	# Increment Down votes
	@cherrypy.expose
	def downvote(self, idimg):
		try:
			sessionID = cherrypy.request.cookie.get("session_id").value
			db = sql.connect('database.db')

			userID = db.execute("SELECT id FROM users WHERE sessionID=?",(sessionID,))
			userID = userID.fetchone()[0]

			value = db.execute("SELECT id FROM votes WHERE idimg=? AND idusr=?", (idimg,userID,))
			value = value.fetchone()
			if (value==None):
				db.execute("INSERT INTO votes (idimg,idusr,vote) VALUES (?,?,?)",(idimg,userID,"None"))
				db.commit()

			value = db.execute("SELECT vote FROM votes WHERE idimg=? AND idusr=?", (idimg,userID,))
			value = value.fetchone()[0]

			if (value==None):
				db.execute("INSERT INTO votes (idimg,idusr,vote) VALUES (?,?,?)",(idimg,userID,"None"))
				db.commit()

			if (value=="false"):
				return
			elif (value=="true"):
				db.execute("UPDATE images SET ups = ups - 1 WHERE id=?",(idimg,))
				db.commit()

			# Update thumbs_down count in votes table
			db.execute("UPDATE votes SET vote = ? WHERE idimg=? AND idusr=?", ("false",idimg,userID,))
			db.commit()
			db.execute("UPDATE images SET dwn = dwn + 1 WHERE id=?", (idimg,))
			db.commit()
			db.close()
		except Exception as e:
				return "Error: " + str(e)




	def get_username(self):
		# Retrieve the user's session or unique identifier from the appropriate source
		# Query the database to retrieve the username based on the identifier
		db = sql.connect("database.db")
		cursor = db.cursor() 

		cursor.execute("SELECT username FROM users WHERE sessionID = ?", (cherrypy.session.id,))
		result = cursor.fetchone()
		db.close()

		if result:
			return result[0]
		else:
			return "Unknown User"




	@cherrypy.expose
	def imageproc(self, id, select):
		db = sql.connect('database.db')
		cursor = db.cursor()
		cursor.execute("SELECT * FROM images WHERE id = ?", (id,))
		row = cursor.fetchone()
		db.close()

		if row is None:
			return "Image not found."

		image_path = row[2]

		db = sql.connect("database.db")
		cursor = db.cursor()
		cursor.execute("SELECT id FROM users WHERE sessionID = ?", (cherrypy.session.id,))
		result = cursor.fetchone()
		db.close()

		if result:
			fileNameProc = "processed_image" + str(result[0]) + ".jpg"
		else:
			fileNameProc = "processed_image" + "Unknown" + ".jpg"

		processed_image_path = os.path.join(baseDir, "..", "tmp", fileNameProc)

		response = {"processedImagePath": "../tmp/" + fileNameProc}

		self.delete_processed_images()
		image_processing(image_path, processed_image_path, select)

		return json.dumps(response).encode("utf-8")




	@cherrypy.expose
	def deleteProcessedImages(self):
		self.delete_processed_images()

	def selectBestImage(self):
		db = sql.connect('database.db')
		ups,path = db.execute("SELECT ups, path FROM images").fetchall()
		maiores = {}

		for value in ups,path:
			maiores[ups]=path

			if len(maiores) < 3:
				maiores.append((ups, path))
			else:
				maiores.sort(reverse=True)
				if ups > maiores[0][0]:
					maiores[0] = (ups, path)
		for i in maiores:
			return db.execute("SELECT id FROM images")






	def delete_processed_images(self):
		# Logic to delete unnecessary processed images
		db = sql.connect("database.db")
		cursor = db.cursor()
		cursor.execute("SELECT id FROM users WHERE sessionID = ?", (cherrypy.session.id,))
		idUser = cursor.fetchone()[0]
		if not idUser:idUser = "Unknown"
		db.close()
		folder_path = os.path.join(baseDir, '..', 'tmp')
		for file_name in os.listdir(folder_path):
			if file_name.startswith("processed_image") and str(idUser) in file_name:
				file_path = os.path.join(folder_path, file_name)
				os.remove(file_path)




	@cherrypy.expose
	def removeImage(self, idimg):
		db = sql.connect("database.db")
		try:
			path = db.execute("SELECT path FROM images WHERE id=?",(idimg,))
			path = path.fetchone()[0]
			path = os.path.join(baseDir, os.pardir ,path)
			os.remove(path)

			db.execute("DELETE FROM images WHERE id=?",(idimg,))
			db.commit()
			db.execute("DELETE FROM votes WHERE idimg=?",(idimg,))
			db.commit()
			return "Image successfuly removed from the server! Returning you to the Gallery."
		except:
			return "Oops... Something unexpected happened! Try again latter or contact the admin."