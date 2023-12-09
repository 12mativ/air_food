from datetime import datetime, time
from dotenv import load_dotenv
import requests
import os
import pytz

load_dotenv()

# Определение времени начала и конца каждого интервала
breakfast_start = time(5, 0)
breakfast_end = time(10, 0)

lunch_start = time(10, 0)
lunch_end = time(16, 0)

dinner_start = time(16, 0)
dinner_end = time(5, 0)  # До 4:59 утра следующего дня

def recognize_time_interval(current_time):
    # Текущее время, для которого вы хотите определить принадлежность к интервалам
    # Проверка, к какому интервалу относится текущее время
    if breakfast_start < current_time <= breakfast_end:
        return ("breakfast")
    elif lunch_start < current_time <= lunch_end:
        return ("lunch")
    elif current_time > dinner_start or current_time <= dinner_end:
        return ("dinner")
    else:
        return ("Введено неверное время")
    

def time_to_minutes(t):
    return t.hour * 60 + t.minute

def recognize_time_amount(flight_duration, takeoff_time):
    flight_duration_in_minutes = flight_duration * 60
    
    breakfast_time = 0
    lunch_time = 0
    dinner_time = 0

    current_time_interval = recognize_time_interval(takeoff_time)
    if (current_time_interval == "breakfast"):
        difference_minutes = time_to_minutes(breakfast_end) - time_to_minutes(takeoff_time)
        if (difference_minutes > flight_duration_in_minutes):
            breakfast_time = flight_duration_in_minutes / 60
            return {"breakfast": breakfast_time, "lunch": lunch_time, "dinner": dinner_time}
        else:
            breakfast_time = (time_to_minutes(breakfast_end) - time_to_minutes(takeoff_time)) / 60
            flight_duration_in_minutes -= difference_minutes
            if (flight_duration_in_minutes < time_to_minutes(lunch_end) - time_to_minutes(lunch_start)):
                lunch_time = flight_duration_in_minutes / 60
                return {"breakfast": breakfast_time, "lunch": lunch_time, "dinner": dinner_time}
            else:
                lunch_time = (time_to_minutes(lunch_end) - time_to_minutes(lunch_start)) / 60
                flight_duration_in_minutes -= (time_to_minutes(lunch_end) - time_to_minutes(lunch_start))
                dinner_time = flight_duration_in_minutes / 60
                return {"breakfast": breakfast_time, "lunch": lunch_time, "dinner": dinner_time}
    elif (current_time_interval == "lunch"):
        difference_minutes = time_to_minutes(lunch_end) - time_to_minutes(takeoff_time)
        if (difference_minutes > flight_duration_in_minutes):
            lunch_time = flight_duration_in_minutes / 60
            return {"breakfast": breakfast_time, "lunch": lunch_time, "dinner": dinner_time}
        else:
            lunch_time = (time_to_minutes(lunch_end) - time_to_minutes(takeoff_time)) / 60
            flight_duration_in_minutes -= difference_minutes
            if (flight_duration_in_minutes < time_to_minutes(dinner_end) - time_to_minutes(dinner_start) + (24*60)):
                dinner_time = flight_duration_in_minutes / 60
                return {"breakfast": breakfast_time, "lunch": lunch_time, "dinner": dinner_time}
            else:
                dinner_time = (time_to_minutes(dinner_end) - time_to_minutes(dinner_start) + (24*60)) / 60
                flight_duration_in_minutes -= (time_to_minutes(dinner_end) - time_to_minutes(dinner_start) + (24*60))
                breakfast_time = flight_duration_in_minutes / 60
                return {"breakfast": breakfast_time, "lunch": lunch_time, "dinner": dinner_time}
    elif (current_time_interval == "dinner"):
        if (time_to_minutes(takeoff_time) >= 16*60):
            difference_minutes = time_to_minutes(dinner_end) - time_to_minutes(takeoff_time) + (24*60)
        else:
            difference_minutes = time_to_minutes(dinner_end) - time_to_minutes(takeoff_time)
        if (difference_minutes >= flight_duration_in_minutes):
            dinner_time = flight_duration_in_minutes / 60
            return {"breakfast": breakfast_time, "lunch": lunch_time, "dinner": dinner_time}
        else:
            dinner_time = difference_minutes / 60
            flight_duration_in_minutes -= difference_minutes
            if (flight_duration_in_minutes < time_to_minutes(breakfast_end) - time_to_minutes(breakfast_start)):
                breakfast_time = flight_duration_in_minutes / 60
                return {"breakfast": breakfast_time, "lunch": lunch_time, "dinner": dinner_time}
            else:
                breakfast_time = (time_to_minutes(breakfast_end) - time_to_minutes(breakfast_start)) / 60
                flight_duration_in_minutes -= (time_to_minutes(breakfast_end) - time_to_minutes(breakfast_start))
                if(flight_duration_in_minutes / 60 > 6):
                   lunch_time = 6.0
                   dinner_time += (flight_duration_in_minutes / 60) - 6
                else:
                    lunch_time = flight_duration_in_minutes / 60
                return {"breakfast": breakfast_time, "lunch": lunch_time, "dinner": dinner_time}
        

