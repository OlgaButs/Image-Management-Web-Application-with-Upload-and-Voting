import os.path
import cherrypy
from app import Root
from api.api import API
#import platform
#from pasta.ficheiro import classe

# The absolute path to this file's base directory
baseDir = os.path.abspath(os.path.dirname(__file__))

##cherrypy.config.update({"server.socket_port": 10004})
"""
cherrypy.config.update({
    'server.socket_host' : '192.168.1.102',
    'server.socket_port' : 1234,})
"""

# Dictionary with this application's static directories configuration
config = {	"/": 		{	"tools.staticdir.root": baseDir,
							"tools.sessions.on" : True,
							"tools.sessions.storage_class" : cherrypy.lib.sessions.FileSession,
							"tools.sessions.storage_path" : os.path.join(baseDir, "Sessions"),
							"tools.sessions.name" : "session_id",
							"tools.sessions.timeout" : 15},
			"/uploads":	{	"tools.staticdir.on": True, "tools.staticdir.dir": "uploads" },
			"/js":		{	"tools.staticdir.on": True, "tools.staticdir.dir": "js"     },
			"/css":		{	"tools.staticdir.on": True, "tools.staticdir.dir": "css"    },
            "/images":	{	"tools.staticdir.on": True, "tools.staticdir.dir": "images" },
            "/tmp":		{	"tools.staticdir.on": True, "tools.staticdir.dir": "tmp"}
         }#"/html":	{	"tools.staticdir.on": True, "tools.staticdir.dir": "html" },

#cherrypy.tree.mount(API(), "/api")
root = Root()
root.api = API()

cherrypy.quickstart(root, "/", config)