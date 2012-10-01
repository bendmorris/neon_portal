def get_connection():
    import psycopg2 as dbapi
    con = dbapi.connect(host='serenity.bluezone.usu.edu', port=5432, user='bendmorris', password='lbwaE1995', database='dodobase')
    return con
    
CONNECTION = get_connection()

def get_site_ids():
    cursor = CONNECTION.cursor()
    cursor.execute('SELECT site_id FROM site_data.site_info_v11')
    
