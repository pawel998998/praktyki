import cherrypy
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dziennik"
)

mycursor = mydb.cursor()

with open("login_register/login_page.html", encoding="utf-8") as template:
    login_page = template.read()

with open("login_register/register_page.html", encoding="utf-8") as template:
   register_page = template.read()

with open("e_dziennik/plan_lekcji.html", encoding="utf-8") as template:
   plan_lekcji = template.read()

with open("admin/plan_lekcji_admin.html", encoding="utf-8") as template:
   plan_lekcji_admin = template.read()



class main(object):
   @cherrypy.expose
   def index(self):
      return login_page

   @cherrypy.expose
   def index_login_page(self):
      return login_page

   @cherrypy.expose
   def index_register_page(self):
      return register_page

   @cherrypy.expose
   def plan_lekcji(self):

      plan_lekcji_srodek = ""

      mycursor.execute("select * from plan_lekcji")
      plan_lekcji_db = mycursor.fetchall()

      plan_lekcji_template_poczatek = "<table><thead><tr><th>Godzina</th><th>Poniedziałek</th><th>Wtorek</th><th>Środa</th><th>Czwartek</th><th>Piątek</th></tr></thead>"
      for i in range(len(plan_lekcji_db)):
         plan_lekcji_template_srodek = f"<tbody><tr><tr><td>{plan_lekcji_db[i][1]} - {plan_lekcji_db[i][2]}</td><td>{plan_lekcji_db[i][3]}</td><td>{plan_lekcji_db[i][4]}</td><td>{plan_lekcji_db[i][5]}</td><td>{plan_lekcji_db[i][6]}</td><td>{plan_lekcji_db[i][7]}</td></tr></tbody>"
         plan_lekcji_srodek += plan_lekcji_template_srodek
      plan_lekcji_template_koniec = "</table>"

      plan_lekcji_template = f"{plan_lekcji_template_poczatek}{plan_lekcji_srodek}{plan_lekcji_template_koniec}"
      return plan_lekcji.replace("{table}", plan_lekcji_template)

   @cherrypy.expose
   def plan_lekcji_admin(self):
      return plan_lekcji_admin

   @cherrypy.expose
   def login(self, email, password):
      dobre_haslo = 0
      dobry_email = 0
      mycursor.execute(f"select email from logowanie where email = '{email}'")
      email_db = mycursor.fetchall()
      mycursor.execute(f"select password from logowanie where password = '{password}'")
      password_db = mycursor.fetchall()

      for i in range(len(email_db)):
         if email_db[i][0] == email:
            dobry_email = 1
      for i in range(len(password_db)):
         if password_db[i][0] == password:
            dobre_haslo = 1

      if dobry_email == 1 and dobre_haslo == 1:
         raise cherrypy.HTTPRedirect("/plan_lekcji")
      if dobry_email == 0:
         return login_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Zły email.</p></div></center>")
      if dobre_haslo == 0:
         return login_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Złe hasło.</p></div></center>")

   @cherrypy.expose
   def register(self, firstname, lastname, email, password, confirmpassword):
      dobre_imie = 0
      dobre_nazwisko = 0
      dobry_email = 0
      dobre_haslo = 0
      dobre_drugie_haslo = 0
      regex_mail = 0

      mycursor.execute(f"select email from logowanie where email = '{email}'")
      email_db = mycursor.fetchall()
      mycursor.execute(f"select password from logowanie where password = '{password}'")
      password_db = mycursor.fetchall()

      try:
         if email == email_db[0][0]:
            dobry_email = 0
         else:
            dobry_email = 1
      except:
         dobry_email = 1

      if len(firstname) >= 3:
         dobre_imie = 1

      if len(lastname) >= 3:
         dobre_nazwisko = 1

      if len(password) >= 6:
         dobre_haslo = 1

      if check(email) == True:
         regex_mail = 1

      if password == confirmpassword:
         dobre_drugie_haslo = 1

      if regex_mail == 1 and dobre_imie == 1 and dobre_nazwisko == 1 and dobry_email == 1 and dobre_haslo == 1 and dobre_drugie_haslo == 1:
         query = "INSERT INTO logowanie (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)"
         values = (firstname, lastname, email, password)
         mycursor.execute(query, values)
         mydb.commit()


         # Dane logowania do skrzynki pocztowej
         login = "kochamtruskawki998@gmail.com"
         password_sftp = "oflgetnuwfyobuei"


         # Tworzenie wiadomości email
         msg = MIMEMultipart()
         msg["From"] = login
         msg["To"] = email
         msg["Subject"] = "Rejestracja"
         body = f"""
         <h1>Rejestracja</h1>
         <p>Pomyślnie zarejestrowales się. Dane:</p></br>
         <p>Imię: {firstname}</p></br>
         <p>Nazwisko: {lastname}</p></br>
         <p>Email: {email}</p></br>
         <p>Hasło: {password}</p></br>
         """

         msg.attach(MIMEText(body, "html"))
         try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(login, password_sftp)
            # Wysyłanie wiadomości
            server.sendmail(login, email, msg.as_string())
            server.quit()
         except:
            pass

        


         return login_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Pomyślnie zarejestrowano. Mozesz się zalogować</p></div></center>")

      if regex_mail == 0:
         return register_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Niepoprawny email.</p></div></center>")
      if dobre_imie == 0:
         return register_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Imię jest za krótkie. Musi mieć minimum 3 znaki.</p></div></center>")
      if dobre_nazwisko == 0:
         return register_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Nazwisko jest za krótkie. Musi mieć minimum 3 znaki.</p></div></center>")
      if dobre_haslo == 0:
         return register_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Hasło jest za krótke. Musi mieć minimum 6 znaków dlugości.</p></div></center>")
      if dobre_drugie_haslo == 0:
         return register_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Hasła się różnią.</p></div></center>")
      if dobry_email == 0:
         return login_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Znaleziono email w bazie danych. Zaloguj się.</p></div></center>")

main = main()
cherrypy.tree.mount(main, '/')

cherrypy.config.update({'server.socket_port': 25565,'engine.autoreload_on': True})
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(main)