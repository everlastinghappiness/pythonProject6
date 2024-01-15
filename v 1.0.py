import os
import pygame
import sys
import random


pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Гонки")


def terminate():
    pygame.quit()
    sys.exit()


car_width = car_height = 50
x = 50
FPS = 50
score = 0
font_main = pygame.font.SysFont('Arial', 50)
objects = []
font_game = pygame.font.Font(None, 36)


def start_screen(screen):
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('fon.jpg'),
                                 (screen.get_width(), screen.get_height()))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        for object in objects:
            object.process()
        pygame.display.flip()
        clock.tick(FPS)


def second_screen(screen):
    intro_text = ["Правила игры",
                  "В верху экрана будут появляться арифметические примеры.",
                  "Ваша задача: устно решить пример и заехать машинкой в туннель,",
                  "обозначенный правильным ответом.",
                  "Управление машинкой осуществляется нажатием кнопок: 'вверх', 'вниз', 'вправо'.",
                  "Удачи!"]
    clock = pygame.time.Clock()

    fon = pygame.transform.scale(load_image('fon.jpg'),
                                 (screen.get_width(), screen.get_height()))

    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()
car_group = pygame.sprite.Group()
tunnel_group = pygame.sprite.Group()
road_group = pygame.sprite.Group()


class Button:
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#cfcfcf',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font_main.render(buttonText, True, (0, 0, 0))
        self.alreadyPressed = False
        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2])
        screen.blit(self.buttonSurface, self.buttonRect)


customButton = Button(600, 290, 170, 50, 'start')


class Math:
    def __init__(self):
        self.a = random.randrange(0, 11)
        self.b = random.randrange(0, 11)
        self.i = random.randrange(0, 2)
        self.j = random.randrange(0, 2)
        self.answer = 0
        self.incorrect1 = 0
        self.incorrect2 = 0
        self.example = ''

    def correct_answer(self):
        if self.i == 0:
            self.answer = self.a * self.b
            self.example = str(self.a) + ' * ' + str(self.b)
        else:
            if self.a != 0 and self.b != 0:
                if self.j == 0:
                    self.answer = self.a * self.b // self.a
                    self.example = str(self.a * self.b) + ' % ' + str(self.a)
                else:
                    self.answer = self.a * self.b // self.b
                    self.example = str(self.a * self.b) + ' % ' + str(self.b)
            else:
                self.answer = self.a * self.b
                self.example = str(self.a) + ' * ' + str(self.b)
        return self.answer, self.example

    def incorrect_answer(self):
        if self.answer != 0:
            self.incorrect1 = random.randrange(self.answer - 5, self.answer)
            self.incorrect2 = random.randrange(self.answer + 1, self.answer + 6)
        else:
            self.incorrect1 = random.randrange(self.answer + 1, self.answer + 5)
            self.incorrect2 = random.randrange(self.answer + 5, self.answer + 9)
        return self.incorrect1, self.incorrect2


#answer, example = Math.correct_answer()
#incor1, incor2 = Math.incorrect_answer()


tunnel_image = load_image('tunnel.png')
car_image = load_image('car.png')
road_image = load_image('road.png')


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(car_group, all_sprites)
        self.image = car_image
        self.car_image = car_image

        self.rect = self.car_image.get_rect()
        self.rect.x = 10
        self.rect.y = 200

    def update(self, x, y):
        self.rect.left += x
        self.rect.top += y


class Tunnel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(tunnel_group, all_sprites)
        self.image = tunnel_image
        self.tunnel_image = tunnel_image

        self.rect = self.tunnel_image.get_rect()
        self.rect.x = 600
        self.rect.y = 100

        #self.mask = pygame.mask.from_surface(self.image)
        #self.rect.left = self.image.get_width()
        #self.mask = pygame.mask.from_surface(self.image)


def main():
    start_screen(screen)
    second_screen(screen)
    screen.fill('white')

    car = Car()
    score_text = font_game.render("Score: " + str(score), True, 'black')
    score_exampl = font_game.render(str(), True, 'black')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT]:
                car.update(car_width, 0)
            elif key[pygame.K_DOWN]:
                car.update(0, car_height)
            elif key[pygame.K_UP]:
                car.update(0, -car_height)
        screen.fill('white')
        all_sprites.draw(screen)
        tunnel_group.draw(screen)
        car_group.draw(screen)

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
