# Example file showing a circle moving on screen
import pygame



# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

images = [] 
for i in range(1, 8):
  image = pygame.image.load(f"sprites/green_virus/Green{i}.png").convert_alpha()
  scaled_image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
  images.append(scaled_image)



player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

current_sprite = 1
image_clock = 0
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    screen.blit(images[current_sprite], player_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

    if image_clock % 5 == 0:
      current_sprite = (current_sprite + 1) % len(images)

    image_clock += 1

pygame.quit()