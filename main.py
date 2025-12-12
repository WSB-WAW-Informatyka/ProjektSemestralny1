import os
import sys
import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        if font:
            text_surf = font.render(self.text, True, (240, 240, 240))
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered


def main():
    pygame.init()

    VERSION: str = "0.0.1"

    WIDTH: int = 1920
    HEIGHT: int = 1080
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Giereczka")
    clock = pygame.time.Clock()

    try:
        _ = pygame.font
        pygame.font.init()
        font_available = True
    except Exception:
        font_available = False

    if font_available:
        title_font = pygame.font.SysFont("arial", 72)
        button_font = pygame.font.SysFont("arial", 36)
    else:
        title_font = button_font = None
        print("Warning: pygame font module not available — continuing without rendered text.")

    base_dir = os.path.dirname(__file__)
    bg_candidates = [
        os.path.join(base_dir, "assets", "background.png"),
        os.path.join(base_dir, "background.png"),
    ]
    background = None
    for path in bg_candidates:
        if not os.path.isfile(path):
            print(f"Background not found at: {path}")
            continue
        try:
            img = pygame.image.load(path)
            background = pygame.transform.smoothscale(img.convert_alpha(), (WIDTH, HEIGHT))
            print(f"Loaded background (pygame): {path}")
            break
        except Exception as e:
            print(f"pygame failed to load '{path}': {e}")
            try:
                from PIL import Image
                pil = Image.open(path).convert("RGBA")
                data = pil.tobytes()
                surf = pygame.image.frombuffer(data, pil.size, "RGBA")
                background = pygame.transform.smoothscale(surf.convert_alpha(), (WIDTH, HEIGHT))
                print(f"Loaded background via Pillow: {path}")
                break
            except Exception as e2:
                print(f"Pillow fallback also failed for '{path}': {e2}")
                background = None
                continue

    # Colors
    BG_COLOR = (12, 12, 30)
    TITLE_COLOR = (240, 240, 240)
    BUTTON_COLOR = (60, 100, 60)
    BUTTON_HOVER_COLOR = (100, 160, 100)

    # Create buttons
    button_width = 300
    button_height = 60
    button_x = (WIDTH - button_width) // 2
    start_button = Button(button_x, HEIGHT // 2, button_width, button_height, "Start", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    settings_button = Button(button_x, HEIGHT // 2 + 100, button_width, button_height, "Ustawienia", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    quit_button = Button(button_x, HEIGHT // 2 + 200, button_width, button_height, "Wyjdź", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    buttons = [start_button, settings_button, quit_button]

    running = True
    started = False
    while running and not started:
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event):
                    started = True
                elif settings_button.is_clicked(event):
                    print("Settings button pressed")
                    # TODO: otworzyć menu ustawień
                elif quit_button.is_clicked(event):
                    running = False

        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BG_COLOR)

        if font_available and title_font:
            title_surf = title_font.render("Giereczka o wężu", True, TITLE_COLOR)
            screen.blit(title_surf, ((WIDTH - title_surf.get_width()) // 2, HEIGHT // 4))

        for button in buttons:
            button.draw(screen, button_font)

        # Version label
        if font_available and button_font:
            version_font = pygame.font.SysFont("arial", 48)
            version_surf = version_font.render(f"v{VERSION}", True, (0, 0, 0))
            screen.blit(version_surf, (20, HEIGHT - 60))

        pygame.display.flip()
        clock.tick(60)

    if started:
        print("Game start requested (Start button pressed).")
        # TODO: rozpocząć grę
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
