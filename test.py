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
        return
        

print(recognize_time_amount(12, time(7, 0)))
  



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