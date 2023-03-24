import mysql.connector
import random

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dziennik"
)

mycursor = mydb.cursor()

godziny_od = ["8:00","8:50","9:45","10:35","11:40","12:30","13:25","14:15","15:05"]
godziny_do = ["8:45","9:35","10:30","11:20","12:25","13:15","14:10","15:00","15:50"]
poniedzialek = ["Matematyka","Angielski","Informatyka","Biologia","Fizyka","WF","Religa","Rosyjski","Niemiecki"]
wtorek = ["Matematyka","Angielski","Informatyka","Biologia","Fizyka","WF","Religa","Rosyjski","Niemiecki"]
sroda = ["Matematyka","Angielski","Informatyka","Biologia","Fizyka","WF","Religa","Rosyjski","Niemiecki"]
czwartek = ["Matematyka","Angielski","Informatyka","Biologia","Fizyka","WF","Religa","Rosyjski","Niemiecki"]
piatek = ["Matematyka","Angielski","Informatyka","Biologia","Fizyka","WF","Religa","Rosyjski","Niemiecki"]

random.shuffle(poniedzialek)
random.shuffle(wtorek)
random.shuffle(sroda)
random.shuffle(czwartek)
random.shuffle(piatek)

for i in range(len(godziny_od)):
  query = "INSERT INTO `plan_lekcji` (`godziny_od`, `godziny_do`, `poniedziałek`, `wtorek`, `sroda`, `czwartek`, `piatek`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
  values = (godziny_od[i], godziny_do[i], poniedzialek[i], wtorek[i], sroda[i], czwartek[i], piatek[i])
  mycursor.execute(query, values)
  mydb.commit()