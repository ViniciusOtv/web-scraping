import mysql.connector
from mysql.connector import errorcode
import datetime


def write_values(category_name, link, created, updated):
    try:
        db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database='carrefourdb'
        )
        cursor = db_connection.cursor()
        add_category = """ INSERT INTO category (category_name, link, created, updated)
                    VALUES
                    (%s, %s, %s, %s) """
        
        data = (str(category_name), str(link), created, updated)

        cursor.execute(add_category, data)
        db_connection.commit()
        print(cursor.rowcount, "record inserted.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    finally:
        if (db_connection.is_connected()):
             cursor.close()
             db_connection.close()
             print("MySQL connection is closed")

# write_values('Teste', 'teste', '2020-06-29 19:58:39', '2020-06-29 19:58:39' )
