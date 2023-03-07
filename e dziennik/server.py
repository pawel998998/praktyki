import cherrypy
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dziennik"
)

mycursor = mydb.cursor()

with open("login_page.html", encoding="utf-8") as template:
    login_page = template.read()

with open("register_page.html", encoding="utf-8") as template:
   register_page = template.read()

with open("sprawdziany.html", encoding="utf-8") as template:
   sprawdziany = template.read()

with open("plan_zajec.html", encoding="utf-8") as template:
   plan_zajec = template.read()

with open("zadania.html", encoding="utf-8") as template:
   zadania = template.read()

with open("oceny.html", encoding="utf-8") as template:
   oceny = template.read()



class main(object):
   @cherrypy.expose
   def index_login_page(self):
      return login_page

   @cherrypy.expose
   def index_register_page(self):
      return register_page

   @cherrypy.expose
   def index_login(self):
      return login_page

   @cherrypy.expose
   def sprawdziany(self):
      return sprawdziany

   @cherrypy.expose
   def plan_zajec(self):
      return plan_zajec

   @cherrypy.expose
   def zadania(self):
      return zadania

   @cherrypy.expose
   def oceny(self):
      return oceny


   @cherrypy.expose
   def login(self, email, password):
      mycursor.execute("select email, password from logowanie")
      data = mycursor.fetchall()
      for i in range(len(data)):
         if email in data[i] and password in data[i]:
            return oceny
         else:
            return login_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Zły mail lub hasło</p></div></center>")

   @cherrypy.expose
   def register(self, firstname, lastname, email, password, confirmpassword):
      mycursor.execute(f"Select firstname, lastname, email, password from logowanie WHERE email = '{email}'")
      login_and_password_list = mycursor.fetchall()
      if len(login_and_password_list) > 0:
         return register_page
      mycursor.execute(f"Select firstname, lastname, email, password from logowanie")
      login_and_password_list = mycursor.fetchall()
      for i in range(len(login_and_password_list)):
         if len(firstname) < 3 or len(lastname) < 3 or len(password) < 6 or password != confirmpassword:
            return register_page
         else:
            query = "INSERT INTO logowanie (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)"
            values = (firstname, lastname, email, password)
            mycursor.execute(query, values)
            mydb.commit()
            return login_page


cherrypy.config.update({'server.socket_port': 25565,'engine.autoreload_on': False})
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(main())