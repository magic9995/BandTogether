from readline import insert_text
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ENTER PASSWORD"
)

mycursor = mydb.cursor()
#Using the database user
mycursor.execute("USE USER")



#mycursor.execute("CREATE DATABASE USER")

# In MySQL DB decimal(4,2) allows entering only a total of 4 digits. As you see in decimal(4,2), it means you can enter a total of 4 digits out of which two digits are meant for keeping after the decimal point.

# So, if you enter 100.0 in MySQL database, it will show an error like "Out of Range Value for column".

# So, you can enter in this range only: from 00.00 to 99.99.


#mycursor.execute("CREATE TABLE spotify (username VARCHAR(255), liveness decimal(4,2), valence decimal(4,2), danceability decimal(4,2), loudness decimal(4,2), mode decimal(4,2), acousticness decimal(4,2), instrumentalness decimal(4,2), tempo decimal(4,2), energy decimal(4,2), longitude int, latitude int)")

#mycursor.execute("SHOW TABLES")

def insertData(username, liveness, valence, danceability, loudness, mode, acousticness, instrumentalness, tempo, energy, longitude, latitude):
    mySql_insert_query = """INSERT INTO spotify (username, liveness, valence, danceability, loudness, mode, acousticness, instrumentalness, tempo, energy, longitude, latitude) 
                           VALUES 
                           ("{}", {}, {}, {}, {},{}, {}, {}, {},{},{},{})""".format(username, liveness, valence, danceability, loudness, mode, acousticness, instrumentalness, tempo, energy, longitude, latitude)
    mycursor.execute(mySql_insert_query)
    mydb.commit()
    print("Added the value")

def deleteWhereUserNameIs(username):
  sql = "DELETE FROM spotify WHERE username = '{}'".format(username)
  mycursor.execute(sql)
  mydb.commit()
  print("Delete the user with username " + username)


def printValuesInTable():  
  print("PRINTING VALUES FROM TABLE.....")
  # execute your query
  mycursor.execute("SELECT * FROM spotify")
  
  # fetch all the matching rows 
  result = mycursor.fetchall()
  
  # loop through the rows
  for row in result:
    print(row)
    print("\n")

def modifySpotifyData(username, listSpotifyData):
  deleteWhereUserNameIs(username)
  insertData(listSpotifyData[0],listSpotifyData[1],listSpotifyData[2],listSpotifyData[3],listSpotifyData[4],listSpotifyData[5],listSpotifyData[6],listSpotifyData[7],listSpotifyData[8],listSpotifyData[9], listSpotifyData[10], listSpotifyData[11])

def returnSpotifyDataForUsername(username):
  sql = "SELECT * FROM spotify WHERE username = '{}'".format(username)
  mycursor.execute(sql)
  result = mycursor.fetchone()
  return {"username": result[0], "liveness": result[1], "valence": result[2], "danceability": result[3], "loudness": result[4], "mode": result[5], "acousticness": result[6], "instrumentalness": result[7], "tempo": result[8], "energy": result[9],"longitude": result[10], "latitude": result[11] }


def returnDataOfTableInList():
    listOutput = []
    mycursor.execute("SELECT * FROM spotify")
    # fetch all the matching rows 
    result = mycursor.fetchall()
    # loop through the rows
    for row in result:
        listOutput.append({"username": row[0], "liveness": row[1], "valence": row[2], "danceability": row[3], "loudness": row[4], "mode": row[5], "acousticness": row[6], "instrumentalness": row[7], "tempo": row[8], "energy": row[9],"longitude": row[10], "latitude": row[11] })
    return listOutput

def returnUserLocation(username):
    sql = "SELECT longitude,latitude FROM spotify WHERE username = '{}'".format(username)
    mycursor.execute(sql)
    result = mycursor.fetchone()

    return {"longitude": result[0], "latitude":result[1]}

def containsUser(username):
   sql = "SELECT * FROM spotify WHERE username = '{}'".format(username)
   mycursor.execute(sql)
   result = mycursor.fetchone()
   if (result is None):
     return False
   else: 
     return True




#insertData("NULL","NULL" ,"NULL" ,"NULL" ,"NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL")
deleteWhereUserNameIs("NULL")
#deleteWhereNameIs("name2")
#printValuesInTable()
print(returnUserLocation("username2"))
# print(containsUser("username2"))
#print(returnSpotifyDataForUsername("username1"))
#print(returnDataOfTableInList())
# print(returnUserDataForUsername("username1"))