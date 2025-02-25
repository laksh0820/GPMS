import psycopg2

DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_HOST = ""

# connect to database
try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host=DB_HOST)
    print("Database connected successfully")
except:
    print("Database not connected successfully")

# creating a cursor
db = conn.cursor() 

# DROP all previous tables
db.execute("""""")

# create table
db.execute("""""")

db.close()
conn.close()


