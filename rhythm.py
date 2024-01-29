import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 1
SHOOT_DELAY = 20

# Colors
PASTEL_BLUE = (173, 216, 230)
PASTEL_PINK = (255, 182, 193)
PASTEL_YELLOW = (255, 255, 153)
PASTEL_GREEN = (144, 238, 144)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
NEON = (57, 255, 20)
BLACK = (0, 0, 0)

# Particles
particles = []

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top of the Point Rhythm Game")

# Fonts
font = pygame.font.Font(None, 36)

# Function to generate random triangles
def generate_random_triangle():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    size = random.randint(20, 40)
    color = random.choice([PASTEL_BLUE, PASTEL_PINK, PASTEL_YELLOW, PASTEL_GREEN])
    velocity = random.uniform(1, 5)  # Random velocity for varying speeds
    return [(x, y - size), (x - size, y + size), (x + size, y + size), color, velocity]

# Generate initial triangles
triangles = [generate_random_triangle() for _ in range(5)]

# Game loop
clock = pygame.time.Clock()
running = True
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            for triangle in triangles:
                if pygame.Rect(triangle[0], triangle[2]).collidepoint(mouseX, mouseY):
                    # Triangle clicked, remove and spawn a new one
                    triangles.remove(triangle)
                    triangles.append(generate_random_triangle())
                    particles.extend([(triangle[0][0], triangle[0][1], random.choice([PASTEL_BLUE, PASTEL_PINK, PASTEL_YELLOW, PASTEL_GREEN]), random.randint(5, 10), random.uniform(0, 2*math.pi)) for _ in range(20)])
                    # Increase the score
                    score += 1

    # Update triangles
    for triangle in triangles:
        x, y, size, color, velocity = triangle[0][0], triangle[0][1], triangle[2][1] - triangle[1][1], triangle[3], triangle[4]
        y += velocity
        if y > HEIGHT + size:
            # Reset triangle if it goes below the screen
            y = -size
            x = random.randint(50, WIDTH - 50)
            velocity = random.uniform(1, 5)
        triangle[0] = (x, y - size)
        triangle[1] = (x - size, y + size)
        triangle[2] = (x + size, y + size)
        triangle[4] = velocity

    # Update particles
    particles = [(p[0] + math.cos(p[4]) * 2, p[1] + math.sin(p[4]) * 2, p[2], p[3] - 0.5, p[4] + 0.1) for p in particles if p[3] > 0]

    # Draw everything
    screen.fill(BLACK)  # Background color
    for triangle in triangles:
        pygame.draw.polygon(screen, triangle[3], triangle[:3])

    for particle in particles:
        pygame.draw.circle(screen, particle[2], (int(particle[0]), int(particle[1])), int(particle[3]))

    # Display the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
