import os
import sys
import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
min_spn, max_spn = 0.0005, 50
cord_x, cord_y = input('Введите нужные координаты (две переменные через пробел): ').split()
spn = float(input('Введите масштаб (одна десятичная дробь): '))


def load_map():
    """Готовим запрос"""
    global spn
    spn = max(min_spn, min(max_spn, spn))
    print(f"Текущий масштаб: {spn}")

    params = {
        'll': f'{cord_x},{cord_y}',
        'spn': f'{spn},{spn}',
        'apikey': api_key
    }
    response = requests.get(server_address, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open("map.png", "wb") as file:
        file.write(response.content)

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
pygame.display.set_caption("Карта")
load_map()
running = True
while running:
    map_image = pygame.image.load("map.png")
    screen.blit(map_image, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                spn /= 1.5
                print(spn)
                load_map()
            elif event.key == pygame.K_DOWN:
                spn *= 1.5
                load_map()

pygame.quit()

if os.path.exists("map.png"):
    os.remove("map.png")
