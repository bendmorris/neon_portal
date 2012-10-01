import sqlite3 as dbapi

con = dbapi.connect('neon_portal.db')
cur = con.cursor()
try: cur.execute('DROP TABLE sp_list_splistdocument')
except: pass