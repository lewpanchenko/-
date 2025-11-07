import pygame
import random
import sys

from main import background

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 500, 600
BALL_RADIUS = 20
SPIKE_WIDTH = 40
SPIKE_HEIGHT = 20
SPIKE_SPEED = 3
SPAWN_RATE = 60  # кадры между появлением шипов
BALL_SPEED = 5

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шарик и шипы")
clock = pygame.time.Clock()

background_image = pygame.image.load("background.png")
ball_image = pygame.image.load("ball.jpg")

class player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.radius = BALL_RADIUS
        self.speed = BALL_SPEED
        self.alive = True

    def move(self, direction):
        if direction == "left" and self.x - self.radius > 0:
            self.x -= self.speed
        if direction == "right" and self.x + self.radius < WIDTH:
            self.x += self.speed
        if direction == "up" and self.y - self.radius > 0:
            self.y -= self.speed
        if direction == "down" and self.y + self.radius < HEIGHT:
            self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.radius)

    def check_collision(self, spike):
        # Простое определение столкновения
        distance_x = abs(self.x - spike.x)
        distance_y = abs(self.y - spike.y)

        if distance_x < (self.radius + spike.width // 2) and distance_y < (self.radius + spike.height // 2):
            return True
        return False


class Spike:
    def __init__(self):
        self.width = SPIKE_WIDTH
        self.height = SPIKE_HEIGHT
        self.x = random.randint(self.width, WIDTH - self.width)
        self.y = -self.height
        self.speed = SPIKE_SPEED

    def update(self):
        self.y += self.speed

    def draw(self):
        # Рисуем треугольник (шип)
        points = [
            (self.x, self.y + self.height),  # нижняя точка
            (self.x - self.width // 2, self.y),  # левая верхняя
            (self.x + self.width // 2, self.y)  # правая верхняя
        ]
        pygame.draw.polygon(screen, RED, points)

    def is_off_screen(self):
        return self.y > HEIGHT


def show_game_over():
    font = pygame.font.SysFont(None, 74)
    text = font.render("ИГРА ОКОНЧЕНА", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    font_small = pygame.font.SysFont(None, 36)
    restart_text = font_small.render("Нажмите R для перезапуска", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def main():
    ball = Ball()
    spikes = []
    frame_count = 0
    score = 0

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if ball.alive:
            # Управление шариком
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                ball.move("left")
            if keys[pygame.K_RIGHT]:
                ball.move("right")
            if keys[pygame.K_UP]:
                ball.move("up")
            if keys[pygame.K_DOWN]:
                ball.move("down")

            # Создание новых шипов
            frame_count += 1
            if frame_count >= SPAWN_RATE:
                spikes.append(Spike())
                frame_count = 0
                score += 1

            # Обновление шипов
            for spike in spikes[:]:
                spike.update()

                # Проверка столкновений
                if ball.check_collision(spike):
                    ball.alive = False

                # Удаление шипов за экраном
                if spike.is_off_screen():
                    spikes.remove(spike)

        # Отрисовка
        screen.blit(background_image, (0,0))

        # Отрисовка шарика
        ball.draw()

        # Отрисовка шипов
        for spike in spikes:
            spike.draw()

        # Отрисовка счета
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # Если шарик мертв, показываем экран окончания игры
        if not ball.alive:
            show_game_over()
            # Перезапуск игры
            ball = Ball()
            spikes = []
            frame_count = 0
            score = 0

        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()