import time
import random
import logging
from argparse import ArgumentParser, RawTextHelpFormatter

import psycopg2
from psycopg2.errors import SerializationFailure

#mycursor.execute("CREATE DATABASE USER")


#mycursor.execute("CREATE TABLE users (name VARCHAR(255), password VARCHAR(255), email VARCHAR(255), username VARCHAR(255), phone int)")

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Users (name VARCHAR(255), password VARCHAR(255), email VARCHAR(255), username VARCHAR(255) PRIMARY KEY, phone int)"
        )
    conn.commit()

def insertUser(conn,name, password, email, username, phone):
    with conn.cursor() as cur:
            cur.execute(
        f"""INSERT INTO Users (name, password, email, username, phone) VALUES ('{name}', '{password}', '{email}', '{username}', 5)"""
        )
    print("Added the value")
    conn.commit()
  

def deleteWhereUserNameIs(conn,username):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM USERS WHERE username = '{}'".format(username))
        logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    print("Deleted the user with name " + username)
    conn.commit() 

def returnPasswordWhereUserNameIs(conn,username):
    with conn.cursor() as cur:
        cur.execute("SELECT PASSWORD FROM Users WHERE username = '{}'".format(username))
        logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
        result = cur.fetchall();
        conn.commit() 
    for password in result:
        return password

def modifyUserData(conn,username, listUserData):
  deleteWhereUserNameIs(conn,username)
  insertUser(conn,listUserData[0],listUserData[1],listUserData[2],listUserData[3],listUserData[4])

def print_values(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Users")
        logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        print(f"Balances at {time.asctime()}:")
        for row in rows:
            print(row)

def returnUserData(conn,username):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Users WHERE username = '{}'".format(username))
        logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
        result = cur.fetchone()
    conn.commit() 
    return {"name": result[0],"password": result[1], "email": result[2], "username": result[3], "phone": result[4] }

def returnDataOfTableInList(conn):
    listOutput = []
    with conn.cursor() as cur:
        cur.execute(
          "SELECT * FROM Users"
        )
        result = cur.fetchall()
    conn.commit()
    for row in result:
        listOutput.append({"name": row[0],"password": row[1], "email": row[2], "username": row[3], "phone": row[4] })
    return(listOutput)

def containsUser(conn,username):
    with conn.cursor() as cur:
        cur.execute(
          "SELECT * FROM Users WHERE username = '{}'".format(username)
        )
        result = cur.fetchone()
    conn.commit()
    if (result is None):
        return False
    else: 
        return True

def getConn():
    conn = psycopg2.connect("postgresql://vaidya45:xTFH37o0EEDY3gOd-UyZrw@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dblast-horgi-470")
    return conn


