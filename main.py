# Example file showing a circle moving on screen
import pygame
# Removed invalid import; use pygame.Rect directly in the code



# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

green_images = [] 
for i in range(1, 8):
  image = pygame.image.load(f"sprites/green_virus/Green{i}.png").convert_alpha()
  scaled_image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
  green_images.append(scaled_image)

blue_images = []
for i in range(1, 8):
  image = pygame.image.load(f"sprites/blue_virus/Blue{i}.png").convert_alpha()
  scaled_image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
  blue_images.append(scaled_image)

# Bullet state
bullets = []
bullet_speed = 700
bullet_radius = 6
shoot_cooldown = 0.15  # seconds between shots
shoot_timer = 0.0
bullet_damage = 25

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
enemy_pos = pygame.Vector2(screen.get_width() / 4, screen.get_height() / 4)
enemy_killed = False
enemy_max_health = 100
enemy_health = enemy_max_health

current_sprite = 1
image_clock = 0
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # Update bullets
    for b in bullets:
        b["pos"] += b["vel"] * dt

    # Check bullet collisions against the enemy using circle distance
    for b in bullets[:]:
      if not enemy_killed:
        img = blue_images[current_sprite]
        enemy_center = pygame.Vector2(enemy_pos.x + img.get_width() / 2, enemy_pos.y + img.get_height() / 2)
        enemy_radius = 25
        if (b["pos"] - enemy_center).length() <= enemy_radius:
          enemy_health -= bullet_damage
          try:
            bullets.remove(b)
          except ValueError:
            pass
          if enemy_health <= 0:
            enemy_killed = True

    shoot_timer -= dt
    bullet_position = pygame.Vector2(player_pos.x + green_images[current_sprite].get_width() / 2, player_pos.y + green_images[current_sprite].get_height() / 2)
    if keys[pygame.K_UP]:
      bullets.append({
        "pos": bullet_position,
        "vel": pygame.Vector2(0, -bullet_speed),
      })
      shoot_timer = shoot_cooldown
    if keys[pygame.K_DOWN]:
      bullets.append({
        "pos": bullet_position,
        "vel": pygame.Vector2(0, bullet_speed),
      })
      shoot_timer = shoot_cooldown
    if keys[pygame.K_LEFT]:
      bullets.append({
        "pos": bullet_position,
        "vel": pygame.Vector2(-bullet_speed, 0),
      })
      shoot_timer = shoot_cooldown
    if keys[pygame.K_RIGHT]:
      bullets.append({
        "pos": bullet_position,
        "vel": pygame.Vector2(bullet_speed, 0),
      })
      shoot_timer = shoot_cooldown
    
    # Remove off-screen bullets
    bullets = [
        b for b in bullets
        if -20 <= b["pos"].x <= screen.get_width() + 20
        and -20 <= b["pos"].y <= screen.get_height() + 20
    ]
    # Remove 0 velocity bullets
    bullets = [
        b for b in bullets
        if b["vel"].length() > 0
    ]

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    for b in bullets:
        pygame.draw.circle(screen, "yellow", (int(b["pos"].x), int(b["pos"].y)), bullet_radius)
    screen.blit(green_images[current_sprite], player_pos)

    if not enemy_killed:
      img = blue_images[current_sprite]
      center_x = int(enemy_pos.x + img.get_width() / 2)
      # Draw health bar above the enemy
      bar_width = 56
      bar_height = 8
      bar_x = center_x - bar_width // 2
      bar_y = int(enemy_pos.y) - 12
      # Background
      pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(bar_x, bar_y, bar_width, bar_height))
      # Foreground (health)
      fg_width = max(0, int(bar_width * (enemy_health / enemy_max_health)))
      pygame.draw.rect(screen, (50, 200, 50), pygame.Rect(bar_x, bar_y, fg_width, bar_height))
      # Optional border
      pygame.draw.rect(screen, (0,0,0), pygame.Rect(bar_x, bar_y, bar_width, bar_height), 1)
      # Draw enemy sprite
      screen.blit(img, enemy_pos)

    


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

    if image_clock % 5 == 0:
      current_sprite = (current_sprite + 1) % len(green_images)

    image_clock += 1

    for b in bullets:
        print(b["vel"].length())


pygame.quit()