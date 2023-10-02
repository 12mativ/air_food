class FoodIndex:
    def __init__(self):
        self.index = 0  # Инициализируем индекс еды

    def calculate_index(self, passengers, flight_duration, class_of_service):
        # Рассчитываем индекс еды на основе характеристик рейса
        increment_value = 0
        decrement_value = 0
        
        # Учитываем длительность полета и количество пассажиров
        flight_duration = int(flight_duration)
        if flight_duration > 300:
            increment_value += 5
            if flight_duration > 600:
                increment_value += 10
        else:
            decrement_value += 5
        
        # Учитываем класс обслуживания
        if class_of_service == "business":
            increment_value += 10
        elif class_of_service == "economy":
            decrement_value += 5
        
        # Применяем инкремент и декремент к индексу
        self.index += increment_value
        self.index -= decrement_value
        
        # Ограничиваем индекс так, чтобы он не мог стать отрицательным
        if self.index < 0:
            self.index = 0

    def get_index(self):
        return self.index
