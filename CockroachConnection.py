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
            "CREATE TABLE IF NOT EXISTS Users (name VARCHAR(255), password VARCHAR(255), email VARCHAR(255), username VARCHAR(255), phone int)"
        )
    conn.commit()

def insertUser(conn,name, password, email, username, phone):
    with conn.cursor() as cur:
        cur.execute(
           f"""INSERT INTO Users (name, password, email, username, phone) VALUES ('{name}', '{password}', '{email}', '{username}', {phone})"""
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
        cur.execute("SELECT * FROM USERS WHERE username = '{}'".format(username))
        logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
        result = cur.fetchone()
    conn.commit() 
    return(result)

def main():
    conn = psycopg2.connect("postgresql://vaidya45:xTFH37o0EEDY3gOd-UyZrw@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dblast-horgi-470")
    create_table(conn)
    insertUser(conn,"Raghav", "password2", "email2", "username2", 123456)
    insertUser(conn,"Ram", "password3", "email22", "username21", 123456)
    print("Table:- ")
    print_values(conn)
    #print("Raghav's Data:- ")
    #print(returnUserData(conn,"username2"))
    #print(returnPasswordWhereUserNameIs(conn,"username2"))
    #modifyUserData(conn,"username2",["ABC","ppp","emaaill","ussrrrnnnmmm",10])
    conn.close()

    
"""database connection string

For cockroach demo, use
'postgresql://<username>:<password>@<hostname>:<port>/bank?sslmode=require',
with the username and password created in the demo cluster, and the hostname
and port listed in the (sql/tcp) connection parameters of the demo cluster
welcome message.

For CockroachCloud Free, use
'postgres://<username>:<password>@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/<cluster-name>.bank?sslmode=verify-full&sslrootcert=<your_certs_directory>/cc-ca.crt'.

If you are using the connection string copied from the Console, your username,
password, and cluster name will be pre-populated. Replace
<your_certs_directory> with the path to the 'cc-ca.crt' downloaded from the
Console.

"""

if __name__ == "__main__":
    main()

