import pygame

from stats import Stats


class Scores():
    """Вывод игровой статистики"""

    def __init__(self, screen: pygame.Surface, stats: Stats):
        """Инициализируем подсчет очков"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = (139, 195, 74)
        self.font = pygame.font.SysFont(None, 36)
        self.image_score()
        self.image_record()
        self.image_guns_left()


    def image_score(self):
        """Преобразовывает текст счета в графическое изображение"""
        self.score_img = self.font.render(f"СЧЁТ: {self.stats.score}", True, self.text_color, (0, 0, 0))
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 40
        self.score_rect.top = 20


    def image_record(self):
        """Преобразует рекорд в графическое изображение"""
        self.record_img = self.font.render(f"РЕКОРД: {self.stats.record}", True, self.text_color, (0, 0, 0))
        self.record_rect = self.record_img.get_rect()
        self.record_rect.centerx = self.screen_rect.centerx
        self.record_rect.top = 20


    def image_guns_left(self):
        """Преобразует кол-во жизней в графическое изображение"""
        self.guns_left_img = self.font.render(f"ЖИЗНЕЙ: {self.stats.guns_left}", True, self.text_color, (0, 0, 0))
        self.guns_left_rect = self.guns_left_img.get_rect()
        self.guns_left_rect.left = self.screen_rect.left + 40
        self.guns_left_rect.top = 20


    def show_score(self):
        """Вывод счета на экран"""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.record_img, self.record_rect)
        self.screen.blit(self.guns_left_img, self.guns_left_rect)
