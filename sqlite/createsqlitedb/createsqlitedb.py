# Vyasan Valavil
# Tutorial from Python's website that shows you how to create an SQLite DB
# It cannot over-write a DB with this script, you need to delete it manually each time.

import sqlite3
import time

#it will create the DB if it does not exist
con = sqlite3.connect("tutorial.db")

#we need a database cursor to execute SQL statements
cur = con.cursor()

#now create a table "movie" with 4 columns
cur.execute("CREATE TABLE movie(title, year, score)")

#store the results in a variable
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())

#store a specific table in results
res = cur.execute("SELECT name FROM sqlite_master WHERE name='movie'")
print(res.fetchone())

#insert entries into that table by opening a transaxtion
cur.execute("""
    INSERT INTO movie VALUES
        ('Monty Python and the Holy Grail', 1975, 8.2),
        ('And Now for Something Completely Different', 1971, 7.5)
            """)
#commit those entries
con.commit()

#check if you can see the entry
res = cur.execute("SELECT score FROM movie")
print(res.fetchall())

#now add some values from a list of tuples:
data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]
cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data) #watch out for number of ? marks...
con.commit()  # Remember to commit the transaction after executing INSERT.