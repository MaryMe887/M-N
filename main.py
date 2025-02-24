import os
import sys
import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
min_spn, max_spn = 0.0005, 50
cord_x, cord_y = input('Введите нужные координаты (две переменные через пробел): ').split()
spn = float(input('Введите масштаб (одна десятичная дробь): '))
min_lat, max_lat = -85.0, 85.0
min_lon, max_lon = -180.0, 180.0


def load_map():
    """Готовим запрос"""
    global spn, cord_y, cord_x
    spn = max(min_spn, min(max_spn, spn))
    cord_x = max(min_lon, min(max_lon, float(cord_x)))
    cord_y = max(min_lat, min(max_lat, float(cord_y)))
    print(f"Координаты: {cord_x}, {cord_y} | Масштаб: {spn}")

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
            if event.key == pygame.K_PAGEUP:
                spn /= 1.5
                load_map()
            elif event.key == pygame.K_PAGEDOWN:
                spn *= 1.5
                load_map()
            elif event.key == pygame.K_UP:
                cord_y = min(max_lat, float(cord_y) + spn)
                load_map()
            elif event.key == pygame.K_DOWN:
                cord_y = max(min_lat, float(cord_y) - spn)
                load_map()
            elif event.key == pygame.K_LEFT:
                cord_x = max(min_lon, float(cord_x) - spn)
                load_map()
            elif event.key == pygame.K_RIGHT:
                cord_x = min(max_lon, float(cord_x) + spn)
                load_map()

pygame.quit()

if os.path.exists("map.png"):
    os.remove("map.png")