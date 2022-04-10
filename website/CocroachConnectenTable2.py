import time
import random
import logging
from argparse import ArgumentParser, RawTextHelpFormatter

import psycopg2
from psycopg2.errors import SerializationFailure

from CockroachConnection import modifyUserData

#mycursor.execute("CREATE DATABASE USER")

# In MySQL DB decimal(4,2) allows entering only a total of 4 digits. As you see in decimal(4,2), it means you can enter a total of 4 digits out of which two digits are meant for keeping after the decimal point.

# So, if you enter 100.0 in MySQL database, it will show an error like "Out of Range Value for column".

# So, you can enter in this range only: from 00.00 to 99.99.

#mycursor.execute("SHOW TABLES")

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute(
           "CREATE TABLE IF NOT EXISTS spotify (username VARCHAR(255), liveness decimal(4,2), valence decimal(4,2), danceability decimal(4,2), loudness decimal(4,2), mode decimal(4,2), acousticness decimal(4,2), instrumentalness decimal(4,2), tempo decimal(4,2), energy decimal(4,2),longitude int, latitude int)"
        )
    conn.commit()

def insertData(conn,username, liveness, valence, danceability, loudness, mode, acousticness, instrumentalness, tempo, energy,longitude,latitude):
    with conn.cursor() as cur:
        cur.execute(
           f"""INSERT INTO spotify (username, liveness, valence, danceability, loudness, mode, acousticness, instrumentalness, tempo, energy,longitude,latitude) 
                           VALUES 
                           ('{username}', {liveness}, {valence}, {danceability}, {loudness},{mode}, {acousticness}, {instrumentalness}, {tempo},{energy},{longitude},{latitude})"""
        )
    print("Added the value")
    conn.commit()

def deleteWhereUserNameIs(conn,username):
    with conn.cursor() as cur:
        cur.execute(
           "DELETE FROM spotify WHERE username = '{}'".format(username)
        )
    print("Delete the user with username " + username)
    conn.commit()

def print_values(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM spotify")
        rows = cur.fetchall()
        conn.commit()
        for row in rows:
            print(row)

def modifySpotifyData(conn,username, listSpotifyData):
  deleteWhereUserNameIs(conn,username)
  insertData(conn,listSpotifyData[0],listSpotifyData[1],listSpotifyData[2],listSpotifyData[3],listSpotifyData[4],listSpotifyData[5],listSpotifyData[6],listSpotifyData[7],listSpotifyData[8],listSpotifyData[9],listSpotifyData[10],listSpotifyData[11])

def returnSpotifyDataOfUsername(conn,username):
    with conn.cursor() as cur:
        cur.execute(
          "SELECT * FROM spotify WHERE username = '{}'".format(username)
        )
        result = cur.fetchone()
    conn.commit()
    return {"username": result[0], "liveness": result[1], "valence": result[2], "danceability": result[3], 
    "loudness": result[4], "mode": result[5], 
    "acousticness": result[6], "instrumentalness": result[7], 
    "tempo": result[8], "energy": result[9],
    "longitude": result[10], "latitude": result[11] }

def returnDataOfTableInList(conn):
    listOutput = []
    with conn.cursor() as cur:
        cur.execute(
          "SELECT * FROM spotify"
        )
        result = cur.fetchall()
    conn.commit()
    for row in result:
        listOutput.append({"username": row[0], "liveness": row[1], "valence": row[2], "danceability": row[3], "loudness": row[4], "mode": row[5], "acousticness": row[6], "instrumentalness": row[7], "tempo": row[8], "energy": row[9],"longitude": row[10], "latitude": row[11] })
    return(listOutput)

def returnUserLocation(conn,username):
    with conn.cursor() as cur:
        cur.execute(
          "SELECT longitude,latitude FROM spotify WHERE username = '{}'".format(username)
        )
        result = cur.fetchone()
    conn.commit()
    return {"longitude": result[0], "latitude":result[1]}

def containsUser(conn,username):
    with conn.cursor() as cur:
        cur.execute(
          "SELECT * FROM spotify WHERE username = '{}'".format(username)
        )
        result = cur.fetchone()
    conn.commit()
    if (result is None):
        return False
    else: 
        return True
    
def checkWithinRangeUsingLoop(conn,username):
    listOutput = []
    listData =  returnDataOfTableInList(conn)
    dictLocation = returnUserLocation(conn,username)
    latitude = dictLocation["latitude"]
    longitude = dictLocation["longitude"]

    for dictData in listData:
        localLat = dictData["latitude"]
        localLong = dictData["longitude"]
        insideSQRT = math.pow(69.1*(localLat - latitude),2) + math.pow(69.1*(localLong - longitude)*math.cos(localLat/57.3),2)
        if (math.sqrt(insideSQRT) < 100):
            listOutput.append(dictData)
    return listOutput

def getConn():
    conn = psycopg2.connect("postgresql://vaidya45:xTFH37o0EEDY3gOd-UyZrw@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dblast-horgi-470")
    return conn
