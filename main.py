import os
import sys
import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1'
min_spn, max_spn = 0.0005, 50
# cord_x, cord_y = input('Введите нужные координаты (две переменные через пробел): ').split()
cord_x, cord_y = None, None
spn = 0.002
min_x, max_x = -85.0, 85.0
min_y, max_y = -180.0, 180.0


def load_map():
    """Готовим запрос"""
    global spn, cord_x, cord_y
    spn = max(min_spn, min(max_spn, spn))
    cord_x = max(min_y, min(max_y, float(cord_x)))
    cord_y = max(min_x, min(max_x, float(cord_y)))
    print(f"Координаты: {cord_x}, {cord_y} | Масштаб: {spn}")

    params = {
        'll': f'{cord_x},{cord_y}',
        'spn': f'{spn},{spn}',
        'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
    }
    response = requests.get(server_address, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open("map.png", "wb") as file:
        file.write(response.content)
    map_image = pygame.image.load("map.png")
    screen.blit(map_image, (0, 0))


def geocode(address):
    geocode_server = 'https://geocode-maps.yandex.ru/1.x/'
    params = {
        'apikey': '8013b162-6b42-4997-9691-77b7074026e0',
        'geocode': address,
        'format': 'json'
    }
    response = requests.get(geocode_server, params=params)
    json_response = response.json()
    try:
        cords = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"][
            "pos"]
        x, y = map(float, cords.split())
        return x, y
    except IndexError:
        print("Объект не найден")
        return None, None


# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
pygame.display.set_caption("Карта")

font = pygame.font.Font(None, 30)
input_box = pygame.Rect(200, 225, 140, 32)
color_inactive = pygame.Color('red')
color_active = pygame.Color('green')
color = color_inactive
active = False
text = ''
running = True
while running:
    screen.fill((0, 0, 0))
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(font.render('Введите место, которое ищите(*´▽`*)', True, color), (170, 200))
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 3)
    if os.path.exists("map.png"):
        map_image = pygame.image.load("map.png")
        screen.blit(map_image, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
            color = color_active if active else color_inactive
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    x, y = geocode(text)
                    if x and y:
                        cord_x, cord_y = x, y
                        load_map()
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.key == pygame.K_PAGEUP:
                spn /= 1.5
                load_map()
            elif event.key == pygame.K_PAGEDOWN:
                spn *= 1.5
                load_map()
            elif event.key == pygame.K_UP:
                cord_y = min(max_x, float(cord_y) + spn)
                load_map()
            elif event.key == pygame.K_DOWN:
                cord_y = max(min_x, float(cord_y) - spn)
                load_map()
            elif event.key == pygame.K_LEFT:
                cord_x = max(min_y, float(cord_x) - spn)
                load_map()
            elif event.key == pygame.K_RIGHT:
                cord_x = min(max_y, float(cord_x) + spn)
                load_map()
    pygame.display.flip()
pygame.quit()

if os.path.exists("map.png"):
    os.remove("map.png")
