from flask import Flask, request, json
from food_index_calc import FoodIndex
from db import getMenu
from handle_food_index import handle_food_index

app = Flask(__name__)

@app.route('/menu', methods=['POST'])
def create_task():
    reqBody = request.json
    
    food_index = FoodIndex()

    food_index.calculate_index(
        passengers=reqBody["passengers"], 
        flight_duration=reqBody["flight_duration"], 
        class_of_service=reqBody["class_of_service"],
    )

    current_index = food_index.get_index()
    current_quality_type = handle_food_index(current_index)

    # TODO DELETE PRINTS    
    print(f'Current index: {current_index}')
    print(f'Current quality type: {current_quality_type}')

    menu = getMenu(reqBody["airline_name"], current_quality_type)

    if (menu):
        menu_json = json.dumps({'menu': menu[3]}, ensure_ascii=False)
        return menu_json, 200
    else:
        menu_json = json.dumps({'message': 'Меню не существует'}, ensure_ascii=False)
        return menu_json, 404
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)