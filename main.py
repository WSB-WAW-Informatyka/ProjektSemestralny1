import os
import sys
import pygame

class Button:
    def __init__(self, x, y, width, height, text_id, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_id = text_id
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface, font, lang_texts):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text = lang_texts[self.text_id]
        text_surf = font.render(text, True, (240, 240, 240))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered


# GLOBALNE (dla patcha jakości)
quality_setting = "high"


def main():
    pygame.init()

    VERSION: str = "0.0.1"

    WIDTH: int = 1920
    HEIGHT: int = 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Giereczka")
    clock = pygame.time.Clock()

    pygame.font.init()
    title_font = pygame.font.SysFont("arial", 72)
    button_font = pygame.font.SysFont("arial", 36)

    # Języki
    LANG_PL: dict[str] = {
        "title": "Giereczka o wężu",
        "start": "Start",
        "settings": "Ustawienia",
        "quit": "Wyjdź",
        "settings_title": "Ustawienia",
        "quality": "Jakość",
        "language": "Język",
        "exit": "Wyjście",
        "quality_title": "Jakość",
        "low": "Niska",
        "high": "Wysoka",
        "language_title": "Język",
        "pl": "Polski",
        "en": "Angielski"
    }

    LANG_EN: dict[str] = {
        "title": "Snake Game",
        "start": "Start",
        "settings": "Settings",
        "quit": "Quit",
        "settings_title": "Settings",
        "quality": "Quality",
        "language": "Language",
        "exit": "Back",
        "quality_title": "Quality",
        "low": "Low",
        "high": "High",
        "language_title": "Language",
        "pl": "Polish",
        "en": "English"
    }

    current_lang: dict[str] = LANG_PL

    # Colors
    BG_COLOR = (12, 12, 30)
    BUTTON_COLOR = (60, 100, 60)
    BUTTON_HOVER_COLOR = (100, 160, 100)

    # Buttons
    button_w, button_h = 300, 60
    bx = (WIDTH - button_w) // 2

    start_button = Button(bx, HEIGHT // 2, button_w, button_h, "start", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    settings_button = Button(bx, HEIGHT // 2 + 100, button_w, button_h, "settings", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    quit_button = Button(bx, HEIGHT // 2 + 200, button_w, button_h, "quit", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    main_buttons = [start_button, settings_button, quit_button]

    quality_button = Button(bx, HEIGHT // 2, button_w, button_h, "quality", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    language_button = Button(bx, HEIGHT // 2 + 100, button_w, button_h, "language", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    settings_exit_button = Button(bx, HEIGHT // 2 + 200, button_w, button_h, "exit", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    settings_buttons = [quality_button, language_button, settings_exit_button]

    # MENU JAKOŚCI — tylko Niska / Wysoka / Wyjście
    quality_low = Button(bx, HEIGHT // 2, button_w, button_h, "low", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    quality_high = Button(bx, HEIGHT // 2 + 100, button_w, button_h, "high", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    quality_exit = Button(bx, HEIGHT // 2 + 200, button_w, button_h, "exit", BUTTON_COLOR, BUTTON_HOVER_COLOR)

    quality_buttons = [
        quality_low,
        quality_high,
        quality_exit
    ]

    # język
    lang_pl_btn = Button(bx, HEIGHT // 2, button_w, button_h, "pl", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    lang_en_btn = Button(bx, HEIGHT // 2 + 100, button_w, button_h, "en", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    lang_exit_btn = Button(bx, HEIGHT // 2 + 200, button_w, button_h, "exit", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    language_buttons = [lang_pl_btn, lang_en_btn, lang_exit_btn]

    current_screen = "main"

    global quality_setting
    quality_setting = "high"

    running: bool = True
    started: bool = False

    while running and not started:
        mouse = pygame.mouse.get_pos()

        # HOVER UPDATE
        if current_screen == "main":
            for b in main_buttons: b.update(mouse)
        elif current_screen == "settings":
            for b in settings_buttons: b.update(mouse)
        elif current_screen == "quality":
            for b in quality_buttons: b.update(mouse)
        elif current_screen == "language":
            for b in language_buttons: b.update(mouse)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "main":
                    if start_button.is_clicked(event):
                        started = True
                    elif settings_button.is_clicked(event):
                        current_screen = "settings"
                    elif quit_button.is_clicked(event):
                        running = False

                elif current_screen == "settings":
                    if quality_button.is_clicked(event):
                        current_screen = "quality"
                    elif language_button.is_clicked(event):
                        current_screen = "language"
                    elif settings_exit_button.is_clicked(event):
                        current_screen = "main"

                elif current_screen == "quality":
                    if quality_low.is_clicked(event):
                        quality_setting = "low"
                    elif quality_high.is_clicked(event):
                        quality_setting = "high"
                    elif quality_exit.is_clicked(event):
                        current_screen = "settings"

                elif current_screen == "language":
                    if lang_pl_btn.is_clicked(event):
                        current_lang = LANG_PL
                    elif lang_en_btn.is_clicked(event):
                        current_lang = LANG_EN
                    elif lang_exit_btn.is_clicked(event):
                        current_screen = "settings"

        # DRAW
        screen.fill(BG_COLOR)

        if current_screen == "main":
            title = title_font.render(current_lang["title"], True, (240, 240, 240))
            screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 4))
            for b in main_buttons:
                b.draw(screen, button_font, current_lang)

        elif current_screen == "settings":
            title = title_font.render(current_lang["settings_title"], True, (240, 240, 240))
            screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 4))
            for b in settings_buttons:
                b.draw(screen, button_font, current_lang)

        elif current_screen == "quality":
            title = title_font.render(current_lang["quality_title"], True, (240, 240, 240))
            screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 4))
            for b in quality_buttons:
                b.draw(screen, button_font, current_lang)

        elif current_screen == "language":
            title = title_font.render(current_lang["language_title"], True, (240, 240, 240))
            screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 4))
            for b in language_buttons:
                b.draw(screen, button_font, current_lang)

        version_font = pygame.font.SysFont("arial", 48)
        version_surf = version_font.render(f"v{VERSION}", True, (0, 0, 0))
        screen.blit(version_surf, (20, HEIGHT - 60))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# --- SYSTEM JAKOŚCI ---
def get_scale_from_quality(q):
    if q == "low":
        return 0.4
    return 1.0  # high = pełna jakość


_original_flip = pygame.display.flip

def patched_flip():
    global quality_setting

    scale = get_scale_from_quality(quality_setting)

    if scale == 1:
        _original_flip()
        return

    screen_surf = pygame.display.get_surface()
    w, h = screen_surf.get_size()

    small = pygame.transform.smoothscale(screen_surf, (int(w * scale), int(h * scale)))
    big = pygame.transform.scale(small, (w, h))

    pygame.display.get_surface().blit(big, (0, 0))
    pygame.display.update()

pygame.display.flip = patched_flip


if __name__ == "__main__":
    main()