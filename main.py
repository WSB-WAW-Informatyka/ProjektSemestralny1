import os
import sys
import pygame
import random

class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_size = 30
        self.grid_width = width // self.tile_size
        self.grid_height = height // self.tile_size
        
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.obstacles = self.create_obstacles()
        self.food = self.spawn_food()
        self.score = 0
        self.move_counter = 0
        self.move_interval = 5
        
    def create_obstacles(self):
        obstacles = []
        for x in range(5, 15):
            obstacles.append((x, 10))
        for y in range(15, 25):
            obstacles.append((20, y))
        for x in range(25, 35):
            obstacles.append((x, 20))
        return obstacles
    
    def spawn_food(self):
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                return (x, y)
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction[1] == 0:
                self.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction[1] == 0:
                self.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction[0] == 0:
                self.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction[0] == 0:
                self.next_direction = (1, 0)
    
    def update(self):
        self.move_counter += 1
        if self.move_counter < self.move_interval:
            return False
        
        self.move_counter = 0
        self.direction = self.next_direction
        
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            return True  # Game over
        
        if new_head in self.snake:
            return True  # Game over
        
        if new_head in self.obstacles:
            return True  # Game over
        
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()
        
        return False
    
    def draw(self, surface):
        surface.fill((20, 20, 40))
        
        grid_color = (40, 40, 60)
        for x in range(0, self.width, self.tile_size):
            pygame.draw.line(surface, grid_color, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, self.tile_size):
            pygame.draw.line(surface, grid_color, (0, y), (self.width, y), 1)
        
        obstacle_color = (100, 100, 150)
        for obs in self.obstacles:
            pygame.draw.rect(surface, obstacle_color,
                           (obs[0] * self.tile_size + 1, obs[1] * self.tile_size + 1,
                            self.tile_size - 2, self.tile_size - 2))
        
        food_color = (255, 200, 0)
        pygame.draw.rect(surface, food_color,
                        (self.food[0] * self.tile_size + 2, self.food[1] * self.tile_size + 2,
                         self.tile_size - 4, self.tile_size - 4))
        
        snake_color = (100, 255, 100)
        head_color = (150, 255, 150)
        
        head = self.snake[0]
        pygame.draw.rect(surface, head_color,
                        (head[0] * self.tile_size + 1, head[1] * self.tile_size + 1,
                         self.tile_size - 2, self.tile_size - 2))
        
        for segment in self.snake[1:]:
            pygame.draw.rect(surface, snake_color,
                           (segment[0] * self.tile_size + 1, segment[1] * self.tile_size + 1,
                            self.tile_size - 2, self.tile_size - 2))


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


# GLOBALNE
quality_setting = "high"


