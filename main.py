import os
import sys
import pygame
import random
import time

class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_size = 30
        self.viewport_width = width // self.tile_size 
        self.viewport_height = height // self.tile_size
        self.grid_width = self.viewport_width * 3 
        self.grid_height = self.viewport_height * 3
        
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.obstacles = self.create_obstacles()
        self.foods = [self.spawn_food() for _ in range(5)]
        self.food_spawn_times = {food: time.time() for food in self.foods}
        self.score = 0
        self.move_counter = 0
        self.move_interval = 5
        self.food_eaten = False
        
        # Głód
        self.hunger = 100
        self.hunger_decay_rate = 0.08
        self.food_spoil_time = 8
        self.food_despawn_time = 15
        self.max_food_value = 40
        self.min_food_value = 10
        
    def create_obstacles(self):
        obstacles = []
        snake_center = (self.grid_width // 2, self.grid_height // 2)
        
        BUSH_PRESETS = [
            [(0, 0), (1, 0)],
            [(0, 0), (0, 1)],
            [(0, 0), (1, 1)],
            [(0, 0), (1, 0), (0, 1), (1, 1)],
            [(0, 0), (1, 0), (2, 0), (1, 1)],
            [(0, 0), (0, 1), (0, 2), (1, 1)],
            [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 0), (1, 0), (-1, 0), (0, 1), (0, 2)],
        ]
        
        WATER_PRESETS = [
            [(0, 0), (1, 0)],
            [(0, 0), (0, 1)],
            [(0, 0), (1, 1)],
            [(0, 0), (1, 0), (0, 1), (1, 1)],
            [(0, 0), (1, 0), (2, 0), (1, 1)],
            [(0, 0), (0, 1), (0, 2), (1, 1)],
            [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (0, 2), (-1, 1), (1, 0)],
        ]
        
        obstacle_set = set(obstacles)
        
        bush_attempts = 0
        max_bush_attempts = 200
        bushes_placed = 0
        
        while bushes_placed < 12 and bush_attempts < max_bush_attempts:
            bush_preset = random.choice(BUSH_PRESETS)
            bush_x = random.randint(10, self.grid_width - 11)
            bush_y = random.randint(10, self.grid_height - 11)
            
            if abs(bush_x - snake_center[0]) > 10 and abs(bush_y - snake_center[1]) > 10:
                too_close = False
                for offset_x, offset_y in bush_preset:
                    nx, ny = bush_x + offset_x, bush_y + offset_y
                    if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                        for existing_x, existing_y in obstacle_set:
                            if abs(nx - existing_x) <= 3 and abs(ny - existing_y) <= 3:
                                too_close = True
                                break
                    if too_close:
                        break
                
                if not too_close:
                    for offset_x, offset_y in bush_preset:
                        nx, ny = bush_x + offset_x, bush_y + offset_y
                        if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height and (nx, ny) not in obstacle_set:
                            obstacle_set.add((nx, ny))
                    
                    bushes_placed += 1
            
            bush_attempts += 1
        
        water_attempts = 0
        max_water_attempts = 200
        water_placed = 0
        
        while water_placed < 10 and water_attempts < max_water_attempts:
            puddle_preset = random.choice(WATER_PRESETS)
            puddle_x = random.randint(10, self.grid_width - 11)
            puddle_y = random.randint(10, self.grid_height - 11)
            
            if abs(puddle_x - snake_center[0]) > 10 and abs(puddle_y - snake_center[1]) > 10:
                too_close = False
                for offset_x, offset_y in puddle_preset:
                    nx, ny = puddle_x + offset_x, puddle_y + offset_y
                    if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                        for existing_x, existing_y in obstacle_set:
                            if abs(nx - existing_x) <= 4 and abs(ny - existing_y) <= 4:
                                too_close = True
                                break
                    if too_close:
                        break
                
                if not too_close:
                    for offset_x, offset_y in puddle_preset:
                        nx, ny = puddle_x + offset_x, puddle_y + offset_y
                        if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height and (nx, ny) not in obstacle_set:
                            obstacle_set.add((nx, ny))
                    
                    water_placed += 1
            
            water_attempts += 1
        
        for river_num in range(3):
            start_pos = random.choice(['left', 'right', 'top', 'bottom'])
            if start_pos == 'left':
                river_x, river_y = 1, random.randint(8, self.grid_height - 9)
                direction = (1, 0)
            elif start_pos == 'right':
                river_x, river_y = self.grid_width - 2, random.randint(8, self.grid_height - 9)
                direction = (-1, 0)
            elif start_pos == 'top':
                river_x, river_y = random.randint(8, self.grid_width - 9), 1
                direction = (0, 1)
            else:
                river_x, river_y = random.randint(8, self.grid_width - 9), self.grid_height - 2
                direction = (0, -1)
            
            river_length = random.randint(20, 40)
            for step in range(river_length):
                river_width = random.randint(1, 2)
                
                if direction[0] != 0:
                    for w in range(river_width):
                        nx, ny = river_x, river_y + w - river_width // 2
                        if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                            if (nx, ny) not in obstacle_set and (abs(nx - snake_center[0]) > 8 or abs(ny - snake_center[1]) > 8):
                                obstacle_set.add((nx, ny))
                else:
                    for w in range(river_width):
                        nx, ny = river_x + w - river_width // 2, river_y
                        if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                            if (nx, ny) not in obstacle_set and (abs(nx - snake_center[0]) > 8 or abs(ny - snake_center[1]) > 8):
                                obstacle_set.add((nx, ny))
                
                river_x += direction[0]
                river_y += direction[1]
                
                if random.random() < 0.1:
                    if direction[0] != 0:
                        new_dy = random.choice([-1, 0, 1])
                        if new_dy != 0:
                            direction = (direction[0], new_dy)
                    else:
                        new_dx = random.choice([-1, 0, 1])
                        if new_dx != 0:
                            direction = (new_dx, direction[1])
                
                river_x = max(1, min(river_x, self.grid_width - 2))
                river_y = max(1, min(river_y, self.grid_height - 2))
        
        obstacles = list(obstacle_set)
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
        self.food_eaten = False
        
        self.hunger -= self.hunger_decay_rate
        if self.hunger < 0:
            self.hunger = 0
        
        if self.hunger <= 0:
            return True  # Śmierć głodowa
        
        foods_to_remove = []
        for food in self.foods:
            if time.time() - self.food_spawn_times[food] >= self.food_despawn_time:
                foods_to_remove.append(food)
        
        for food in foods_to_remove:
            self.foods.remove(food)
            del self.food_spawn_times[food]
        
        while len(self.foods) < 5:
            new_food = self.spawn_food()
            self.foods.append(new_food)
            self.food_spawn_times[new_food] = time.time()
        
        if self.move_counter < self.move_interval:
            return False
        
        self.move_counter = 0
        self.direction = self.next_direction
        
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            return True
        
        if new_head in self.snake:
            return True
        
        if new_head in self.obstacles:
            return True
        
        self.snake.insert(0, new_head)
        
        food_eaten_index = None
        for i, food in enumerate(self.foods):
            if new_head == food:
                self.score += 10
                self.food_eaten = True
                
                food_age = time.time() - self.food_spawn_times[food]
                spoil_ratio = min(food_age / self.food_spoil_time, 1.0)  # 0 to 1
                food_value = self.max_food_value - (self.max_food_value - self.min_food_value) * spoil_ratio
                
                self.hunger = min(self.hunger + food_value, 100)
                
                food_eaten_index = i
                break
        
        if food_eaten_index is not None:
            old_food = self.foods.pop(food_eaten_index)
            del self.food_spawn_times[old_food]
            new_food = self.spawn_food()
            self.foods.append(new_food)
            self.food_spawn_times[new_food] = time.time()
        else:
            self.snake.pop()
        
        return False
    
    def draw(self, surface):
        snake_head_x, snake_head_y = self.snake[0]
        camera_x = snake_head_x - self.viewport_width // 2
        camera_y = snake_head_y - self.viewport_height // 2
        
        camera_x = max(-1, min(camera_x, self.grid_width - self.viewport_width + 1))
        camera_y = max(-1, min(camera_y, self.grid_height - self.viewport_height + 1))
        
        # Kolor podłoża
        ground_color = (110, 145, 65)
        
        start_x = int(camera_x)
        start_y = int(camera_y)
        end_x = int(camera_x + self.viewport_width) + 1
        end_y = int(camera_y + self.viewport_height) + 1
        
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                screen_x = (x - camera_x) * self.tile_size
                screen_y = (y - camera_y) * self.tile_size
                
                if -self.tile_size < screen_x < self.width and -self.tile_size < screen_y < self.height:
                    pygame.draw.rect(surface, ground_color,
                                    (screen_x, screen_y, self.tile_size, self.tile_size))
        
        # Kolor trawy
        grass_color = (80, 120, 40)
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                screen_x = (x - camera_x) * self.tile_size
                screen_y = (y - camera_y) * self.tile_size
                
                if -self.tile_size < screen_x < self.width and -self.tile_size < screen_y < self.height:
                    noise1 = ((x * 73 + y * 97) % 256) / 256.0
                    noise2 = ((x * 151 + y * 163) % 256) / 256.0
                    noise3 = ((x * 211 + y * 227) % 256) / 256.0
                    combined_noise = (noise1 + noise2 * 0.5 + noise3 * 0.25) / 1.75
                    
                    if combined_noise > 0.55:
                        num_tufts = 1 + int(combined_noise * 2)
                        for tuft in range(num_tufts):
                            tuft_seed = (x * 151 + y * 157 + tuft * 163) % 10
                            tuft_x = screen_x + 2 + (tuft_seed * 3) % (self.tile_size - 4)
                            tuft_y = screen_y + 2 + ((tuft_seed * 5) % (self.tile_size - 4))
                            tuft_width = 2 + (tuft_seed % 2)
                            tuft_height = 4 + (tuft_seed % 3)
                            pygame.draw.rect(surface, grass_color, (tuft_x, tuft_y, tuft_width, tuft_height))
        
        boundary_color = (0, 0, 0)
        
        for x in range(int(camera_x) - 2, int(camera_x + self.viewport_width) + 3):
            for y in range(int(camera_y) - 2, int(camera_y + self.viewport_height) + 3):
                is_boundary = (x < 0 or x >= self.grid_width or 
                              y < 0 or y >= self.grid_height)
                
                if is_boundary:
                    screen_x = (x - camera_x) * self.tile_size
                    screen_y = (y - camera_y) * self.tile_size
                    
                    pygame.draw.rect(surface, boundary_color,
                                    (screen_x, screen_y, self.tile_size, self.tile_size))
        
        # Kolor siatki
        grid_color = (100, 120, 80)
        for x in range(start_x, end_x + 1):
            screen_x = (x - camera_x) * self.tile_size
            pygame.draw.line(surface, grid_color, (screen_x, 0), (screen_x, self.height), 1)
        for y in range(start_y, end_y + 1):
            screen_y = (y - camera_y) * self.tile_size
            pygame.draw.line(surface, grid_color, (0, screen_y), (self.width, screen_y), 1)
        
        # Kolory przeszkód
        tree_color = (34, 139, 34) # na razie niewykorzystane
        bush_color = (85, 107, 47)
        water_color = (65, 105, 225)
        
        for obs in self.obstacles:
            screen_x = (obs[0] - camera_x) * self.tile_size
            screen_y = (obs[1] - camera_y) * self.tile_size
            if -self.tile_size < screen_x < self.width and -self.tile_size < screen_y < self.height:
                color_hash = (obs[0] + obs[1]) % 3
                if color_hash == 0:
                    color = tree_color
                elif color_hash == 1:
                    color = bush_color
                else:
                    color = water_color
                
                pygame.draw.rect(surface, color,
                               (screen_x + 1, screen_y + 1,
                                self.tile_size - 2, self.tile_size - 2))
        
        food_color = (255, 200, 0)
        for food in self.foods:
            food_age = time.time() - self.food_spawn_times[food]
            food_remaining_ratio = max(1 - (food_age / self.food_despawn_time), 0)  # 1 to 0
            
            max_food_size = self.tile_size - 4
            current_food_size = max_food_size * food_remaining_ratio
            offset = (max_food_size - current_food_size) / 2
            
            if current_food_size > 0:
                screen_x = (food[0] - camera_x) * self.tile_size
                screen_y = (food[1] - camera_y) * self.tile_size
                if -self.tile_size < screen_x < self.width and -self.tile_size < screen_y < self.height:
                    pygame.draw.rect(surface, food_color,
                                    (screen_x + 2 + offset, 
                                     screen_y + 2 + offset,
                                     current_food_size, current_food_size))
        
        snake_color = (100, 255, 100)
        head_color = (150, 255, 150)
        eye_color = (0, 0, 0)
        tongue_color = (255, 100, 100)
        
        head = self.snake[0]
        screen_x = (head[0] - camera_x) * self.tile_size
        screen_y = (head[1] - camera_y) * self.tile_size
        if -self.tile_size < screen_x < self.width and -self.tile_size < screen_y < self.height:
            pygame.draw.rect(surface, head_color,
                            (screen_x + 1, screen_y + 1,
                             self.tile_size - 2, self.tile_size - 2))
            
            eye_size = 3
            eye_offset = 7
            if self.direction == (1, 0):  # Prawo
                pygame.draw.circle(surface, eye_color, (screen_x + self.tile_size - eye_offset, screen_y + eye_offset), eye_size)
                pygame.draw.circle(surface, eye_color, (screen_x + self.tile_size - eye_offset, screen_y + self.tile_size - eye_offset), eye_size)
                pygame.draw.line(surface, tongue_color, (screen_x + self.tile_size - 2, screen_y + self.tile_size // 2), 
                               (screen_x + self.tile_size + 4, screen_y + self.tile_size // 2), 2)
            elif self.direction == (-1, 0):  # Lewo
                pygame.draw.circle(surface, eye_color, (screen_x + eye_offset, screen_y + eye_offset), eye_size)
                pygame.draw.circle(surface, eye_color, (screen_x + eye_offset, screen_y + self.tile_size - eye_offset), eye_size)
                pygame.draw.line(surface, tongue_color, (screen_x + 2, screen_y + self.tile_size // 2), 
                               (screen_x - 4, screen_y + self.tile_size // 2), 2)
            elif self.direction == (0, 1):  # Dół
                pygame.draw.circle(surface, eye_color, (screen_x + eye_offset, screen_y + self.tile_size - eye_offset), eye_size)
                pygame.draw.circle(surface, eye_color, (screen_x + self.tile_size - eye_offset, screen_y + self.tile_size - eye_offset), eye_size)
                pygame.draw.line(surface, tongue_color, (screen_x + self.tile_size // 2, screen_y + self.tile_size - 2), 
                               (screen_x + self.tile_size // 2, screen_y + self.tile_size + 4), 2)
            elif self.direction == (0, -1):  # Góra
                pygame.draw.circle(surface, eye_color, (screen_x + eye_offset, screen_y + eye_offset), eye_size)
                pygame.draw.circle(surface, eye_color, (screen_x + self.tile_size - eye_offset, screen_y + eye_offset), eye_size)
                pygame.draw.line(surface, tongue_color, (screen_x + self.tile_size // 2, screen_y + 2), 
                               (screen_x + self.tile_size // 2, screen_y - 4), 2)
        
        for segment in self.snake[1:]:
            screen_x = (segment[0] - camera_x) * self.tile_size
            screen_y = (segment[1] - camera_y) * self.tile_size
            if -self.tile_size < screen_x < self.width and -self.tile_size < screen_y < self.height:
                pygame.draw.rect(surface, snake_color,
                               (screen_x + 1, screen_y + 1,
                                self.tile_size - 2, self.tile_size - 2))


def draw_hunger_bar(surface, hunger, width, lang_dict):
    """Draw a hunger bar at the bottom center of the screen"""
    bar_width = 400
    bar_height = 30
    bar_x = (width - bar_width) // 2
    bar_y = 680
    
    pygame.draw.rect(surface, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    
    fill_width = (hunger / 100) * bar_width
    
    if hunger > 50:
        color = (0, 255, 0)
    elif hunger > 25:
        color = (255, 200, 0)
    else:
        color = (255, 0, 0)
    
    pygame.draw.rect(surface, color, (bar_x, bar_y, fill_width, bar_height))
    
    pygame.draw.rect(surface, (240, 240, 240), (bar_x, bar_y, bar_width, bar_height), 2)
    
    font = pygame.font.SysFont("arial", 16, bold=True)
    label_text = lang_dict["hunger"].upper()
    label = font.render(label_text, True, (240, 240, 240))
    
    label_x = bar_x + (bar_width - label.get_width()) // 2
    label_y = bar_y + (bar_height - label.get_height()) // 2
    
    outline_color = (0, 0, 0)
    for offset_x in [-2, 2]:
        for offset_y in [-2, 2]:
            outline_label = font.render(label_text, True, outline_color)
            surface.blit(outline_label, (label_x + offset_x, label_y + offset_y))
    
    surface.blit(label, (label_x, label_y))


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
    pygame.mixer.init()

    VERSION: str = "0.7"

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

    game_over_bg = None
    game_over_bg_candidates = [
        os.path.join(base_dir, "assets", "game_over.png"),
        os.path.join(base_dir, "game_over.png"),
    ]
    for path in game_over_bg_candidates:
        if not os.path.isfile(path):
            continue
        try:
            img = pygame.image.load(path)
            game_over_bg = pygame.transform.smoothscale(img.convert_alpha(), (WIDTH, HEIGHT))
            print(f"Loaded game over background: {path}")
            break
        except Exception as e:
            print(f"Failed to load game over background '{path}': {e}")
            continue

    sounds = {}
    audio_files = {
        "explosion": "explosion.mp3",
        "game_over": "game_over.mp3",
        "score": "score.mp3",
        "bgm01": "bgm01.mp3",
        "bgm02": "bgm02.mp3",
        "bgm03": "bgm03.mp3",
    }
    
    for sound_name, filename in audio_files.items():
        audio_candidates = [
            os.path.join(base_dir, "assets", filename),
            os.path.join(base_dir, filename),
        ]
        for path in audio_candidates:
            if not os.path.isfile(path):
                continue
            try:
                sounds[sound_name] = pygame.mixer.Sound(path)
                print(f"Loaded sound: {sound_name} from {path}")
                break
            except Exception as e:
                print(f"Failed to load sound '{filename}': {e}")
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
        "retry": "Ponów",
        "score": "Wynik",
        "hunger": "Głód"
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
        "retry": "Retry",
        "score": "Score",
        "hunger": "Hunger"
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
            death_time = None
            game_over_sound_played = False
            current_bgm = None
            bgm_channel = None
            bgm_tracks = ["bgm01", "bgm02", "bgm03"]
            
            if bgm_tracks and any(track in sounds for track in bgm_tracks):
                current_bgm = random.choice([t for t in bgm_tracks if t in sounds])
                bgm_channel = sounds[current_bgm].play(-1)
            
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
                            if bgm_channel:
                                bgm_channel.pause()
                        elif not is_paused and not game_over:
                            game.handle_input(event)
                    
                    if is_paused and event.type == pygame.MOUSEBUTTONDOWN:
                        if pause_continue.is_clicked(event):
                            is_paused = False
                            if bgm_channel:
                                bgm_channel.unpause()
                        elif pause_restart.is_clicked(event):
                            pygame.mixer.stop()
                            game = SnakeGame(WIDTH, HEIGHT)
                            game_over = False
                            is_paused = False
                            death_time = None
                            game_over_sound_played = False
                            if bgm_tracks and any(track in sounds for track in bgm_tracks):
                                current_bgm = random.choice([t for t in bgm_tracks if t in sounds])
                                bgm_channel = sounds[current_bgm].play(-1)
                        elif pause_menu.is_clicked(event):
                            pygame.mixer.stop()
                            return_to_menu = True
                    
                    if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                        if game_over_retry.is_clicked(event):
                            pygame.mixer.stop()
                            game = SnakeGame(WIDTH, HEIGHT)
                            game_over = False
                            death_time = None
                            game_over_sound_played = False
                            if bgm_tracks and any(track in sounds for track in bgm_tracks):
                                current_bgm = random.choice([t for t in bgm_tracks if t in sounds])
                                bgm_channel = sounds[current_bgm].play(-1)
                        elif game_over_menu.is_clicked(event):
                            pygame.mixer.stop()
                            return_to_menu = True
                
                if not is_paused and not game_over:
                    game_over = game.update()
                    
                    if game.food_eaten and "score" in sounds:
                        sounds["score"].play()
                    
                    if game_over:
                        if bgm_channel:
                            bgm_channel.stop()
                        if "explosion" in sounds:
                            sounds["explosion"].play()
                        death_time = time.time()
                
                if game_over and death_time is not None and (time.time() - death_time) < 2:
                    game.draw(screen)
                    score_font = pygame.font.SysFont("arial", 36)
                    score_surf = score_font.render(f"{current_lang['score']}: {game.score}", True, (240, 240, 240))
                    screen.blit(score_surf, (20, 20))
                    
                    draw_hunger_bar(screen, game.hunger, WIDTH, current_lang)
                elif game_over and death_time is not None and (time.time() - death_time) >= 2:
                    if game_over_bg:
                        screen.blit(game_over_bg, (0, 0))
                    else:
                        overlay = pygame.Surface((WIDTH, HEIGHT))
                        overlay.set_alpha(150)
                        overlay.fill((0, 0, 0))
                        screen.blit(overlay, (0, 0))
                    
                    if "game_over" in sounds and not game_over_sound_played:
                        sounds["game_over"].play()
                        game_over_sound_played = True
                    
                    game_over_title = title_font.render(current_lang["game_over"], True, (240, 100, 100))
                    screen.blit(game_over_title, ((WIDTH - game_over_title.get_width()) // 2, HEIGHT // 4))
                    
                    for b in game_over_buttons:
                        b.draw(screen, button_font, current_lang)
                else:
                    game.draw(screen)
                    
                    score_font = pygame.font.SysFont("arial", 36)
                    score_surf = score_font.render(f"{current_lang['score']}: {game.score}", True, (240, 240, 240))
                    screen.blit(score_surf, (20, 20))
                    
                    draw_hunger_bar(screen, game.hunger, WIDTH, current_lang)
                    
                    if is_paused:
                        overlay = pygame.Surface((WIDTH, HEIGHT))
                        overlay.set_alpha(150)
                        overlay.fill((0, 0, 0))
                        screen.blit(overlay, (0, 0))
                        
                        pause_title = title_font.render(current_lang["pause"], True, (240, 240, 240))
                        screen.blit(pause_title, ((WIDTH - pause_title.get_width()) // 2, HEIGHT // 4))
                        
                        for b in pause_buttons:
                            b.draw(screen, button_font, current_lang)
                
                pygame.display.flip()
                clock.tick(60)
            
            pygame.mixer.stop()
            
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