def calculate_eating_amount(flight_duration):
    if(flight_duration >= 1 and flight_duration <= 3):
        return {'amount': 1, 'type': 'cold'}
    elif(flight_duration > 3 and flight_duration <= 6):
        return {'amount': 1, 'type': 'hot'}
    elif(flight_duration > 6):
        return {'amount': 2, 'type': 'hot'}
    else:
        return None
  

def get_menu_array(flight_duration, takeoff_time):
    eating_amount_info = calculate_eating_amount(flight_duration)
    time_amount_info = recognize_time_amount(flight_duration, takeoff_time)

    menu_array = []

    if(eating_amount_info['amount'] == 1):
        if(time_amount_info['dinner'] == time_amount_info['breakfast']):
            menu_array.append('dinner')
        else:
            menu_array.append(max(time_amount_info, key=time_amount_info.get))
        return menu_array
    elif(eating_amount_info['amount'] == 2):
        sorted_time_amount_info = dict(sorted(time_amount_info.items(), key=lambda x: x[1], reverse=True))
        menu_array.append(list(sorted_time_amount_info.keys())[0])
        menu_array.append(list(sorted_time_amount_info.keys())[1])
        return menu_array
    
def convert_time_to_float(date_time_string):
  # Преобразование строки в объект datetime

  # Получение часов и минут
  hours = date_time_string.hour
  minutes = date_time_string.minute

  # Преобразование часов и минут в общее количество минут
  total_minutes = hours * 60 + minutes

  # Преобразование общего количества минут в часы с плавающей точкой
  float_time = total_minutes / 60

  return float_time
    
def get_flights(limit=10):
    params = {
        'access_key': os.environ['FLIGHT_RADAR_KEY'],
        'airline_icao' :'AFL'
    }

    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

    api_response = api_result.json()

    flights = []
    for flight in api_response['data'][:limit]:
            current_flight = {}
            departure_time_str = flight['departure']['scheduled']
            arrival_time_str = flight['arrival']['scheduled']

            departure_time = datetime.fromisoformat(departure_time_str[:-6]).replace(tzinfo=pytz.utc)  
            arrival_time = datetime.fromisoformat(arrival_time_str[:-6]).replace(tzinfo=pytz.utc)  
            takeoff_date = departure_time.date()

            duration_hours = round((arrival_time - departure_time).total_seconds() / 3600, 2)
            departure_time_float = round(convert_time_to_float(departure_time), 2)

            current_flight['airline_name'] = "Аэрофлот"
            current_flight['takeoff_date'] = takeoff_date
            current_flight['takeoff_time'] = departure_time_float
            current_flight['flight_duration'] = duration_hours

            flights.append(current_flight)
    return flights