class Stats():
    """Отслеживание статистики"""

    def __init__(self):
        """Инициализирует статистику"""
        self.reset_stats()
        self.run_game = True
        with open("records.txt", "r") as file:
            self.record = int(file.readline())

        self.is_win = False


    def reset_stats(self):
        """Статистика, изменяющаяся во время игры"""
        self.guns_left = 3
        self.score = 0
        
        self.level = 1

    def new_level(self):
        """Переход на новый уровень"""
        self.level += 1
