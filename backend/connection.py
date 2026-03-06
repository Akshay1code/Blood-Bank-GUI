import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="akshay47@2006",
            database="blood_bank",
            port=3306
        )
        print("Database connected successfully")
        return conn
    except mysql.connector.Error as e:
        print("Database connection error:", e)
        return None
