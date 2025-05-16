# Ethan Lawrence 
# Feb 12 2025
# Pygame template ver 2

import pygame
import sys

# Game Config
# Window dimentions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TITLE = 'My Pygame Project'
FPS = 60
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# Font
FONT = 'arial'
FONT_SIZE = {
    'score' : 36,
    'start' : 36,
    'instructions' : 24,
    'game over' : 48,
    'restart' : 26
}

# Player
PLAYER_STATS = {
    'width' : 90,
    'height' : 20,
    'start' : [WINDOW_WIDTH/2, WINDOW_HEIGHT-40],
    'speed' : 20
}
# Ball
BALL_STATS = {
    'radius' : 10,
    'start' : [WINDOW_WIDTH//2, WINDOW_HEIGHT//2],
    'init speed' : [10, -14]
}
# Brick
BRICK_STATS = {
    'width' : 100,
    'height' : 30,
    'padding' : [50, 20],
    'layout' : [6, 8]
}
# Input settings
INPUT_LEFT = pygame.K_a
INPUT_RIGHT = pygame.K_d
# Classes
class Player(pygame.sprite.Sprite):
    '''The Paddle'''
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((PLAYER_STATS['width'], PLAYER_STATS['height']))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # Pos
        self.x = PLAYER_STATS['start'][0]
        self.y = PLAYER_STATS['start'][1]
        self.rect.center = (self.x, self.y)
    
    def update(self):
        print('player')
        '''moves based on input'''
        keys = pygame.key.get_pressed()
        if keys[INPUT_RIGHT] and self.x <= WINDOW_WIDTH-PLAYER_STATS['width']//2 and self.y > WINDOW_HEIGHT - 100:
            self.x += PLAYER_STATS['speed']
        if keys[INPUT_LEFT] and self.x >= PLAYER_STATS['width']//2 and self.y > WINDOW_HEIGHT - 100:
            self.x -= PLAYER_STATS['speed']
        self.rect.center = (self.x, self.y)
class Ball(pygame.sprite.Sprite):
    '''The ball'''
    def __init__(self):
        super().__init__()
        ball_image = pygame.Surface((BALL_STATS['radius']*2, BALL_STATS['radius']*2,))
        pygame.draw.circle(ball_image, WHITE, (BALL_STATS['radius'], BALL_STATS['radius']), BALL_STATS['radius'])
        
        self.image = ball_image
        self.rect = self.image.get_rect()

        # pos
        self.x = BALL_STATS['start'][0]
        self.y = BALL_STATS['start'][1]
        self.x_vel = BALL_STATS['init speed'][0]
        self.y_vel = BALL_STATS['init speed'][1]
        self.rect.center = (self.x, self.y)
    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

        if self.x <= BALL_STATS['radius'] or self.x > WINDOW_WIDTH - BALL_STATS['radius']:
            self.x_vel *= -1
        if self.y <= BALL_STATS['radius']:
            self.y_vel *= -1
        
        self.rect.center = (self.x, self.y)
class Brick(pygame.sprite.Sprite):
    '''A single brick'''
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BRICK_STATS['width'], BRICK_STATS['height']))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Game:
    '''Game logic'''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT)

    def new(self):
        '''starts a new game'''
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group() # Groups to hold the sprites
        self.bricks = pygame.sprite.Group()

        self.score = 0
        self.ball = Ball()
        self.player = Player(WHITE)

        self.all_sprites.add(self.ball)
        self.all_sprites.add(self.player)
        self.players.add(self.player)

        # Place Bricks
        for col in range(BRICK_STATS['layout'][0]):
            for row in range(BRICK_STATS['layout'][1]):
                brick_x = BRICK_STATS['padding'][0] + col * (BRICK_STATS['width'] + BRICK_STATS['padding'][0])
                brick_y = BRICK_STATS['padding'][1] + row * (BRICK_STATS['height'] + BRICK_STATS['padding'][1])

                brick = Brick(brick_x, brick_y, BLUE)
                self.all_sprites.add(brick)
                self.bricks.add(brick)
        self.main()
    def main(self):
        '''Game Loop'''
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def events(self):
        '''Checks if user quits game'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
    def update(self):
        '''updates game internal positions and colitions'''
        self.all_sprites.update()
        # Paddle collision
        hit_paddle = pygame.sprite.spritecollide(self.ball, self.players, False)
        if hit_paddle and self.ball.y_vel > 0:
            self.ball.y = self.player.rect.top - BALL_STATS['radius'] # Keep ball outside of paddle 
            self.ball.y_vel *= -1
        # Brick collision
        hit_brick = pygame.sprite.spritecollide(self.ball, self.bricks, True)
        if hit_brick:
            self.ball.y_vel *= -1
            self.score += len(hit_brick)
        
        # Game over check
        if self.ball.rect.top > WINDOW_HEIGHT:
            self.playing = False
        if not self.bricks:
            self.playing = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(f'Score:{self.score}', FONT_SIZE['score'], RED, WINDOW_WIDTH*3/4, WINDOW_HEIGHT-50)
        pygame.display.flip()

    def show_start(self):
        print('show start')
        self.screen.fill(BLACK)
        self.draw_text('Breakout Game!', FONT_SIZE['start'], RED, WINDOW_WIDTH/2, WINDOW_HEIGHT/3)
        self.draw_text('Press any key to begin...', FONT_SIZE['instructions'], WHITE, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        pygame.display.flip()
        self.wait_for_key()

    def show_game_over(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', FONT_SIZE['game over'], RED, WINDOW_WIDTH/2, WINDOW_HEIGHT/4)
        self.draw_text(f'Score: {self.score}', FONT_SIZE['score'], RED, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.draw_text('Press any key to play again...', FONT_SIZE['restart'], WHITE, WINDOW_WIDTH/2, WINDOW_HEIGHT*3/4)
        pygame.display.flip()
        self.wait_for_key()
    def wait_for_key(self):
        print('wait for key')
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False
    def draw_text(self, text, size, color, x, y):
        print('text')
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

game = Game()
game.show_start()
while game.running:
    game.new()
    game.show_game_over()
pygame.quit()