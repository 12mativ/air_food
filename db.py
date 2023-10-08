import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# db_params = {
#     'host': os.environ['DB_HOST'],
#     'port': os.environ['DB_PORT'],
#     'database': os.environ['DB_DATABASE'],  
#     'user': os.environ['DB_USER'],
#     'password': os.environ['DB_PASSWORD']
# }

def get_db_connection():
    conn = psycopg2.connect(os.environ['DB_URL'])
    return conn

def getMenu(conn, airline_name, quality_type):
    if(conn != None):
        cursor = conn.cursor()

        cursor.execute(f'''
                    SELECT menu.*
                    FROM menu
                    JOIN airline ON menu.airline_id = airline.id
                    WHERE airline.name = '{airline_name}';
        ''')

        result = cursor.fetchall()

        found_medium_menu = False
        for menu in result:
            if (menu[1] == quality_type):
                found_medium_menu = True
                return menu
        if not found_medium_menu:
            return None
            
        cursor.close()
        conn.close()


def getAirlines(conn):
    if(conn != None):
        cursor = conn.cursor()

        cursor.execute(f'''
                    SELECT *
                    FROM airline
        ''')

        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return result