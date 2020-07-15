import mysql.connector
from mysql.connector import errorcode
import datetime

def write_values(name_product, price_of, price_per, promotion, created, updated):
    try:
        db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database='carrefourdb'
        )
        cursor = db_connection.cursor()
        add_product = """ INSERT INTO product (name_product, price_of, price_per, promotion, created, updated)
                    VALUES
                    (%s, %s, %s, %s, %s, %s) """
        
        data = (str(name_product), str(price_of), str(price_per), str(promotion), created, updated)

        cursor.execute(add_product, data)
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

def delete_values_into_product():
    try: 
        db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database='carrefourdb'
        )
         
        cursor = db_connection.cursor()

        delete_product_before_insert = """ Delete from product """
        cursor.execute(delete_product_before_insert)
        db_connection.commit()
        print(cursor.rowcount, "record deleted")

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