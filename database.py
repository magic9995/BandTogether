from readline import insert_text
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ENTER PASSWORD"
)

mycursor = mydb.cursor()
#Using the table user
mycursor.execute("USE USER")

#mycursor.execute("CREATE DATABASE USER")


#mycursor.execute("CREATE TABLE users (name VARCHAR(255), password VARCHAR(255), email VARCHAR(255), username VARCHAR(255), phone int)")


def insertUser(name, password, email, username, phone):
  mySql_insert_query = """INSERT INTO Users (name, password, email, username, phone) 
                           VALUES 
                           ("{}", "{}", "{}", "{}", {})""".format(name, password, email, username, phone)
  mycursor.execute(mySql_insert_query)
  mydb.commit()
  print("Added the value")

def deleteWhereNameIs(name):
  sql = "DELETE FROM USERS WHERE name = '{}'".format(name)
  mycursor.execute(sql)
  mydb.commit()
  print("Delete the user with name " + name)

def deleteWhereUserNameIs(username):
  sql = "DELETE FROM USERS WHERE username = '{}'".format(username)
  mycursor.execute(sql)
  mydb.commit()
  print("Delete the user with name " + username)

def returnPasswordWhereNameIs(name):
  sql = "SELECT PASSWORD FROM USERS WHERE name = '{}'".format(name)
  mycursor.execute(sql)
  result = mycursor.fetchall()
  for password in result:
    return password[0]


def printValuesInTable():  
  print("PRINTING VALUES FROM TABLE.....")
  # execute your query
  mycursor.execute("SELECT * FROM USERS")
  
  # fetch all the matching rows 
  result = mycursor.fetchall()
  
  # loop through the rows
  for row in result:
    print(row)
    print("\n")

def modifyUserData(username, listUserData):
  deleteWhereUserNameIs(username)
  insertUser(listUserData[0],listUserData[1],listUserData[2],listUserData[3],listUserData[4])

def returnUserData(username):
  sql = "SELECT * FROM USERS WHERE username = '{}'".format(username)
  mycursor.execute(sql)
  result = mycursor.fetchone()
  return(result)




#insertUser("name2", "password2", "email2", "username2", 123456)
#deleteWhereNameIs("name2")
printValuesInTable()
#print(returnPasswordWhereNameIs("name1"))
#modifyUserData("username1",["nameNew","passwordNew","emailNew","usernameNew",123456])
print(returnUserData("username1"))