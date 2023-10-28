from flask import Flask, request, json, jsonify
from flask_cors import CORS
from food_index_calc import FoodIndex
from db import getMenu, get_db_connection, getAirlines
from handle_food_index import handle_food_index
import json
from flask_restx import Api, Resource, fields, marshal

app = Flask(__name__)
CORS(app)

api = Api(app, version='1.0', title='Air Food API', description='API for inflight meal selection')

menu_model = api.model('Menu', {
    'menu': fields.List(fields.String),
})

airline_model = api.model('Airline', {
    'airlines': fields.List(fields.Nested(api.model('AirlineInfo', {
        'id': fields.String,
        'name': fields.String,
    }))),
})


conn = None

@api.route('/menu')
class MenuResource(Resource):
    @api.expect(menu_model)
    def post(self):
        """
        Retrieve menu for the given parameters.
        """
        try:
            reqBody = request.json
            if ("flight_duration") not in reqBody:
                error_message = "Параметр 'flight_duration' отсутствует в запросе."
                return {'error': error_message}, 400
            elif ("class_of_service_data") not in reqBody:
                error_message = "Параметр 'class_of_service_data' отсутствует в запросе."
                return {'error': error_message}, 400
            elif ("takeoff_time") not in reqBody:
                error_message = "Параметр 'takeoff_time' отсутствует в запросе."
                return {'error': error_message}, 400
            elif ("landing_time") not in reqBody:
                error_message = "Параметр 'landing_time' отсутствует в запросе."
                return {'error': error_message}, 400
            elif ("airline_name") not in reqBody:
                error_message = "Параметр 'airline_name' отсутствует в запросе."
                return {'error': error_message}, 400
            

            menu = getMenu(
                conn, 
                reqBody["airline_name"], 
                reqBody["flight_duration"], 
                reqBody["class_of_service_data"],
                reqBody["takeoff_time"],
                reqBody["landing_time"],
                reqBody["special_menu_codes"],
            ) 
            if (menu):
                menu_data = {'menu': menu[3]}
                return menu_data, 200
            else:
                menu_json = {'message': 'Меню не существует'}
                return menu_json, 404
        except Exception as e:
            raise e
    

@api.route('/airlines')
class AirlinesResource(Resource):
    @api.marshal_with(airline_model, as_list=True)
    def get(self):
        """
        Get the list of available airlines.
        """
        try:
            conn = get_db_connection()
            airlines = getAirlines(conn)
            result = [{'id': item[0], 'name': item[1]} for item in airlines]
            if (result):
                return {'airlines': result}, 200
            else:
                return {'error': 'Авиакомпании не найдены'}, 404
        except Exception as e:
            raise e
    
    
if __name__ == '__main__':
    conn = get_db_connection()
    app.run(debug=True, port=8000)
