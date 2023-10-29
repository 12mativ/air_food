import psycopg2
from datetime import datetime, time
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

def calculate_eating_amount(flight_duration):
    if(flight_duration >= 1 and flight_duration <= 3):
        return {'amount': 1, 'type': 'cold'}
    elif(flight_duration > 3 and flight_duration <= 6):
        return {'amount': 1, 'type': 'hot'}
    elif(flight_duration > 6):
        return{'amount': 2, 'type': 'hot'}
    else:
        return None
    
def calculate_menu_timetype(takeoff_time, landing_time, flight_duration):
    return {'time_type': ['breakfast', 'lunch'], 'temperature_type': 'hot'}

def recognize_time_interval(current_time):
    
    # Определение времени начала и конца каждого интервала
    breakfast_start = time(5, 0)
    breakfast_end = time(9, 59)

    lunch_start = time(10, 0)
    lunch_end = time(16, 0)

    dinner_start = time(16, 0)
    dinner_end = time(4, 59)  # До 4:59 утра следующего дня

    # Текущее время, для которого вы хотите определить принадлежность к интервалам
    # Проверка, к какому интервалу относится текущее время
    if breakfast_start <= current_time <= breakfast_end:
        return ("Завтрак")
    elif lunch_start <= current_time <= lunch_end:
        return ("Обед")
    elif current_time >= dinner_start or current_time <= dinner_end:
        return ("Ужин")
    else:
        return ("Введено неверное время")

def calculate_count_food(flight_duration, class_of_service_data):
    return

def getMenu(conn, airline_name):
    if(conn != None):
        cursor = conn.cursor()

        cursor.execute(f'''
                    SELECT menu.*
                    FROM menu
                    JOIN airline ON menu.airline_id = airline.id
                    WHERE airline.name = '{airline_name}';
        ''')

        result = cursor.fetchall()

        
        cursor.close()
        conn.close()


def getAirlines(conn):
    if (conn != None):
        cursor = conn.cursor()

        cursor.execute(f'''
                    SELECT *
                    FROM airline
        ''')

        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return result