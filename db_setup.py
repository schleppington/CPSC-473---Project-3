import sqlite3
con = sqlite3.connect('planner.db') # Warning: This file is created in the current directory
con.execute("CREATE TABLE users (user_id INTEGER PRIMARY KEY, user_first_name char(50) NOT NULL, user_last_name char(50) NOT NULL, username char(50) NOT NULL, password char(50) NOT NULL)")
con.execute("INSERT INTO users (user_first_name, user_last_name, username, password) VALUES ('Richard', 'Fields', 'rtfjr86', 'password')")
con.commit()
