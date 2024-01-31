import pygame
import sys
import colorsys
import random

# Initialize Pygame
pygame.init()
pygame.mouse.set_visible(False)

# Set up display
infoObject = pygame.display.Info()  # Get information about the screen
width, height = infoObject.current_w, infoObject.current_h  # Get the screen width and height
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Rainbow Brick Breaker")

# Colors
bg_color = (0, 0, 0)

# Brick settings
brick_rows = max(min(int(height / 60), 15), 5)  # Adjust rows according to screen height, set min and max
brick_cols = max(min(int(width / 60), 20), 10)  # Adjust columns according to screen width, set min and max
brick_width = max(min(width // (brick_cols + 1), 100), 20)  # Adjust brick width, set min and max
brick_height = max(min((height // 2) // brick_rows, 60), 10)  # Adjust brick height, set min and max
brick_gap = 5
brick_margin_top = 40  # Adjust margin

# Paddle settings
paddle_width = width // 6  # Adjust paddle width according to screen width
paddle_height = height // 40  # Adjust paddle height according to screen height
paddle_speed = width // 120  # Adjust paddle speed
paddle = pygame.Rect(width // 2 - paddle_width // 2, height - paddle_height * 2, paddle_width, paddle_height)

# Ball settings
ball_radius = height // 80  # Adjust ball radius according to screen height
balls = []  # Create a list to store the balls


def get_rainbow_color(i):
    hue = i % 360
    hue /= 360
    saturation = 1
    value = 1
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    return tuple(int(x * 255) for x in rgb)


def create_rainbow_bricks():
    bricks = []
    # Calculate total width of all bricks and gaps
    total_width = brick_cols * brick_width + (brick_cols - 1) * brick_gap
    # Calculate left margin so that bricks are centered
    left_margin = (width - total_width) // 2

    for row in range(brick_rows):
        brick_row = []
        for col in range(brick_cols):
            brick = pygame.Rect(
                left_margin + col * (brick_width + brick_gap),  # Add space on the sides
                row * (brick_height + brick_gap) + brick_margin_top,  # Add space at the top
                brick_width,
                brick_height,
            )
            brick_row.append(brick)
        bricks.append(brick_row)
    return bricks


def draw_bricks(bricks):
    for row in range(brick_rows):
        for col in range(brick_cols):
            if col < len(bricks[row]):
                brick = bricks[row][col]
                color = get_rainbow_color(row * 60)
                pygame.draw.rect(screen, color, brick)


def move_paddle():
    mouse_x, _ = pygame.mouse.get_pos()
    paddle.centerx = mouse_x
    paddle.clamp_ip(screen.get_rect())


def move_ball(bricks):
    for ball in balls:
        ball.pos[0] += ball.vel[0]
        ball.pos[1] += ball.vel[1]

        # Check for collisions with walls
        if ball.pos[0] <= ball.radius or ball.pos[0] >= width - ball.radius:
            ball.vel[0] = -ball.vel[0]
        if ball.pos[1] <= ball.radius:
            ball.vel[1] = -ball.vel[1]

        # Check for collisions with bricks
        ball_rect = pygame.Rect(ball.pos[0] - ball.radius, ball.pos[1] - ball.radius, ball.radius * 2, ball.radius * 2)
        for row in range(brick_rows):
            for col in range(brick_cols):
                if col < len(bricks[row]):
                    brick = bricks[row][col]
                    if brick.colliderect(ball_rect):
                        bricks[row].pop(col)  # Remove the brick
                        ball.vel[1] = -ball.vel[1]  # Reverse ball velocity
                        break  # Exit the inner loop

        # Check if the ball goes out of the screen
        if ball.pos[1] >= height + ball.radius:
            balls.remove(ball)  # Remove the ball from the list
            reset_ball()  # Reset the ball to its initial position

        # Check for collision with the paddle
        if paddle.colliderect(ball_rect):
            ball.vel[1] = -ball.vel[1]

def all_blocks_gone(bricks):
    return all(len(row) == 0 for row in bricks)

class Ball:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.radius = ball_radius


def reset_ball():
    ball_pos = [width // 2, height - paddle_height - ball_radius - 5]
    ball_vel = [random.choice([-1, 1]) * random.uniform(4, 6), -random.uniform(4, 6)]
    new_ball = Ball(pos=ball_pos, vel=ball_vel)
    balls.append(new_ball)


# Add the first ball to the list
reset_ball()
# Add desired number of balls to the list
for _ in range(3):  # Change this number to add more or fewer balls
    reset_ball()


def draw_ball():
    for ball in balls:
        pygame.draw.circle(screen, (255, 255, 255), list(map(int, ball.pos)), ball.radius)



def draw_paddle():
    pygame.draw.rect(screen, (255, 255, 255), paddle)

def display_win_screen():
    # Clear screen
    screen.fill(bg_color)
    
    # Display "you win" message
    font = pygame.font.Font(None, 74)
    text = font.render("YOU WIN!", 1, (255, 255, 255))
    screen.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
    
    # Display fireworks (this is just an example, you'll need to implement the actual fireworks)
    for _ in range(50):  # Change this number to add more or fewer fireworks
        firework_pos = [random.randint(0, width), random.randint(0, height)]
        pygame.draw.circle(screen, (255, 255, 255), firework_pos, 5)
    
    # Update display
    pygame.display.flip()
    
    # Wait a few seconds before ending the game
    pygame.time.wait(3000)

    pygame.quit()
    sys.exit()

def main():
    global bricks
    bricks = create_rainbow_bricks()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear screen
        screen.fill(bg_color)

        # Move paddle
        move_paddle()

        # Move ball
        move_ball(bricks)
        if all_blocks_gone(bricks):
            display_win_screen()

        # Draw bricks
        draw_bricks(bricks)

        # Draw paddle
        draw_paddle()

        # Draw ball
        draw_ball()

        # Update display
        pygame.display.flip()
        pygame.time.delay(16)  # Control the game speed


if __name__ == "__main__":
    main()
