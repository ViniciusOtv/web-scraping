import sqlite3
from sqlite3 import Error
import datetime

database = r"C:\Users\vinicius.silva\source\repos\python-projects\web-scraping-online-market\selenium-web-scraping\carrefour\carrefour.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
         specified by db_file
     :param db_file: database file
     :return: Connection object or None
     """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        print('criando a conexão')
    except Error as e:
        print(e)
    return conn


def create_table(conn, sql_table):
    """ create a table from the sql_table statement
    :param conn: Connection object
    :param sql_table: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql_table)
    except Error as e:
        print(e)


print('tabela criada ')
date = datetime.datetime.now()


def main():
    category_table = """CREATE TABLE IF NOT EXISTS category (
                                        id_category integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        name_category TEXT NOT NULL,
                                        link TEXT NOT NULL,
                                        created Date Not Null,
                                        updated Date NOT NULL
                                    ); """

    conn = create_connection(database)
    if conn is not None:
        print('criando a tabela')
        create_table(conn, category_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()

def connection_validate():
    conn = create_connection(database)
    if conn is not None:
        return conn
    else:
        print("Error! cannot create the database connection.")

# def write_values_into_category(name_category, link, creation_date, update_date):
#     conn = connection_validate()
#     conn.execute(''' INSERT INTO category(name_category, link, created, updated)
#     VALUES (?, ?, ?, ?) ''', (name_category, link, creation_date, update_date))
#     print('inserindo dados na tabela')

def read_category():
    conn = connection_validate()
    print('consultando tabela de categorias')
    conn.execute("SELECT * FROM category")