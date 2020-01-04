import os
import sqlite3
import logging


DATABASE = 'data/pychecker.db'

def open_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def initialize_db():
    try:
        open_db().cursor().execute(create_db_query())
    except sqlite3.Error as e:
        print(e)

def create_db_query():
    sql = """
    CREATE TABLE IF NOT EXISTS "application" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL,
    "check_interval" INTEGER NOT NULL,
	"check_data"	json,
	"expected"	json,
	"http_notification"	json
    );
    """
    return sql

def select(command):
    conn = open_db()
    conn.row_factory = dict_factory

    return conn.cursor().execute(command).fetchall()

def insert(command):
    conn = open_db()
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()
    return cur.lastrowid

def update(command):
    conn = open_db()
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()
    return

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
