class FoodIndex:
    def __init__(self):
        self.index = 0  # Инициализируем индекс еды
        self.weight_flight_duration = 0.2  # Вес длительности полета
        self.weight_class_of_service = 0.3  # Вес класса обслуживания
        self.weight_passengers = 0.1  # Вес количества пассажиров

    def set_weights(self, weight_flight_duration, weight_class_of_service, weight_passengers):
        # Устанавливаем веса параметров
        self.weight_flight_duration = weight_flight_duration
        self.weight_class_of_service = weight_class_of_service
        self.weight_passengers = weight_passengers

    def calculate_index(self, flight_duration, class_of_service_data):
        # Рассчитываем индекс еды на основе характеристик рейса
        increment_value = 0
        decrement_value = 0
        
        # Учитываем длительность полета
        flight_duration = int(flight_duration)
        if flight_duration > 300:
            increment_value += 5 * self.weight_flight_duration
            if flight_duration > 600:
                increment_value += 10 * self.weight_flight_duration
        else:
            decrement_value += 5 * self.weight_flight_duration
        
        # Учитываем классы обслуживания и их количество
        for class_data in class_of_service_data:
            class_type = class_data["type"]
            passengers = class_data["amount"]
            
            if class_type == "business":
                increment_value += 10 * self.weight_class_of_service * passengers / 100  # Учитываем количество пассажиров
            elif class_type == "economy":
                # Учитываем количество пассажиров в эконом-классе с меньшим весом
                increment_value += 5 * self.weight_class_of_service * passengers / 100
        
        # Применяем инкремент и декремент к индексу
        self.index += increment_value
        self.index -= decrement_value
        
        # Ограничиваем индекс так, чтобы он не мог стать отрицательным
        if self.index < 0:
            self.index = 0

    def get_index(self):
        return self.index
