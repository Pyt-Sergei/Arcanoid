import pygame as pg
import sys
from random import randrange as rnd


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10: # delta_x == delta_y
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    else:
        dx = -dx

    return dx, dy


WIDTH, HEIGHT = 1200, 700
fps = 60

# platform setting
platform_w, platform_h = 330, 30
platform_speed = 15
platform = pg.Rect(WIDTH // 2 - platform_w // 2, HEIGHT - platform_h - 10, platform_w, platform_h )

#ball setting
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pg.Rect( rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# blocks setting variations
block_list = [pg.Rect(10 + 120 * i, 10 + 50 * j, 100,30) for i in range(10) for j in range(4)]
color_list = [( rnd(60, 255), rnd(60, 255), rnd(60, 255) ) for  i in range(10) for j in range(4)]
#block_list = [pg.Rect(20 + 117 * i, 20 + 40 * j, 107,30) for i in range(10) for j in range(4)]
#color_list = [( rnd(60, 255), rnd(60, 255), rnd(60, 255) ) for  i in range(10) for j in range(4)]
#block_list = [pg.Rect(120 * i, 50 + 30 * j, 120,30) for i in range(10) for j in range(6)]
#color_list = [( rnd(60, 255), rnd(60, 255), rnd(60, 255) ) for  i in range(10) for j in range(6)]

pg.init()
sc = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()
pg.display.set_caption('Arcanoid')
end_font = pg.font.Font('typo_pixel.ttf', 40)
wi_font = pg.font.Font('typo_pixel.ttf', 40)

while True:
    sc.fill(pg.Color('darkslategray'))

    [sys.exit() for event in pg.event.get() if event.type == pg.QUIT ]

    # drawing
    pg.draw.circle  (sc, pg.Color('lightblue'),ball.center, ball_radius )
    [pg.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pg.draw.rect(sc, pg.Color('yellow'), platform)

    # ball movement
    ball.x += dx * ball_speed
    ball.y += dy * ball_speed

    # collisions left & right
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    # collision bottom
    if ball.centery < ball_radius:
        dy = -dy
    # collision with platform
    if ball.colliderect(platform) and dy > 0:
         dx, dy = detect_collision(dx, dy, ball, platform)
    # collision with block
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        fps += 2

    # control platform
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and platform.left > 0:
        platform.left -= platform_speed
    if keys[pg.K_RIGHT] and platform.right < WIDTH:
        platform.left += platform_speed

    pg.display.flip()
    clock.tick(fps)