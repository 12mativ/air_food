from datetime import datetime, time

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
        return{'amount': 2, 'type': 'hot'}
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


print(get_menu_array(4, time(8, 0)))


# 1) difference1 = max_завтрак_time - takeoff_time (= 3)
# 2) if (difference1 > flight_duration) {
#  время_полета_завтрак = flight_duration
#  return
# } else {
#  flight_duration -= difference1 (flight_duration = 9)

#  if (flight_duration > обед_time) {
#    flight_duration -= обед_time (flight_duration = 3)
#  } else {
#    время_полета_обед = flight_duration
#    return
#  }
# }
# 4) if (flight_duration < ужин_time) {
#  время_полета_ужин = flight_duration
#  return
# } else {
#  flight_duration -= ужин_time
#  время_полета_ужин = flight_duration
#  return
# }    