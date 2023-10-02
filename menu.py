class MenuDatabase:
    def __init__(self):
        # Создаем базу данных с диапазонами индексов и соответствующими меню
        self.menus = [
            {"index_range": (0, 5), "title": "Меню 1", "items": ["Блюдо 1", "Блюдо 2", "Блюдо 3"]},
            {"index_range": (5, 10), "title": "Меню 2", "items": ["Блюдо 4", "Блюдо 5", "Блюдо 6"]},
            {"index_range": (10, 15), "title": "Меню 3", "items": ["Блюдо 7", "Блюдо 8", "Блюдо 9"]},
            # Другие диапазоны и меню
        ]

    def get_menu_by_index(self, index):
        # Ищем меню, соответствующее заданному индексу
        for menu in self.menus:
            index_range = menu["index_range"] 
            if index_range[0] <= index < index_range[1]:
                return menu
        
        # Если индекс не соответствует ни одному диапазону, возвращаем стандартное меню
        return {"title": "Стандартное меню", "items": ["Блюдо 3333", "Блюдо 2", "Блюдо 3"]}
