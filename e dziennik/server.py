import cherrypy
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import os

secret_key = '1234'
admin = False
class Session:
    def __init__(self):
        self.data = {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

    def delete(self, key):
        del self.data[key]

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
  database="dziennik")

mycursor = mydb.cursor()

with open("login_register/login.html", encoding="utf-8") as template:
    login_page = template.read()

with open("login_register/register.html", encoding="utf-8") as template:
   register_page = template.read()

with open("e_dziennik/template.html", encoding="utf-8") as template:
   template = template.read()

class main(object):
   @cherrypy.expose
   def index(self):
      raise cherrypy.HTTPRedirect("/plan_lekcji")

   @cherrypy.expose
   def clear_cookies(self):
      for cookie_name in cherrypy.request.cookie:
         #return str(cherrypy.response.cookie)
         cherrypy.response.cookie[cookie_name]['expires'] = 0
      raise cherrypy.HTTPRedirect("/index_login_page")


   @cherrypy.expose
   def index_login_page(self):
      cherrypy.session['logged_in'] = False
      return login_page

   @cherrypy.expose
   def index_register_page(self):
      return register_page

   @cherrypy.expose
   def zadania(self):
      global admin
      zadania_srodek = ""
      mycursor.execute("select * from zadania")
      zadania_db = mycursor.fetchall()
      zadania_template_poczatek = "<table><thead><tr><th>data</th><th>zadanie</th><th>przedmiot</th><th>opis</th></tr></thead>"
      for i in range(len(zadania_db)):
         zadania_template_srodek = f"<tbody><tr><td>{zadania_db[i][4]}</td><td>{zadania_db[i][1]}</td><td>{zadania_db[i][3]}</td><td>{zadania_db[i][2]}</td></tr></tbody>"
         zadania_srodek += zadania_template_srodek
      zadania_template_koniec = "</table>"
      zadania_template = f"{zadania_template_poczatek}{zadania_srodek}{zadania_template_koniec}"
      if cherrypy.session.get('logged_in'):
         mycursor.execute("select email from admin")
         admin_db = mycursor.fetchall()

         for i in range(len(admin_db)):
            if cherrypy.session["user"] == admin_db[0][i]:
               admin = True
            else:
               admin = False
         if admin == True:
            raise cherrypy.HTTPRedirect('/zadania_admin')         
         else:
            return template.replace("{table}", zadania_template).replace("{subject}", "Zadania")

      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def zadania_admin(self):
      global admin
      zadania_srodek = ""
      mycursor.execute("select * from zadania")
      zadania_db = mycursor.fetchall()
      zadania_template_poczatek = "<table><thead><tr><th>data</th><th>zadanie</th><th>przedmiot</th><th>opis</th><th>Edytowanie</th></tr></thead>"
      for i in range(len(zadania_db)):
         zadania_template_srodek = f"<tbody><tr><td>{zadania_db[i][4]}</td><td>{zadania_db[i][1]}</td><td>{zadania_db[i][3]}</td><td>{zadania_db[i][2]}</td><td><a class='abcd'  href='zadania_admin_edycja?id={zadania_db[i][0]}'>Edytuj</a><a class='abcd'  href='zadania_admin_usun?id={zadania_db[i][0]}'>Usuń</a></td></tr></tbody>"
         zadania_srodek += zadania_template_srodek
      zadania_template_koniec = "</table>"
      zadania_template = f"{zadania_template_poczatek}{zadania_srodek}<a class='wyloguj abcd'  href='zadania_admin_dodaj'>Dodaj</a>{zadania_template_koniec}"
      if cherrypy.session.get('logged_in'):
         mycursor.execute("select email from admin")
         admin_db = mycursor.fetchall()

         for i in range(len(admin_db)):
            if cherrypy.session["user"] == admin_db[0][i]:
               admin = True
            else:
               admin = False
         if admin == True:
            return template.replace("{table}", zadania_template).replace("{subject}", "Zadania")
         else:
            raise cherrypy.HTTPRedirect('/zadania')
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def zadania_admin_edycja(self, id):
      mycursor.execute(f"select data from zadania where id = '{id}'")
      data_db = mycursor.fetchall()
      mycursor.execute(f"select zadanie from zadania where id = '{id}'")
      zadanie_db = mycursor.fetchall()
      mycursor.execute(f"select przedmiot from zadania where id = '{id}'")
      przedmiot_db = mycursor.fetchall()
      mycursor.execute(f"select opis from zadania where id = '{id}'")
      opis_db = mycursor.fetchall()
      prompt = "<form method='POST' action='/zadania_admin_submit'>"
      prompt += "<table>"
      prompt += "<table><thead><tr><th>data</th><th>zadanie</th><th>przedmiot</th><th>opis</th><th>Zapisywanie</th></tr></thead>"
      prompt += f"<input type='hidden' placeholder='id' value='{id}' name='id'>"
      prompt += f"<td><input placeholder='data' value='{data_db[0][0]}' type='date' name='data'></td>"
      prompt += f"<td><input placeholder='zadanie' value='{zadanie_db[0][0]}' type='input' name='zadanie'></td>"
      prompt += f"<td><input placeholder='przedmiot' value='{przedmiot_db[0][0]}' type='input' name='przedmiot'></td>"
      prompt += f"<td><input placeholder='opis' value='{opis_db[0][0]}' type='input' name='opis'></td>"
      prompt +="<td><button type='submit'>Zapisz</button></form></td>"
      prompt += "</table>"
      if cherrypy.session.get('logged_in'):
         return template.replace("{table}", prompt).replace("{subject}", "Zadania")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def zadania_admin_submit(self, id, data, zadanie, przedmiot, opis):
      sql = f"UPDATE zadania SET zadanie = %s, opis = %s, przedmiot = %s, data = %s WHERE id = {id}"
      values = (zadanie, opis, przedmiot, data)
      mycursor.execute(sql, values)
      mydb.commit()
      if cherrypy.session.get('logged_in'):
         raise cherrypy.HTTPRedirect("/zadania")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')
      

   @cherrypy.expose
   def zadania_admin_dodaj(self):
      prompt = "<form method='POST' action='/zadania_admin_dodaj_submit'>"
      prompt += "<table><thead><tr><th>data</th><th>zadanie</th><th>przedmiot</th><th>opis</th><th>Zapisywanie</th></tr></thead>"
      prompt += f"<td><input placeholder='data' type='date' name='data'></td>"
      prompt += f"<td><input placeholder='zadanie' type='input' name='zadanie'></td>"
      prompt += f"<td><input placeholder='przedmiot' type='input' name='przedmiot'></td>"
      prompt += f"<td><input placeholder='opis' type='input' name='opis'></td>"
      prompt +="<td><button type='submit'>Zapisz</button></td></table></form>"
      if cherrypy.session.get('logged_in'):
         return template.replace("{table}", prompt).replace("{subject}", "Zadania")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')
      

   @cherrypy.expose
   def zadania_admin_dodaj_submit(self, data, zadanie, przedmiot, opis):
      sql = "INSERT INTO `zadania` (`zadanie`, `opis`, `przedmiot`, `data`) VALUES (%s, %s, %s, %s)"
      val = (zadanie, opis, przedmiot, data)
      mycursor.execute(sql, val)
      if cherrypy.session.get('logged_in'):
         raise cherrypy.HTTPRedirect("/zadania")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def zadania_admin_usun(self, id):
      global admin
      if cherrypy.session.get('logged_in'):
         mycursor.execute("select email from admin")
         admin_db = mycursor.fetchall()

         for i in range(len(admin_db)):
            if cherrypy.session["user"] == admin_db[0][i]:
               admin = True
            else:
               admin = False
         if admin == True:
            mycursor.execute(f"DELETE FROM zadania WHERE `zadania`.`id` = {id}")
            mydb.commit()
            raise cherrypy.HTTPRedirect('/zadania_admin')
         else:
            raise cherrypy.HTTPRedirect('/zadania')
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')
      


   @cherrypy.expose
   def plan_lekcji(self):
      global admin
      plan_lekcji_srodek = ""
      mycursor.execute("select * from plan_lekcji")
      plan_lekcji_db = mycursor.fetchall()
      plan_lekcji_template_poczatek = "<table><thead><tr><th>Godzina</th><th>Poniedziałek</th><th>Wtorek</th><th>Środa</th><th>Czwartek</th><th>Piątek</th></tr></thead>"
      for i in range(len(plan_lekcji_db)):
         plan_lekcji_template_srodek = f"<tbody><tr><tr><td>{plan_lekcji_db[i][1]} - {plan_lekcji_db[i][2]}</td><td>{plan_lekcji_db[i][3]}</td><td>{plan_lekcji_db[i][4]}</td><td>{plan_lekcji_db[i][5]}</td><td>{plan_lekcji_db[i][6]}</td><td>{plan_lekcji_db[i][7]}</td></td></tbody>"
         plan_lekcji_srodek += plan_lekcji_template_srodek
      plan_lekcji_template_koniec = "</table>"
      plan_lekcji_template = f"{plan_lekcji_template_poczatek}{plan_lekcji_srodek}{plan_lekcji_template_koniec}"
      if cherrypy.session.get('logged_in'):
         mycursor.execute("select email from admin")
         admin_db = mycursor.fetchall()

         for i in range(len(admin_db)):
            if cherrypy.session["user"] == admin_db[0][i]:
               admin = True
            else:
               admin = False
         if admin == True:
            raise cherrypy.HTTPRedirect('/plan_lekcji_admin')
         else:
            return template.replace("{table}", plan_lekcji_template).replace("{subject}", "Plan lekcji")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')
      

   @cherrypy.expose
   def plan_lekcji_admin(self):
      plan_lekcji_srodek = ""
      mycursor.execute("select * from plan_lekcji")
      plan_lekcji_db = mycursor.fetchall()
      plan_lekcji_template_poczatek = "<table><thead><tr><th>Godzina</th><th>Poniedziałek</th><th>Wtorek</th><th>Środa</th><th>Czwartek</th><th>Piątek</th><th>Edytowanie</th></tr></thead>"
      for i in range(len(plan_lekcji_db)):
         plan_lekcji_template_srodek = f"<tbody><tr><tr><td>{plan_lekcji_db[i][1]} - {plan_lekcji_db[i][2]}</td><td>{plan_lekcji_db[i][3]}</td><td>{plan_lekcji_db[i][4]}</td><td>{plan_lekcji_db[i][5]}</td><td>{plan_lekcji_db[i][6]}</td><td>{plan_lekcji_db[i][7]}</td><td><a class='abcd'  href='plan_lekcji_admin_edycja?id={plan_lekcji_db[i][0]}'>Edytuj</a><a class='abcd'  href='plan_lekcji_admin_usun?id={plan_lekcji_db[i][0]}'>Usuń</a></td></tbody>"
         plan_lekcji_srodek += plan_lekcji_template_srodek
      plan_lekcji_template_koniec = "</table>"
      plan_lekcji_template = f"{plan_lekcji_template_poczatek}{plan_lekcji_srodek}<a class='wyloguj abcd'  href='plan_lekcji_admin_dodaj'>Dodaj</a>{plan_lekcji_template_koniec}"
      if cherrypy.session.get('logged_in'):
         return template.replace("{table}", plan_lekcji_template).replace("{subject}", "Plan lekcji")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def plan_lekcji_admin_edycja(self, id):
      mycursor.execute(f"select * from przedmiot")
      przedmiot_db = mycursor.fetchall()
      mycursor.execute(f"select * from plan_lekcji where id = '{id}'")
      plan_lekcji_db = mycursor.fetchall()
      prompt = "<form method='POST' action='/plan_lekcji_admin_edycja_submit'>"
      prompt += "<table><thead><tr><th>godzina_od</th><th>godzina_do</th><th>Poniedziałek</th><th>Wtorek</th><th>Środa</th><th>Czwartek</th><th>Piątek</th><th>Edytowanie</th></tr></thead>"
      prompt += f"<input type='hidden' type='number' name='id' value={id}>"
      prompt += f"<td><input type='text' name='godziny_od' value={plan_lekcji_db[0][1]}></td>"
      prompt += f"<td><input type='text' name='godziny_do' value={plan_lekcji_db[0][2]}></td>"
      for y in range(5):
         prompt+= f"<td><select name='dane{y+1}'>"
         for i in range(len(przedmiot_db)):
            if przedmiot_db[i][1] == plan_lekcji_db[0][y+3]:
               prompt+= f"<option selected>{przedmiot_db[i][1]}</option>"
            else:
               prompt+= f"<option>{przedmiot_db[i][1]}</option>"
         prompt+= "</select></td>"
      prompt +="<td><button type='submit'>Zapisz</button></td></table></form>"
      if cherrypy.session.get('logged_in'):
         return template.replace("{table}", prompt).replace("{subject}", "Plan lekcji")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')
      

   @cherrypy.expose
   def plan_lekcji_admin_edycja_submit(self, godziny_od, godziny_do, dane1, dane2, dane3, dane4, dane5, id):
      mycursor.execute("UPDATE `plan_lekcji` SET `godziny_od` = %s, `godziny_do` = %s, `poniedziałek` = %s, `wtorek` = %s, `sroda` = %s, `czwartek` = %s, `piatek` = %s WHERE `plan_lekcji`.`id` = %s;", (godziny_od, godziny_do, dane1, dane2, dane3, dane4, dane5, id))
      mydb.commit()
      if cherrypy.session.get('logged_in'):
         raise cherrypy.HTTPRedirect("/plan_lekcji_admin")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def plan_lekcji_admin_dodaj(self):
      global admin
      prompt = "<form method='POST' action='/plan_lekcji_admin_dodaj_submit'>"
      prompt += "<table><thead><tr><th>godzina_od</th><th>godzina_do</th><th>Poniedziałek</th><th>Wtorek</th><th>Środa</th><th>Czwartek</th><th>Piątek</th><th>Edytowanie</th></tr></thead>"
      prompt += f"<td><input placeholder='godziny_od' type='text' name='godziny_od'></td>"
      prompt += f"<td><input placeholder='godziny_do' type='text' name='godziny_do'></td>"
      prompt += f"<td><input placeholder='poniedzialek' type='text' name='poniedzialek'></td>"
      prompt += f"<td><input placeholder='wtorek' type='text' name='wtorek'></td>"
      prompt += f"<td><input placeholder='sroda' type='text' name='sroda'></td>"
      prompt += f"<td><input placeholder='czwartek' type='text' name='czwartek'></td>"
      prompt += f"<td><input placeholder='piatek' type='text' name='piatek'></td>"
      prompt +="<td><button type='submit'>Zapisz</button></td></table></form>"
      if cherrypy.session.get('logged_in'):
         mycursor.execute("select email from admin")
         admin_db = mycursor.fetchall()

         for i in range(len(admin_db)):
            if cherrypy.session["user"] == admin_db[0][i]:
               admin = True
            else:
               admin = False
         if admin == True:
            return template.replace("{table}", prompt).replace("{subject}", "Plan lekcji")
         else:
            raise cherrypy.HTTPRedirect('/plan_lekcji')
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def plan_lekcji_admin_dodaj_submit(self, godziny_od, godziny_do, poniedzialek, wtorek, sroda, czwartek, piatek):
      sql = "INSERT INTO `plan_lekcji` (`godziny_od`, `godziny_do`, `poniedziałek`, `wtorek`, `sroda`, `czwartek`, `piatek`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
      val = (godziny_od, godziny_do, poniedzialek, wtorek, sroda, czwartek, piatek)
      mycursor.execute(sql, val)
      mydb.commit()
      if cherrypy.session.get('logged_in'):
         raise cherrypy.HTTPRedirect("/plan_lekcji")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def plan_lekcji_admin_usun(self, id):
      global admin
      if cherrypy.session.get('logged_in'):
         mycursor.execute("select email from admin")
         admin_db = mycursor.fetchall()

         for i in range(len(admin_db)):
            if cherrypy.session["user"] == admin_db[0][i]:
               admin = True
            else:
               admin = False
         if admin == True:
            mycursor.execute(f"DELETE FROM plan_lekcji WHERE `plan_lekcji`.`id` = {id}")
            mydb.commit()
            raise cherrypy.HTTPRedirect('/plan_lekcji_admin')
         else:
            raise cherrypy.HTTPRedirect('/plan_lekcji')
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def login(self, email, password):
      cherrypy.session['logged_in'] = False
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

      cherrypy.session["user"] = email 

      if dobry_email == 1 and dobre_haslo == 1:
         cherrypy.session['logged_in'] = True
         raise cherrypy.HTTPRedirect("/plan_lekcji")
      if dobry_email == 0:
         return login_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Zły email.</p></div></center>")
      if dobre_haslo == 0:
         return login_page.replace("<!-- {zle okienko} -->", "<center><div class='zle_okienko'><p class='napis'>Złe hasło.</p></div></center>")


   @cherrypy.expose
   def logout(self):
      cherrypy.session['logged_in'] = False
      raise cherrypy.HTTPRedirect('/clear_cookies')
      
   @cherrypy.expose
   def register(self, firstname, lastname, email, password, confirmpassword):
      dobre_imie = 0
      dobre_nazwisko = 0
      dobry_email = 0
      dobre_haslo = 0
      dobre_drugie_haslo = 0
      regex_mail = 0

      mycursor.execute("SELECT email FROM logowanie WHERE email = %s", (email,))
      email_db = mycursor.fetchall()
      mycursor.execute("SELECT password FROM logowanie WHERE password = %s", (password,))
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
         login = "kochamtruskawki998@gmail.com"
         password_sftp = "oflgetnuwfyobuei"
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

   @cherrypy.expose
   def sprawdziany(self):
      global admin
      sprawdziany_srodek = ""
      mycursor.execute("select * from sprawdziany")
      sprawdziany_db = mycursor.fetchall()
      sprawdziany_template_poczatek = "<table><thead><tr><th>data</th><th>przedmiot</th><th>opis</th></tr></thead>"
      for i in range(len(sprawdziany_db)):
         sprawdziany_template_srodek = f"<tbody><tr><td>{sprawdziany_db[i][2]}</td><td>{sprawdziany_db[i][1]}</td><td>{sprawdziany_db[i][3]}</td></tr></tbody>"
         sprawdziany_srodek += sprawdziany_template_srodek
      sprawdziany_template_koniec = "</table>"
      sprawdziany_template = f"{sprawdziany_template_poczatek}{sprawdziany_srodek}{sprawdziany_template_koniec}"
      if cherrypy.session.get('logged_in'):
         mycursor.execute("select email from admin")
         admin_db = mycursor.fetchall()

         for i in range(len(admin_db)):
            if cherrypy.session["user"] == admin_db[0][i]:
               admin = True
            else:
               admin = False

         if admin == True:
            raise cherrypy.HTTPRedirect('/sprawdziany_admin')
         else:
            return template.replace("{table}", sprawdziany_template).replace("{subject}", "Sprawdziany")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')


   @cherrypy.expose
   def sprawdziany_admin(self):
      global admin
      sprawdziany_srodek = ""
      mycursor.execute("select * from sprawdziany")
      sprawdziany_db = mycursor.fetchall()
      sprawdziany_template_poczatek = "<table><thead><tr><th>data</th><th>przedmiot</th><th>opis</th><th>Edytowanie</th></tr></thead>"
      for i in range(len(sprawdziany_db)):
         sprawdziany_template_srodek = f"<tbody><tr><td>{sprawdziany_db[i][2]}</td><td>{sprawdziany_db[i][1]}</td><td>{sprawdziany_db[i][3]}</td><td><a class='abcd'  href='sprawdziany_admin_edycja?id={sprawdziany_db[i][0]}'>Edytuj</a><a class='abcd'  href='sprawdziany_admin_usun?id={sprawdziany_db[i][0]}'>Usuń</a></td></tr></tbody>"
         sprawdziany_srodek += sprawdziany_template_srodek
      sprawdziany_template_koniec = "</table>"
      sprawdziany_template = f"{sprawdziany_template_poczatek}{sprawdziany_srodek}<a class='wyloguj abcd'  href='sprawdziany_admin_dodaj'>Dodaj</a>{sprawdziany_template_koniec}"
      if cherrypy.session.get('logged_in'):
         mycursor.execute("select email from admin")
         admin_db = mycursor.fetchall()

         for i in range(len(admin_db)):
            if cherrypy.session["user"] == admin_db[0][i]:
               admin = True
            else:
               admin = False
         if admin == True:
            return template.replace("{table}", sprawdziany_template).replace("{subject}", "Sprawdziany")
         else:
            raise cherrypy.HTTPRedirect('/sprawdziany')
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def sprawdziany_admin_edycja(self, id):
      mycursor.execute(f"select data from sprawdziany where id = '{id}'")
      data_db = mycursor.fetchall()
      mycursor.execute(f"select przedmiot from sprawdziany where id = '{id}'")
      przedmiot_db = mycursor.fetchall()
      mycursor.execute(f"select opis from sprawdziany where id = '{id}'")
      opis_db = mycursor.fetchall()
      prompt = "<form method='POST' action='/sprawdziany_admin_submit'>"
      prompt += "<table><thead><tr><th>data</th><th>przedmiot</th><th>opis</th><th>Edytowanie</th></tr></thead>"
      prompt += f"<input type='hidden' placeholder='id' value='{id}' name='id'>"
      prompt += f"<td><input placeholder='data' value='{data_db[0][0]}' type='date' name='data'></td>"
      prompt += f"<td><input placeholder='przedmiot' value='{przedmiot_db[0][0]}' type='input' name='przedmiot'></td>"
      prompt += f"<td><input placeholder='opis' value='{opis_db[0][0]}' type='input' name='opis'></td>"
      prompt +="<td><button type='submit'>Zapisz</button></td></table></form>"
      if cherrypy.session.get('logged_in'):
         return template.replace("{table}", prompt).replace("{subject}", "Sprawdziany")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def sprawdziany_admin_submit(self, id, data, przedmiot, opis):
      sql = f"UPDATE sprawdziany SET opis = %s, przedmiot = %s, data = %s WHERE id = {id}"
      values = (opis, przedmiot, data)
      mycursor.execute(sql, values)
      mydb.commit()
      if cherrypy.session.get('logged_in'):
         raise cherrypy.HTTPRedirect("/sprawdziany")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')
      

   @cherrypy.expose
   def sprawdziany_admin_dodaj(self):
      global admin
      prompt = "<form method='POST' action='/sprawdziany_admin_dodaj_submit'>"
      prompt += "<table><thead><tr><th>data</th><th>przedmiot</th><th>opis</th><th>Edytowanie</th></tr></thead>"
      prompt += f"<td><input placeholder='data' type='date' name='data'></td>"
      prompt += f"<td><input placeholder='przedmiot' type='input' name='przedmiot'></td>"
      prompt += f"<td><input placeholder='opis' type='input' name='opis'></td>"
      prompt +="<td><button type='submit'>Zapisz</button></td></table></form>"
      if cherrypy.session.get('logged_in'):
         mycursor.execute("select email from admin")
         admin_db = mycursor.fetchall()

         for i in range(len(admin_db)):
            if cherrypy.session["user"] == admin_db[0][i]:
               admin = True
            else:
               admin = False
         if admin == True:

            return template.replace("{table}", prompt).replace("{subject}", "Sprawdziany")
         else:
            raise cherrypy.HTTPRedirect('/sprawdziany')
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def sprawdziany_admin_dodaj_submit(self, data, przedmiot, opis):
      sql = "INSERT INTO `sprawdziany` (`opis`, `przedmiot`, `data`) VALUES (%s, %s, %s)"
      val = (opis, przedmiot, data)
      mycursor.execute(sql, val)
      mydb.commit()
      if cherrypy.session.get('logged_in'):
         raise cherrypy.HTTPRedirect("/sprawdziany_admin")
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def sprawdziany_admin_usun(self, id):
      global admin
      if cherrypy.session.get('logged_in'):
         mycursor.execute("select email from admin")
         admin_db = mycursor.fetchall()

         for i in range(len(admin_db)):
            if cherrypy.session["user"] == admin_db[0][i]:
               admin = True
            else:
               admin = False
         if admin == True:
            mycursor.execute(f"DELETE FROM sprawdziany WHERE `sprawdziany`.`id` = {id}")
            mydb.commit()
            raise cherrypy.HTTPRedirect('/sprawdziany_admin')
         else:
            raise cherrypy.HTTPRedirect('/sprawdziany')
      else:
         raise cherrypy.HTTPRedirect('/index_login_page')

   @cherrypy.expose
   def oceny(self):
      mycursor.execute(f"select id from logowanie where `email` = {cherrypy.session['user']}")
      id_query_usera = mycursor.fetchall()
      mycursor.execute(f"SELECT oceny.ocena, oceny.typ, oceny.data, oceny.id_przedmiot, przedmiot.nazwa FROM oceny INNER JOIN przedmiot ON oceny.id_przedmiot = przedmiot.id WHERE oceny.id_ucznia = '{id_query_usera[0][0]}'")
      oceny_db = mycursor.fetchall()
      prompt = "<table><thead><tr><th>data</th><th>ocena</th><th>przedmiot</th><th>typ</th></tr></thead>"
      for i in range(len(oceny_db)):
         prompt += f"<tr><td>{oceny_db[i][2]}</td>"
         prompt += f"<td>{oceny_db[i][0]}</td>"
         prompt += f"<td>{oceny_db[i][4]}</td>"
         prompt += f"<td>{oceny_db[i][1]}</td></tr>"
      prompt += "</table>"

      return template.replace("{table}", prompt).replace("{subject}", "Oceny")


main = main()
cherrypy.tree.mount(main, '/')
cherrypy.config.update({
   'server.socket_port': 25565,
   'engine.autoreload_on': True,
   'tools.sessions.on': True,
   'tools.sessions.storage_type': 'ram',
   'tools.sessions.locking': 'explicit',
   'tools.sessions.name': 'sesja_logowania',
   'tools.sessions.timeout': 60,
   'tools.encode.on': True,
   'tools.encode.key': secret_key,
   'tools.encode.encode_headers': True
   })

cherrypy.tools.sessions.my_session = cherrypy.Tool('before_handler', Session())
cherrypy.quickstart(main)
