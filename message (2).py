import pygame
import random


def ok():
    pass


# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Определение размеров окна
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

# Создание окна
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Гонки")

# Загрузка изображений
car_image = pygame.image.load("car.png")
car_width = car_image.get_width()
car_height = car_image.get_height()

# Определение скорости и направления движения машин
player_speed = 0
enemy_speed = 5
enemy_directions = [-1, 0, 1]

# Определение начальных позиций машин
player_x = WINDOW_WIDTH / 2 - car_width / 2
player_y = WINDOW_HEIGHT - car_height - 50
enemy_x = random.randint(0, WINDOW_WIDTH - car_width)
enemy_y = -car_height

# Определение счета игрока
score = 0

# Создание шрифта
font = pygame.font.Font(None, 36)

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed = -5
            elif event.key == pygame.K_RIGHT:
                player_speed = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_speed = 0

    # Обновление позиции машин
    player_x += player_speed
    enemy_x += enemy_directions[random.randint(0, 2)] * enemy_speed

    # Проверка столкновения машин
    if enemy_y + car_height > player_y and enemy_y < player_y + car_height:
        if enemy_x + car_width > player_x and enemy_x < player_x + car_width:
            running = False

    # Обновление счета игрока
    if enemy_y > WINDOW_HEIGHT:
        score += 1
        enemy_x = random.randint(0, WINDOW_WIDTH - car_width)
        enemy_y = -car_height

    # Отрисовка объектов на экране
    window.fill(WHITE)
    window.blit(car_image, (player_x, player_y))
    window.blit(car_image, (enemy_x, enemy_y))
    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.update()

# Закрытие Pygame
pygame.quit()
