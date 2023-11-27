import psycopg2
from datetime import time
import os
from dotenv import load_dotenv
from utils import calculate_eating_amount, get_menu_array

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(os.environ['DB_URL'])
    return conn

def float_to_time(current_time):
    hours = int(current_time)
    minutes = int((current_time - hours) * 60)

    return time(hours, minutes) 


def get_airline_id(conn, airline_name):
    cursor = conn.cursor()
    cursor.execute(f'SELECT id FROM airline WHERE name = %s', (airline_name,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    else:
        # Если авиакомпания не найдена, можно вернуть None или выбросить исключение
        return None


def add_special_menus(conn, airline_id, special_menu_codes):
    special_menus = []
    cursor = conn.cursor()
    for special_menu_code in special_menu_codes:
        cursor.execute('''
            SELECT
                smd.specialmenu_id,
                d.name
            FROM
                specialmenudish AS smd
            JOIN
                dish AS d ON smd.dish_id = d.id
            WHERE
                smd.specialmenu_id IN (
                    SELECT id FROM specialmenu WHERE code = %s AND airline_id = %s
                )
        ''', (special_menu_code["code"], airline_id))
        special_menu_dishes = cursor.fetchall()
        if special_menu_dishes:
            special_menu = {
                "code": special_menu_code["code"],
                "amount": special_menu_code["amount"],
                "dishes": [dish[1] for dish in special_menu_dishes]
            }
            special_menus.append(special_menu)
    cursor.close()
    return special_menus

# Обновление функции getMenu
def getMenu(conn, airline_name, flight_duration, class_of_service_data, takeoff_time, landing_time, special_menu_codes):
    airline_id = get_airline_id(conn, airline_name)

    if airline_id is not None:
        cursor = conn.cursor()

        eating_amount_info = calculate_eating_amount(flight_duration)
        menu_array_info = get_menu_array(flight_duration, float_to_time(takeoff_time))

        menu = []
        special_menu = [] 

        # Добавляем основные меню
        for service_class in class_of_service_data:
            for item in menu_array_info:
                cursor.execute(f'''
                    SELECT
                        m.quality_type,
                        m.time_type,
                        m.temperature_type,
                        ARRAY_AGG(d.name) AS dishes
                    FROM
                        menu AS m
                    JOIN
                        menudish AS md ON m.id = md.menu_id
                    JOIN
                        dish AS d ON md.dish_id = d.id
                    WHERE
                        m.airline_id = %s
                        AND m.quality_type = %s
                        AND m.time_type = %s
                        AND m.temperature_type = %s
                    GROUP BY
                        quality_type, time_type, temperature_type;
                ''', (airline_id, service_class["type"], item, eating_amount_info["type"]))

                result = cursor.fetchall()
                if result:
                    menu.append({
                        "quality_type": service_class["type"],
                        "amount": service_class["amount"],
                        "time_type": item,
                        "temperature_type": eating_amount_info["type"],
                        "dishes": result[0][3]
                    })

        # Добавляем специальные меню
        if (special_menu_codes):
            special_menus = add_special_menus(conn, airline_id, special_menu_codes)
            special_menu.extend(special_menus)

        cursor.close()
        conn.close()
        return {"menu": menu, "special_menu": special_menu} 


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