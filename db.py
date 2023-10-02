import psycopg2

db_params = {
    'host': 'localhost',
    'port': 5000,
    'database': 'air_food',  
    'user': 'postgres',
    'password': 'j4Ema3_w1'
}

def getMenu(airline_name, quality_type):
    conn = psycopg2.connect(**db_params)

    cursor = conn.cursor()

    cursor.execute(f'''
                SELECT menu.*
                FROM menu
                JOIN airlines ON menu.airline_id = airlines.id
                WHERE airlines.airline_name = '{airline_name}';
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

menu = getMenu('Аэрофлот', 'good')
print(menu)