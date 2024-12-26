import pygame
import time
import random

pygame.init()
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

STAR_WIDTH = 10
STAR_HEIGHT = 20 

velocity = 10


FONT = pygame.font.SysFont('comicsans', 30)

def draw(player, elapsed_time, stars, hit, seeds):
    WIN.fill('blue')

    time_text = FONT.render(f'TIME: {round(elapsed_time)}s', 1, 'white')
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, 'red', player)
    
    for star in stars:
        pygame.draw.rect(WIN, 'white', star)

    for seed in seeds:
        pygame.draw.rect(WIN, 'black', seed)
    if hit:
        game_over_text = FONT.render("GAME OVER", 1, 'white')
        WIN.blit(game_over_text, (WIDTH / 2, HEIGHT / 2))

    pygame.display.flip()
    pygame.display.update()

def main():
    run = True

    hit = False

    game_over_time = 0

    player = pygame.Rect(WIDTH / 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    start_time = time.time()

    elapsed_time = 0
    
    stars = []
    seeds = []

    star_increment = 1
    last_increment_time = pygame.time.get_ticks()
    increment_interval = 10000  # 10 seconds in milliseconds

    star_addition_interval = 1000  # 1 second in milliseconds
    last_star_add_time = pygame.time.get_ticks()

    seed_count = 1
    

    while run:

        current_time = pygame.time.get_ticks()

# Check if it's time to increment the star count
        if current_time - last_increment_time >= increment_interval:
            star_increment += 1
            last_increment_time = current_time

# Check if it's time to add new stars
        if current_time - last_star_add_time >= star_addition_interval:
            for _ in range(star_increment):
                star_x = random.randint(0, WIDTH)
                star = pygame.Rect(star_x, 0, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            last_star_add_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - velocity >= 0:
            player.x -= velocity
        if keys[pygame.K_RIGHT] and player.x + velocity + PLAYER_WIDTH <= WIDTH:
            player.x += velocity
        if keys[pygame.K_UP] and player.y - velocity >= 0:
            player.y -= velocity
        if keys[pygame.K_DOWN] and player.y + velocity <= HEIGHT:
            player.y += velocity

        for _ in range(seed_count):
            seed_x = random.randint(0, WIDTH)
            seed_y = random.randint(0, HEIGHT - PLAYER_HEIGHT)
            seed = pygame.Rect(seed_x, seed_y, STAR_WIDTH, STAR_HEIGHT)
            seeds.append(seed)




        if player.colliderect(seed):
            seed_count += 1
        
        
        if not hit:

            for star in stars[:]:
                star.y += velocity
                if star.y >= HEIGHT - STAR_HEIGHT:
                    stars.remove(star)
                elif player.colliderect(star):
                    stars.remove(star)
                    hit = True
                    game_over_time = pygame.time.get_ticks()
                
                 
        draw(player, elapsed_time, stars, hit, seeds)

        if hit:
            current_time = pygame.time.get_ticks()
            if current_time - game_over_time >= 5000:
                run = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
