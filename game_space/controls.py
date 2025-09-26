import time
import sys

import pygame
from pygame.sprite import Group

from bullet import Bullet
from gun import Gun
from ino import Ino
from scores import Scores
from stats import Stats


def events(screen: pygame.Surface, gun: Gun, bullets: Group, stats: Stats) -> None:
    """Обработка событий"""
    for event in pygame.event.get(): # обработка событий
        if event.type == pygame.QUIT: # если нажали крестик (выход)
            check_record(stats=stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # вправо
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                gun.mright = True
            # влево
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                gun.mleft = True
            elif event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                new_bullet = Bullet(screen=screen, gun=gun)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                gun.mright = False
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                gun.mleft = False


def update(
    screen: pygame.Surface,
    bg_color: tuple[int],
    gun: Gun,
    bullets: Group,
    inos: Group,
    scores: Scores,
) -> None:
    """Обновление экрана"""
    screen.fill(bg_color)
    scores.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    gun.output()
    inos.draw(screen)
    pygame.display.flip()


def update_bullets(bullets: Group, inos: Group, scores: Scores) -> None:
    """Обновлять позиции пуль"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            # print(f"{len(bullets)=}")

    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)
    if collisions:
        for killed_inos in collisions.values():
            scores.stats.score += 10 * len(killed_inos)
        scores.image_score()


def update_inos(
    inos: Group,
    gun: Gun,
    stats: Stats,
    screen: pygame.Surface,
    bullets: Group,
    scores: Scores,
) -> None:
    """Обновляет позиции пришельцев"""
    if len(inos) == 0:
        bullets.empty()
        stats.new_level()
        create_army(screen=screen, inos=inos, stats=stats)

    inos.update()
    if pygame.sprite.spritecollideany(gun, inos):
        gun_kill(
            stats=stats,
            screen=screen,
            gun=gun,
            inos=inos,
            bullets=bullets,
            scores=scores
        )
    
    inos_check(
        stats=stats,
        screen=screen,
        gun=gun,
        inos=inos,
        bullets=bullets,
        scores=scores,
    )


def inos_check(
    inos: Group,
    gun: Gun,
    stats: Stats,
    screen: pygame.Surface,
    bullets: Group,
    scores: Scores,
) -> None:
    """Проверка добралась ли армия до края"""
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            gun_kill(
                stats=stats,
                screen=screen,
                gun=gun,
                inos=inos,
                bullets=bullets,
                scores=scores,
            )
            break


def gun_kill(
    stats: Stats,
    screen: pygame.Surface,
    gun: Gun,
    inos: Group,
    bullets: Group,
    scores: Scores,
):
    """Столкновение пушки и армии"""
    stats.guns_left -= 1
    print(f"{stats.guns_left=}")
    scores.image_guns_left()
    inos.empty()
    bullets.empty()
    create_army(screen=screen, inos=inos, stats=stats)
    gun.create_gun()
    time.sleep(1)


def create_army(screen: pygame.Surface, inos: Group, stats: Stats):
    """Создает армию пришельцев"""
    ino = Ino(screen=screen)
    ino_width = ino.rect.width
    number_ino_x = int((700 - 2 * ino_width) / ino_width)

    ino_height = ino.rect.height
    # max_number_ino_y = int((screen.get_height() / 1.1 - 2 * ino_height) / ino_height)
    max_number_ino_y = 3 # для отладки

    if stats.level > max_number_ino_y:
        stats.is_win = True
        finish_game(screen=screen, stats=stats)
    elif stats.guns_left <= 0:
        finish_game(screen=screen, stats=stats)
    else:
        for row_number in range(stats.level):
        # for row_number in range(max_number_ino_y + 2): # для отладки
            for ino_number in range(number_ino_x):
                ino = Ino(screen=screen)
                ino.x = ino_width + ino_width * ino_number
                ino.y = ino_height + ino_height * row_number
                ino.rect.x = ino.x
                ino.rect.y = ino.y
                inos.add(ino)


def finish_game(screen: pygame.Surface, stats: Stats) -> None:
    """Закончить игру"""
    if stats.is_win:
        image = pygame.image.load("images/winner.png")
    else:
        image = pygame.image.load("images/loser.png")

    check_record(stats=stats)

    rect = image.get_rect()
    screen_rect = screen.get_rect()
    rect.centerx = screen_rect.centerx
    rect.centery = screen_rect.centery
    screen.blit(image, rect)
    pygame.display.flip()

    time.sleep(5)
    sys.exit()


def check_record(stats: Stats):
    """Проверка новых рекордов"""
    if stats.score > stats.record:
        with open("records.txt", "w") as file:
            file.write(str(stats.score))
