import random
import time
import pygame


class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Calculate resolution scale factor (base resolution is 1280x720)
        base_width = 1280
        base_height = 720
        scale_x = width / base_width
        scale_y = height / base_height
        resolution_scale = (scale_x + scale_y) / 2
        
        # Scale tile size to keep logical map size consistent
        self.tile_size = max(20, int(30 * resolution_scale))
        
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
        # More aggressive scaling for better feel on higher resolutions
        self.move_interval = max(1, int(6 / resolution_scale))
        self.food_eaten = False
        
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
            return True
        
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
                spoil_ratio = min(food_age / self.food_spoil_time, 1.0)
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
        
        grid_color = (100, 120, 80)
        for x in range(start_x, end_x + 1):
            screen_x = (x - camera_x) * self.tile_size
            pygame.draw.line(surface, grid_color, (screen_x, 0), (screen_x, self.height), 1)
        for y in range(start_y, end_y + 1):
            screen_y = (y - camera_y) * self.tile_size
            pygame.draw.line(surface, grid_color, (0, screen_y), (self.width, screen_y), 1)
        
        tree_color = (34, 139, 34)
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
            food_remaining_ratio = max(1 - (food_age / self.food_despawn_time), 0)
            
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
            if self.direction == (1, 0):
                pygame.draw.circle(surface, eye_color, (screen_x + self.tile_size - eye_offset, screen_y + eye_offset), eye_size)
                pygame.draw.circle(surface, eye_color, (screen_x + self.tile_size - eye_offset, screen_y + self.tile_size - eye_offset), eye_size)
                pygame.draw.line(surface, tongue_color, (screen_x + self.tile_size - 2, screen_y + self.tile_size // 2), 
                               (screen_x + self.tile_size + 4, screen_y + self.tile_size // 2), 2)
            elif self.direction == (-1, 0):
                pygame.draw.circle(surface, eye_color, (screen_x + eye_offset, screen_y + eye_offset), eye_size)
                pygame.draw.circle(surface, eye_color, (screen_x + eye_offset, screen_y + self.tile_size - eye_offset), eye_size)
                pygame.draw.line(surface, tongue_color, (screen_x + 2, screen_y + self.tile_size // 2), 
                               (screen_x - 4, screen_y + self.tile_size // 2), 2)
            elif self.direction == (0, 1):
                pygame.draw.circle(surface, eye_color, (screen_x + eye_offset, screen_y + self.tile_size - eye_offset), eye_size)
                pygame.draw.circle(surface, eye_color, (screen_x + self.tile_size - eye_offset, screen_y + self.tile_size - eye_offset), eye_size)
                pygame.draw.line(surface, tongue_color, (screen_x + self.tile_size // 2, screen_y + self.tile_size - 2), 
                               (screen_x + self.tile_size // 2, screen_y + self.tile_size + 4), 2)
            elif self.direction == (0, -1):
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
