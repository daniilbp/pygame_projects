import pygame
from pygame.sprite import Group

import controls

from gun import Gun
from scores import Scores
from stats import Stats


def run():
    pygame.init() # инициализация / создание самой игры
    screen = pygame.display.set_mode((700, 800)) # создаем экран
    pygame.display.set_caption("Космические защитники")
    bg_color = (0, 0, 0) # задаем фоновый цвет
    gun = Gun(screen=screen)
    bullets = Group()
    inos = Group()
    stats = Stats()
    scores = Scores(screen=screen, stats=stats)
    controls.create_army(screen=screen, inos=inos, stats=stats)


    while True: # чтобы ПО не заканчивалось
        controls.events(screen=screen, gun=gun, bullets=bullets, stats=stats)
        gun.update_gun()
        controls.update_bullets(bullets=bullets, inos=inos, scores=scores)
        controls.update_inos(
            inos=inos,
            gun=gun,
            stats=stats,
            screen=screen,
            bullets=bullets,
            scores=scores,
        )
        controls.update(
            screen=screen,
            bg_color=bg_color,
            gun=gun,
            bullets=bullets,
            inos=inos,
            scores=scores,
        )


run()
