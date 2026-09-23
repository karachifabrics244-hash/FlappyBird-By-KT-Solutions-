import pygame, sys, random
pygame.init()
screen_info = pygame.display.Info()
W, H = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Bird Coin Collector")
SKY_BLUE, PIPE_GREEN, BIRD_YELLOW, WHITE, BLACK, RED, COIN_GOLD = (135, 206, 235), (34, 175, 34), (255, 220, 0), (255, 255, 255), (0, 0, 0), (220, 40, 40), (255, 215, 0)
bird_x, bird_y, bird_radius, gravity, velocity = int(W * 0.25), H // 2, int(W * 0.04), 0.4, 0
pipe_width, pipe_gap, pipe_x = int(W * 0.16), int(H * 0.24), W + 50
pipe_height = random.randint(int(H * 0.15), int(H * 0.55))
coin_radius, coin_x, coin_y, coin_active = int(W * 0.025), pipe_x + (pipe_width // 2), pipe_height + (pipe_gap // 2), True
score, coins_collected = 0, 0
font = pygame.font.SysFont("sans", int(W * 0.055), bold=True)
clock = pygame.time.Clock()
running, game_over, game_started = True, False, False
while running:
    screen.fill(SKY_BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if not game_started: game_started = True
            velocity = -7
    top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    bot_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, H)
    bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)
    if game_started and not game_over:
        velocity += gravity
        bird_y += int(velocity)
        pipe_x -= int(W * 0.01)
        coin_x -= int(W * 0.01)
        if pipe_x < -pipe_width:
            pipe_x = W + 50
            pipe_height = random.randint(int(H * 0.15), int(H * 0.55))
            score += 1
            coin_x = pipe_x + (pipe_width // 2)
            coin_y = pipe_height + (pipe_gap // 2)
            coin_active = True
        if coin_active:
            coin_rect = pygame.Rect(coin_x - coin_radius, coin_y - coin_radius, coin_radius * 2, coin_radius * 2)
            if bird_rect.colliderect(coin_rect):
                coins_collected += 1
                coin_active = False
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bot_pipe) or bird_y > H or bird_y < 0: game_over = True
    pygame.draw.rect(screen, PIPE_GREEN, top_pipe)
    pygame.draw.rect(screen, BLACK, top_pipe, 2)
    pygame.draw.rect(screen, PIPE_GREEN, bot_pipe)
    pygame.draw.rect(screen, BLACK, bot_pipe, 2)
    if coin_active:
        pygame.draw.circle(screen, COIN_GOLD, (coin_x, coin_y), coin_radius)
        pygame.draw.circle(screen, BLACK, (coin_x, coin_y), coin_radius, 1)
    pygame.draw.circle(screen, BIRD_YELLOW, (bird_x, bird_y), bird_radius)
    pygame.draw.circle(screen, BLACK, (bird_x, bird_y), bird_radius, 2)
    pygame.draw.circle(screen, WHITE, (bird_x + int(bird_radius*0.4), bird_y - int(bird_radius*0.3)), int(bird_radius*0.25))
    pygame.draw.polygon(screen, RED, [(bird_x + int(bird_radius*0.8), bird_y - 2), (bird_x + int(bird_radius*1.4), bird_y), (bird_x + int(bird_radius*0.8), bird_y + 4)])
    screen.blit(font.render(f"PIPES: {score}", True, BLACK), (30, 30))
    screen.blit(font.render(f"COINS: {coins_collected}", True, RED), (30, 70))
    if not game_started:
        overlay = pygame.Surface((W, H)); overlay.set_alpha(160); overlay.fill(BLACK); screen.blit(overlay, (0, 0))
        txt_title = font.render("FLAPPY COIN HUNTER", True, BIRD_YELLOW)
        txt_tap = font.render("TAP TO FLY & COLLECT", True, WHITE)
        screen.blit(txt_title, (W // 2 - txt_title.get_width() // 2, H // 2 - 40))
        screen.blit(txt_tap, (W // 2 - txt_tap.get_width() // 2, H // 2 + 20))
    if game_over:
        overlay = pygame.Surface((W, H)); overlay.set_alpha(200); overlay.fill(BLACK); screen.blit(overlay, (0, 0))
        txt_go = font.render("GAME OVER", True, RED)
        txt_fs = font.render(f"Pipes Cross: {score}", True, WHITE)
        txt_fc = font.render(f"Coins Pocketed: {coins_collected}", True, COIN_GOLD)
        screen.blit(txt_go, (W // 2 - txt_go.get_width() // 2, H // 2 - 60))
        screen.blit(txt_fs, (W // 2 - txt_fs.get_width() // 2, H // 2 - 10))
        screen.blit(txt_fc, (W // 2 - txt_fc.get_width() // 2, H // 2 + 35))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
