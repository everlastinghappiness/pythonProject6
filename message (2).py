import pygame

import sys
#import os

pygame.init()
# Определение размеров окна
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Гонки")


def terminate():
    pygame.quit()
    sys.exit()


x = 50
speed = 10

score = 0


class Car(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.image.load("car.png")
        self.car_image = pygame.image.load("car.png")

        self.rect = self.car_image.get_rect()
        self.rect.x = 10
        self.rect.y = 200

        self.player_x = WINDOW_WIDTH / 2 - self.rect.width / 2
        self.player_y = WINDOW_HEIGHT - self.rect.height - 50

    def update(self, player_x):
        self.rect.left += speed


# Создание шрифта
font = pygame.font.Font(None, 36)


def main():
    # Отрисовка объектов на экране
    screen.fill('white')

    all_sprites = pygame.sprite.Group()

    car = Car(all_sprites)

    score_text = font.render("Score: " + str(score), True, 'black')
    score_exampl = font.render('2' + str(score), True, 'black')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT]:
                car.update(x)
        screen.fill('white')
        all_sprites.draw(screen)
        screen.blit(score_text, (10, 10))
        screen.blit(score_exampl, (300, 0))
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()




    # Обновление счета игрока
    #if enemy_y > WINDOW_HEIGHT:
       # score += 1
       # enemy_x = random.randint(0, WINDOW_WIDTH - car_width)
        #enemy_y = -car_height
