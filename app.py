import pygame
pygame.init()

# Initialize
GREEN = (52,66,50)
WHITE = (255,255,255)
GRAY = (77,74,73)

WIDTH = 700
HEIGHT = 500
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PyPong')
pygame.mouse.set_visible(0)
FPS = 60

PADDLE_W, PADDLE_H = 10, 100
BALL_RADIUS = 5

SCORE_FONT = pygame.font.SysFont('Cascadia', 20)
WIN_FONT = pygame.font.SysFont('Cascadia', 80)
WIN_SCORE = 10


# Ball Object
class Ball:
    COLOR = WHITE

    def __init__(self, x, y, rad):
        self.x = self.og_x = x
        self.y = self.og_y = y
        self.rad = rad
        self.x_velo = 7
        self.y_velo = self.og_y_velo = 7
    
    def draw(self, wn):
        pygame.draw.circle(wn, self.COLOR, (self.x, self.y), self.rad)

    def move(self):
        self.x += self.x_velo
        self.y += self.y_velo
    
    def reset(self):
        self.x = self.og_x
        self.y = self.og_y
        self.x_velo *= -1
        self.y_velo = self.og_y_velo


# Paddle Object
class Paddle:
    COLOR = WHITE
    VELO = 7

    def __init__(self, x, y, w, h):
        self.x = self.og_x = x
        self.y = self.og_y = y
        self.w = w
        self.h = h

    def draw(self, wn):
        pygame.draw.rect(wn, self.COLOR, (self.x, self.y, self.w, self.h))

    def move(self, up=True):
        if up:
            self.y -= self.VELO
        else:
            self.y += self.VELO
    
    def reset(self):
        self.x = self.og_x
        self.y = self.og_y


# Function to handle ball collision
def collision(ball, l_paddle, r_paddle):
    # Ceiling collisions
    if ball.y + BALL_RADIUS >= HEIGHT or ball.y - BALL_RADIUS <= 0:
        ball.y_velo *= -1

    # Paddle collisions
    if ball.x_velo < 0:
        if ball.y >= l_paddle.y and ball.y <= l_paddle.y + PADDLE_H:
            if ball.x - ball.rad <= l_paddle.x + PADDLE_W:
                ball.x_velo *= -1
    else:
        if ball.y >= r_paddle.y and ball.y < r_paddle.y + PADDLE_H:
            if ball.x + ball.rad >= r_paddle.x:
                ball.x_velo *= -1


# Function to handle player-paddle movement
def paddle_movement(keys, l_paddle, r_paddle):
    #if pressing W key AND as long as paddle will be in y pos >= 0
    if keys[pygame.K_w] and l_paddle.y - l_paddle.VELO >= 0:
        l_paddle.move(up=True)
    if keys[pygame.K_s] and l_paddle.y + PADDLE_H + l_paddle.VELO <= HEIGHT:
        l_paddle.move(up=False)
    
    if keys[pygame.K_UP] and r_paddle.y - l_paddle.VELO >= 0:
        r_paddle.move(up=True)
    if keys[pygame.K_DOWN] and r_paddle.y + PADDLE_H + r_paddle.VELO <= HEIGHT:
        r_paddle.move(up=False)


# Draw window display
def display(wn, paddles, ball, l_score, r_score):
    wn.fill(GREEN)
    
    pygame.draw.line(wn, GRAY, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)

    l_score_text = SCORE_FONT.render(f'{l_score}', 1, WHITE)
    r_score_text = SCORE_FONT.render(f'{r_score}', 1, WHITE)
    wn.blit(l_score_text, (WIDTH*(7/16), 15))
    wn.blit(r_score_text, (WIDTH*(9/16), 15))

    for paddle in paddles:
        paddle.draw(wn)

    ball.draw(wn)

    pygame.display.update()


# Main function
def main():
    run = True
    clock = pygame.time.Clock()

    l_paddle = Paddle(10, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
    r_paddle = Paddle(WIDTH - 10 - PADDLE_W, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    l_score = 0
    r_score = 0

    while run:
        clock.tick(FPS)
        display(wn, [l_paddle, r_paddle], ball, l_score, r_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        ball.move()
        collision(ball, l_paddle, r_paddle)

        keys = pygame.key.get_pressed()
        paddle_movement(keys, l_paddle, r_paddle)

        # Check for score
        if ball.x < 0:
            r_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            l_score += 1
            ball.reset()
        
        # Check for win
        win = False
        if l_score >= WIN_SCORE:
            win = True
            win_text = "Left Player Won"
        elif r_score >= WIN_SCORE:
            win = True
            win_text = "Right Player Won"
        
        # Win callout, reset game
        if win:
            text = WIN_FONT.render(win_text, 1, WHITE)
            wn.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            ball.reset()
            l_paddle.reset()
            r_paddle.reset()
            l_score = 0
            r_score = 0

    pygame.quit

    
if __name__ == '__main__':
    main()
