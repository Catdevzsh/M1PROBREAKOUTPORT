import pygame, sys, numpy as np
pygame.init()
W, H, BR, PW, PH, BW, BH, R, C = 640, 480, 10, 60, 10, 60, 15, 5, 10
WHITE, RED, BLUE = (255, 255, 255), (255, 0, 0), (0, 0, 255)
ball = pygame.Rect(W // 2 - BR // 2, H // 2 - BR // 2, BR * 2, BR * 2)
ball_dx, ball_dy = 3, -3
paddle = pygame.Rect(W // 2 - PW // 2, H - 50, PW, PH)
bricks = [pygame.Rect(j * (BW + 2) + 1, i * (BH + 2) + 1, BW, BH) for i in range(R) for j in range(C)]
powerups = []
screen = pygame.display.set_mode((W, H))
font = pygame.font.Font(None, 36)
score = 0
pygame.mixer.init()
sample_rate, duration, freq = 44100, 0.1, 220.0
t = np.linspace(0, duration, int(sample_rate * duration), False)
square_wave = (0.5 * np.sign(np.sin(2 * np.pi * freq * t)) + 0.5 * 32767).astype(np.int16)
stereo_samples = np.repeat(square_wave[:, None], 2, axis=1)
samples = pygame.sndarray.make_sound(stereo_samples)
def play_sound(): samples.play()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0: paddle.left -= 5
    if keys[pygame.K_RIGHT] and paddle.right < W: paddle.right += 5
    ball.left += ball_dx; ball.top += ball_dy
    if ball.left <= 0 or ball.right >= W: ball_dx = -ball_dx
    if ball.top <= 0: ball_dy = -ball_dy
    if ball.bottom >= H:
        text = font.render("Game Over. Press any key to play again.", True, WHITE)
        screen.blit(text, (W // 2 - text.get_width() // 2, H // 2 - text.get_height() // 2))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYUP: waiting = False
        ball.center = (W // 2, H // 2); ball_dy = -3; score = 0
        bricks = [pygame.Rect(j * (BW + 2) + 1, i * (BH + 2) + 1, BW, BH) for i in range(R) for j in range(C)]
        powerups = []
    if ball.colliderect(paddle): ball_dy = -ball_dy; play_sound()
    brick_collision_index = ball.collidelist(bricks)
    if brick_collision_index != -1: 
        brick = bricks.pop(brick_collision_index); ball_dy = -ball_dy; play_sound(); score += 1
        if np.random.random() < 0.1: powerups.append(pygame.Rect(brick.x, brick.y, 20, 20))
    for powerup in powerups:
        powerup.y += 2
        if paddle.colliderect(powerup):
            powerups.remove(powerup)
            paddle.width += 30
        elif powerup.y > H:
            powerups.remove(powerup)
    screen.fill((0, 0, 0)); pygame.draw.ellipse(screen, WHITE, ball); pygame.draw.rect(screen, WHITE, paddle)
    for brick in bricks: pygame.draw.rect(screen, RED, brick)
    for powerup in powerups: pygame.draw.rect(screen, BLUE, powerup)
    score_text = font.render(f"Score: {score}", True, WHITE); screen.blit(score_text, (10, 10))
    pygame.display.flip(); pygame.time.wait(10)
pygame.quit(); sys.exit()
