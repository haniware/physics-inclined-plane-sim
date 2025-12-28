import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inclined Plane Simulation")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

class InputBox:
    def __init__(self, x, y, w, h, label, default=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (200, 200, 200)
        self.color_active = (100, 150, 255)
        self.color = self.color_inactive
        self.text = default
        self.label = label
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            elif event.unicode.isdigit() or event.unicode in '.-':
                self.text += event.unicode
        return False

    def draw(self, screen):
        label_surf = small_font.render(self.label, True, (0, 0, 0))
        screen.blit(label_surf, (self.rect.x, self.rect.y - 30))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surf = small_font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

    def get_value(self):
        try:
            return float(self.text)
        except:
            return 0.0

input_boxes = [
    InputBox(250, 150, 300, 40, "Initial Velocity (m/s):", "3.5"),
    InputBox(250, 230, 300, 40, "Incline Angle (degrees):", "32"),
    InputBox(250, 310, 300, 40, "Gravity (m/s²):", "9.8")
]

start_button = pygame.Rect(300, 400, 200, 50)

state = "INPUT"
running = True
t = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "INPUT":
            for box in input_boxes:
                if box.handle_event(event):
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    v0 = input_boxes[0].get_value()
                    theta = input_boxes[1].get_value()
                    g = input_boxes[2].get_value()

                    theta_rad = math.radians(theta)
                    a = -g * math.sin(theta_rad)
                    distance = -v0**2 / (2 * a)
                    time_to_max = -v0 / a
                    return_velocity = v0

                    state = "RESULTS"
                    results_timer = pygame.time.get_ticks()

        elif state == "RESULTS":
            if event.type == pygame.MOUSEBUTTONDOWN or (pygame.time.get_ticks() - results_timer > 3000):
                state = "ANIMATION"
                t = 0

    screen.fill((255, 255, 255))

    if state == "INPUT":
        title = font.render("Inclined Plane Simulation", True, (0, 0, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for box in input_boxes:
            box.draw(screen)

        mouse_pos = pygame.mouse.get_pos()
        button_color = (100, 200, 100) if start_button.collidepoint(mouse_pos) else (50, 150, 50)
        pygame.draw.rect(screen, button_color, start_button)
        pygame.draw.rect(screen, (0, 100, 0), start_button, 3)
        button_text = small_font.render("START", True, (255, 255, 255))
        screen.blit(button_text, (start_button.x + 70, start_button.y + 12))

    elif state == "RESULTS":
        title = font.render("Results", True, (0, 0, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        results = [
            f"(a) Distance: {distance:.3f} m",
            f"(b) Time: {time_to_max:.3f} s",
            f"(c) Return Velocity: {return_velocity:.3f} m/s"
        ]

        for i, result in enumerate(results):
            text = small_font.render(result, True, (0, 150, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 50))

        hint = small_font.render("Click or wait to see animation...", True, (150, 150, 150))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 450))

    elif state == "ANIMATION":
        if t <= time_to_max:
            s = v0 * t + 0.5 * a * t**2
            v = v0 + a * t
            direction = "UP"
        else:
            t_return = t - time_to_max
            s = distance - (0.5 * (-a) * t_return**2)
            s = max(0, s)
            v = -a * t_return
            direction = "DOWN"

        if t >= time_to_max * 2:
            t = 0

        scale = 100
        start_x = 100
        start_y = 500

        incline_length = distance * scale + 100
        end_x = start_x + incline_length * math.cos(theta_rad)
        end_y = start_y - incline_length * math.sin(theta_rad)

        pygame.draw.line(screen, (100, 100, 100), (start_x, start_y), (end_x, end_y), 3)
        pygame.draw.line(screen, (200, 200, 200), (start_x - 50, start_y), (start_x + incline_length, start_y), 1)

        obj_x = start_x + s * scale * math.cos(theta_rad)
        obj_y = start_y - s * scale * math.sin(theta_rad)

        pygame.draw.circle(screen, (255, 0, 0), (int(obj_x), int(obj_y)), 15)
        pygame.draw.circle(screen, (100, 0, 0), (int(obj_x), int(obj_y)), 15, 2)

        texts = [
            f"Time: {t:.2f}s / {time_to_max * 2:.2f}s",
            f"Position: {s:.3f}m / {distance:.3f}m",
            f"Velocity: {abs(v):.2f}m/s {direction}",
            f"Angle: {theta}°"
        ]

        for i, text_str in enumerate(texts):
            text = small_font.render(text_str, True, (0, 0, 0))
            screen.blit(text, (10, 20 + i * 30))

        title = font.render("Inclined Plane Motion", True, (0, 0, 255))
        screen.blit(title, (WIDTH - 350, 20))

        t += 1 / 60

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
