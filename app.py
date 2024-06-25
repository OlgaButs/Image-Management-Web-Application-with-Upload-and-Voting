import cherrypy
import sqlite3 as sql
from api.api import API
import time
from jinja2 import Environment,FileSystemLoader

# Para fazer logout: cherrypy.lib.sessions.expire()
# Para verificar o Session ID do user: cherrypy.session.id
# Para verificar o tipo do request: cherrypy.request.method.upper()


class Root(object):

	@cherrypy.expose # Alimentação dos métodos de suporte aos restantes recursos.
	def api():
		return API()




	@cherrypy.expose # Página de Autenticação.
	def login(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		if (checkAuth(self)==True):
			return open("html/login.html",encoding="UTF-8")
		return open("html/login.html",encoding="UTF-8")




	@cherrypy.expose # Página de Registo.
	def registo(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		# Código necessário para gerar um e um só Session ID per user.
		if cherrypy.session.id not in cherrypy.session:
			cherrypy.session[str(cherrypy.session.id)] = str(time.strftime('%d-%m-%Y time:%H:%M:%S'))
		return open("html/registo.html",encoding="UTF-8")




	@cherrypy.expose # Página do Sobre.
	def sobre(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		# Código necessário para gerar um e um só Session ID per user.
		if cherrypy.session.id not in cherrypy.session:
			cherrypy.session[str(cherrypy.session.id)] = str(time.strftime('%d-%m-%Y time:%H:%M:%S'))
		return open("html/sobre.html",encoding="UTF-8")




	@cherrypy.expose # Página do UA.
	def ua(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		# Código necessário para gerar um e um só Session ID per user.
		if cherrypy.session.id not in cherrypy.session:
			cherrypy.session[str(cherrypy.session.id)] = str(time.strftime('%d-%m-%Y time:%H:%M:%S'))
		return open("html/ua.html",encoding="UTF-8")




	@cherrypy.expose # Página do Upload.
	def upload(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		if (checkAuth(self)==True):
			return open("html/upload.html",encoding="UTF-8")
		return open("html/login.html",encoding="UTF-8")




	@cherrypy.expose # Página do Index.
	def index(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		if (checkAuth(self)==True):
			return open("html/index.html",encoding="UTF-8")
		return open("html/login.html",encoding="UTF-8")




	@cherrypy.expose # Página do Image.
	@cherrypy.tools.allow(methods=["GET","POST"])
	def image(self, imgid):
		cherrypy.response.headers["Content-Type"] = "text/html"
		if (checkAuth(self)==True):
			return Environment(loader=FileSystemLoader("html/")).get_template("image.html").render(id=imgid)
			#return open("html/image.html",encoding="UTF-8")
		return open("html/login.html",encoding="UTF-8")




	@cherrypy.expose # Página do Gallery.
	def gallery(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		if (checkAuth(self)==True):
			return open("html/gallery.html",encoding="UTF-8")
		return open("html/login.html",encoding="UTF-8")




	@cherrypy.expose # Página do Process
	def process(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		if (checkAuth(self)==True):
			return open("html/process.html",encoding="UTF-8")
		return open("html/login.html",encoding="UTF-8")
	



# Verifica se o user está logged-in (autenticado).
def checkAuth(self):
	# Código necessário para gerar um e um só Session ID per user.
	if cherrypy.session.id not in cherrypy.session:
		cherrypy.session[str(cherrypy.session.id)] = str(time.strftime('%d-%m-%Y time:%H:%M:%S'))
	db = sql.connect("database.db")
	content = db.execute("SELECT * FROM users;")
	for eachRow in content.fetchall():
			if (cherrypy.session.id in eachRow):
				db.close()
				cherrypy.response.cookie["login_status"] = "true"
				cherrypy.response.cookie["login_status"]["max-age"] = cherrypy.session.timeout
				return True #cherrypy.request.cookie.keys() --> cookies é dict
	db.close()
	cherrypy.response.cookie["login_status"] = "false"
	return False