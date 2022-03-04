import pygame
import random
import sys
pygame.init()

from button import Button

WINDOW_SIZE = (1100, 550)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Catching Game")

BG_COLOR = "#a8fff3"
BLACK = (0, 0, 0)

bowl_img = pygame.image.load("bowl.png")
bowl_img = pygame.transform.scale(bowl_img, (135, 70))

title_font = pygame.font.SysFont("Berlin Sans FB Demi", 80, "bold")
second_title_font = pygame.font.SysFont("Arial", 50, "bold")


def quit_game():
    pygame.quit()
    sys.exit(0)


class Player:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.livesImg = pygame.image.load("heart.png")
        self.score_font = pygame.font.SysFont("Arial", 30, "bold")

    def display_details(self):
        if self.lives <= 0:
            game_over(self)

        # Score
        window.blit(self.score_font.render(f"SCORE:{self.score}", True, BLACK), (10, 10))

        # Lives
        x = WINDOW_SIZE[0] - self.livesImg.get_width()
        for i in range(self.lives):
            window.blit(self.livesImg, (x, 5))
            x -= 50


class Bowl:
    def __init__(self, surface, img, x, y, speed):
        self.surface = surface
        self.img = img
        self.x = x
        self.y = y
        self.speed = speed

        self.width, self.height = self.img.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.surface.blit(self.img, (self.x, self.y))

        # Code for testing the hitbox
        # pygame.draw.rect(self.surface, (255, 0, 0), self.rect, 3)

    def move_left(self):
        if self.x >= 0:
            self.x -= self.speed
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_right(self):
        if (self.x + self.width) <= WINDOW_SIZE[0]:
            self.x += self.speed
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Ball:
    def __init__(self, surface, color, x, y, radius, speed, balls):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.balls = balls

        self.rect = self.get_rect()

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)

        # Code for testing the hitbox
        # pygame.draw.rect(self.surface, (255, 0, 0), self.rect, 3)

    def fall(self, bowl, player):
        if self.y > WINDOW_SIZE[1]:
            self.balls.remove(self)
            player.lives -= 1
            return

        if self.rect.colliderect(bowl.rect):
            self.balls.remove(self)
            player.score += 5
            return

        self.y += self.speed
        self.rect = self.get_rect()

    def get_rect(self):
        return pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)


def game_over(player):
    menu_button = Button(window, "MENU", "#da24ff", "#640078", 350, 250, 400, 160)

    title_label = title_font.render("GAME OVER", True, BLACK)

    second_title_label = second_title_font.render(f"SCORE:{player.score}", True, BLACK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.rect.collidepoint(event.pos):
                    menu()

        window.fill(BG_COLOR)

        window.blit(title_label, (320, 25))
        window.blit(second_title_label, (420, 115))
        menu_button.draw()

        pygame.display.update()


def main():
    clock = pygame.time.Clock()

    player = Player()
    bowl = Bowl(window, bowl_img, 420, 450, 7)

    # time waited before spawning a new ball
    start = pygame.time.get_ticks()
    wait_time = 0
    ball_speed = 4
    balls = []

    count = 0

    # Stores the player's scores
    scoresList = []

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            bowl.move_right()

        if keys[pygame.K_LEFT]:
            bowl.move_left()

        window.fill(BG_COLOR)
        clock.tick(60)
        player.display_details()

        now = pygame.time.get_ticks()
        if now - start >= wait_time:
            start = pygame.time.get_ticks()

            rand_color = [random.randint(0, 255) for _ in range(3)]
            x = random.randint(20, WINDOW_SIZE[0]-20)
            ball = Ball(window, rand_color, x, -10, 20, ball_speed, balls)
            balls.append(ball)

        bowl.draw()

        for b in balls:
            b.fall(bowl, player)
            b.draw()

        count += 1
        if count == 1:
            wait_time = 2000

        scoresList.append(player.score)

        if player.score > 0 and player.score % 30 == 0:
            if scoresList[-1] != scoresList[-2]:
                ball_speed += 1
                bowl.speed += 0.25
                wait_time -= 100

        pygame.display.update()

    quit_game()


def menu():
    play_button = Button(window, "PLAY", "#29d6ac", BLACK, 350, 250, 400, 160)
    title_label = title_font.render("Ball Catch", True, BLACK)
    second_title_label = second_title_font.render("By Roni", True, BLACK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    main()

        window.fill(BG_COLOR)

        window.blit(title_label, (370, 25))
        window.blit(second_title_label, (450, 115))
        play_button.draw()

        pygame.display.update()



if __name__ == "__main__":
    menu()
