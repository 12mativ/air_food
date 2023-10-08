from flask import Flask, request, json
from flask_cors import CORS
from food_index_calc import FoodIndex
from db import getMenu, get_db_connection, getAirlines
from handle_food_index import handle_food_index
import json

app = Flask(__name__)
CORS(app)

conn = None

@app.route('/menu', methods=['POST'])
def createMenu():
    try:
        reqBody = request.json
        if ("flight_duration") not in reqBody:
            error_message = "Параметр 'flight_duration' отсутствует в запросе."
            return json.dumps({'error': error_message}, ensure_ascii=False), 400
        elif ("class_of_service_data") not in reqBody:
            error_message = "Параметр 'class_of_service_data' отсутствует в запросе."
            return json.dumps({'error': error_message}, ensure_ascii=False), 400
        elif ("airline_name") not in reqBody:
            error_message = "Параметр 'airline_name' отсутствует в запросе."
            return json.dumps({'error': error_message}, ensure_ascii=False), 400
        
        food_index = FoodIndex()

        food_index.calculate_index(
            flight_duration=reqBody["flight_duration"], 
            class_of_service_data=reqBody["class_of_service_data"],
        )

        current_index = food_index.get_index()
        current_quality_type = handle_food_index(current_index)

        # TODO DELETE PRINTS    
        print(f'Current index: {current_index}')
        print(f'Current quality type: {current_quality_type}')

        menu = getMenu(conn, reqBody["airline_name"], current_quality_type)

        if (menu):
            menu_json = json.dumps({'menu': menu[3]}, ensure_ascii=False)
            return menu_json, 200
        else:
            menu_json = json.dumps({'message': 'Меню не существует'}, ensure_ascii=False)
            return menu_json, 404
    except Exception as e:
        raise e
    

@app.route('/airlines', methods=['GET'])
def get_airlines():
    try:
        conn = get_db_connection()
        airlines = getAirlines(conn)  # Вызываем вашу функцию для получения данных из базы данных
        
        
        # Создаем список объектов с полями id и name
        data = [{'id': str(item[0]), 'name': item[1]} for item in airlines]

        # Преобразуем список объектов в JSON-массив
        json_array = json.dumps(data, ensure_ascii=False)

        # print(airlines)
        if (airlines):
                # airlines_json = json.dumps(airlines, ensure_ascii=False)
                return json_array, 200
        else:
            return json({'error': 'No airlines found'}), 404
    except Exception as e:
        raise e
    
    
if __name__ == '__main__':
    conn = get_db_connection()
    app.run(debug=True, port=8000)