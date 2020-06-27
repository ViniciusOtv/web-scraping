import sqlite3

sqlite_file = 'carrefour.db'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

name_category = 'vinicius'
link = 'dasjghdsah'
creation_date = '05/09/1994'
update_date = '05/09/1994'

print('inserindo dados na tabela')
c.execute("""INSERT INTO category(name_category, link, created, updated)
VALUES (?, ?, ?, ?)
""", (name_category, link, creation_date, update_date))
print('dados inseridos')
