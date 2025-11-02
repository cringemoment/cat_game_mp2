#THIS IS CHATGPT
#JUST USED TO TEST

import pygame
import sys

pygame.init()
pygame.joystick.init()

# Window setup
WIDTH, HEIGHT = 600, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Controller Tester")

font = pygame.font.SysFont("consolas", 20)
clock = pygame.time.Clock()

# Initialize joystick(s)
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for j in joysticks:
    j.init()

def draw_text(surface, text, x, y, color=(255, 255, 255)):
    """Helper function to draw text."""
    surface.blit(font.render(text, True, color), (x, y))

def render_controller_info():
    """Display all joystick info on screen."""
    y = 20
    if not joysticks:
        draw_text(window, "No controllers detected.", 20, y, (255, 100, 100))
        return

    for j in joysticks:
        draw_text(window, f"🎮 {j.get_name()}", 20, y); y += 30
        draw_text(window, f"  Axes: {j.get_numaxes()}", 40, y); y += 25
        for i in range(j.get_numaxes()):
            axis = j.get_axis(i)
            draw_text(window, f"    Axis {i}: {axis:+.2f}", 60, y)
            y += 20

        draw_text(window, f"  Buttons: {j.get_numbuttons()}", 40, y); y += 25
        for i in range(j.get_numbuttons()):
            pressed = j.get_button(i)
            color = (100, 255, 100) if pressed else (200, 200, 200)
            draw_text(window, f"    Button {i}: {'Pressed' if pressed else 'Released'}", 60, y, color)
            y += 20

        draw_text(window, f"  Hats (D-Pad): {j.get_numhats()}", 40, y); y += 25
        for i in range(j.get_numhats()):
            hat = j.get_hat(i)
            draw_text(window, f"    Hat {i}: {hat}", 60, y)
            y += 20

        y += 20

def main():
    """Main loop."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill((20, 20, 20))
        render_controller_info()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