def main():
    pygame.init()

    VERSION: str = "0.3"

    WIDTH: int = 1280
    HEIGHT: int = 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Giereczka")
    clock = pygame.time.Clock()

    pygame.font.init()
    title_font = pygame.font.SysFont("arial", 72)
    button_font = pygame.font.SysFont("arial", 36)

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

    # Języki
    LANG_PL: dict[str] = {
        "title": "Giereczka o wężu",
        "start": "Start",
        "settings": "Ustawienia",
        "quit": "Wyjdź",
        "settings_title": "Ustawienia",
        "quality": "Jakość",
        "language": "Język",
        "exit": "Powrót",
        "quality_title": "Jakość",
        "low": "Niska",
        "high": "Wysoka",
        "language_title": "Język",
        "pl": "Polski",
        "en": "Angielski",
        "pause": "PAUZA",
        "continue": "Kontynuuj",
        "restart": "Restart",
        "main_menu": "Menu główne",
        "game_over": "KONIEC GRY",
        "retry": "Ponów"
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
        "en": "English",
        "pause": "PAUSE",
        "continue": "Continue",
        "restart": "Restart",
        "main_menu": "Main Menu",
        "game_over": "GAME OVER",
        "retry": "Retry"
    }

    current_lang: dict[str] = LANG_PL

    # Kolorki
    BG_COLOR = (12, 12, 30)
    BUTTON_COLOR = (60, 100, 60)
    BUTTON_HOVER_COLOR = (100, 160, 100)

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

    # MENU JAKOŚCI
    quality_low = Button(bx, HEIGHT // 2, button_w, button_h, "low", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    quality_high = Button(bx, HEIGHT // 2 + 100, button_w, button_h, "high", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    quality_exit = Button(bx, HEIGHT // 2 + 200, button_w, button_h, "exit", BUTTON_COLOR, BUTTON_HOVER_COLOR)

    quality_buttons = [
        quality_low,
        quality_high,
        quality_exit
    ]

    # JĘZYK
    lang_pl_btn = Button(bx, HEIGHT // 2, button_w, button_h, "pl", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    lang_en_btn = Button(bx, HEIGHT // 2 + 100, button_w, button_h, "en", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    lang_exit_btn = Button(bx, HEIGHT // 2 + 200, button_w, button_h, "exit", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    language_buttons = [lang_pl_btn, lang_en_btn, lang_exit_btn]

    # MENU PAUZY
    pause_continue = Button(bx, HEIGHT // 2, button_w, button_h, "continue", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    pause_restart = Button(bx, HEIGHT // 2 + 100, button_w, button_h, "restart", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    pause_menu = Button(bx, HEIGHT // 2 + 200, button_w, button_h, "main_menu", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    pause_buttons = [pause_continue, pause_restart, pause_menu]

    # MENU GAME OVER
    game_over_retry = Button(bx, HEIGHT // 2, button_w, button_h, "retry", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    game_over_menu = Button(bx, HEIGHT // 2 + 100, button_w, button_h, "main_menu", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    game_over_buttons = [game_over_retry, game_over_menu]

    current_screen = "main"

    global quality_setting
    quality_setting = "high"

    running: bool = True
    started: bool = False

    while running:
        while running and not started:
            mouse = pygame.mouse.get_pos()

            if current_screen == "main":
                for b in main_buttons: b.update(mouse)
            elif current_screen == "settings":
                for b in settings_buttons: b.update(mouse)
            elif current_screen == "quality":
                for b in quality_buttons: b.update(mouse)
            elif current_screen == "language":
                for b in language_buttons: b.update(mouse)

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

            if background:
                screen.blit(background, (0, 0))
            else:
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

    # GAME LOOP
        if started and running:
            game = SnakeGame(WIDTH, HEIGHT)
            game_over = False
            is_paused = False
            return_to_menu = False
            
            while running and not return_to_menu:
                mouse = pygame.mouse.get_pos()
                
                if is_paused:
                    for b in pause_buttons:
                        b.update(mouse)
                
                if game_over:
                    for b in game_over_buttons:
                        b.update(mouse)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE and not is_paused and not game_over:
                            is_paused = True
                        elif not is_paused and not game_over:
                            game.handle_input(event)
                    
                    if is_paused and event.type == pygame.MOUSEBUTTONDOWN:
                        if pause_continue.is_clicked(event):
                            is_paused = False
                        elif pause_restart.is_clicked(event):
                            game = SnakeGame(WIDTH, HEIGHT)
                            game_over = False
                            is_paused = False
                        elif pause_menu.is_clicked(event):
                            return_to_menu = True
                    
                    if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                        if game_over_retry.is_clicked(event):
                            game = SnakeGame(WIDTH, HEIGHT)
                            game_over = False
                        elif game_over_menu.is_clicked(event):
                            return_to_menu = True
                
                if not is_paused and not game_over:
                    game_over = game.update()
                
                game.draw(screen)
                
                score_font = pygame.font.SysFont("arial", 36)
                score_surf = score_font.render(f"Score: {game.score}", True, (240, 240, 240))
                screen.blit(score_surf, (20, 20))
                
                if is_paused:
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.set_alpha(150)
                    overlay.fill((0, 0, 0))
                    screen.blit(overlay, (0, 0))
                    
                    pause_title = title_font.render(current_lang["pause"], True, (240, 240, 240))
                    screen.blit(pause_title, ((WIDTH - pause_title.get_width()) // 2, HEIGHT // 4))
                    
                    for b in pause_buttons:
                        b.draw(screen, button_font, current_lang)
                
                if game_over:
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.set_alpha(150)
                    overlay.fill((0, 0, 0))
                    screen.blit(overlay, (0, 0))
                    
                    game_over_title = title_font.render(current_lang["game_over"], True, (240, 100, 100))
                    screen.blit(game_over_title, ((WIDTH - game_over_title.get_width()) // 2, HEIGHT // 4))
                    
                    for b in game_over_buttons:
                        b.draw(screen, button_font, current_lang)
                
                pygame.display.flip()
                clock.tick(60)
            
            started = False

    pygame.quit()
    sys.exit()


# SYSTEM JAKOŚCI
def get_scale_from_quality(q):
    if q == "low":
        return 0.4
    return 1.0  # high = pełna jakość, low = lekko rozmazane


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