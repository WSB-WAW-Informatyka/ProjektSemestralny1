import sys
import pygame
import random
import time

from config import (
    VERSION, WIDTH, HEIGHT, BG_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR,
    LANG_PL, LANG_EN
)
from game import SnakeGame
from ui import draw_hunger_bar
from assets import load_background, load_game_over_bg, load_sounds
from menus import (
    create_main_buttons, create_settings_buttons, create_quality_buttons,
    create_language_buttons, create_pause_buttons, create_game_over_buttons
)
from quality import patched_flip

current_quality_setting = "high"


def main():
    global current_quality_setting
    
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Giereczka")
    clock = pygame.time.Clock()

    pygame.font.init()
    title_font = pygame.font.SysFont("arial", 72)
    button_font = pygame.font.SysFont("arial", 36)

    background = load_background(WIDTH, HEIGHT)
    game_over_bg = load_game_over_bg(WIDTH, HEIGHT)
    sounds = load_sounds()

    current_lang = LANG_PL

    main_buttons = create_main_buttons(WIDTH, HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    settings_buttons = create_settings_buttons(WIDTH, HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    quality_buttons = create_quality_buttons(WIDTH, HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    language_buttons = create_language_buttons(WIDTH, HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    pause_buttons = create_pause_buttons(WIDTH, HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    game_over_buttons = create_game_over_buttons(WIDTH, HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR)

    current_screen = "main"

    current_quality_setting = "high"

    running = True
    started = False

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
                        if main_buttons[0].is_clicked(event):
                            started = True
                        elif main_buttons[1].is_clicked(event):
                            current_screen = "settings"
                        elif main_buttons[2].is_clicked(event):
                            running = False

                    elif current_screen == "settings":
                        if settings_buttons[0].is_clicked(event):
                            current_screen = "quality"
                        elif settings_buttons[1].is_clicked(event):
                            current_screen = "language"
                        elif settings_buttons[2].is_clicked(event):
                            current_screen = "main"

                    elif current_screen == "quality":
                        if quality_buttons[0].is_clicked(event):
                            current_quality_setting = "low"
                        elif quality_buttons[1].is_clicked(event):
                            current_quality_setting = "high"
                        elif quality_buttons[2].is_clicked(event):
                            current_screen = "settings"

                    elif current_screen == "language":
                        if language_buttons[0].is_clicked(event):
                            current_lang = LANG_PL
                        elif language_buttons[1].is_clicked(event):
                            current_lang = LANG_EN
                        elif language_buttons[2].is_clicked(event):
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

            patched_flip(current_quality_setting)
            clock.tick(60)

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
                        if pause_buttons[0].is_clicked(event):
                            is_paused = False
                            if bgm_channel:
                                bgm_channel.unpause()
                        elif pause_buttons[1].is_clicked(event):
                            pygame.mixer.stop()
                            game = SnakeGame(WIDTH, HEIGHT)
                            game_over = False
                            is_paused = False
                            death_time = None
                            game_over_sound_played = False
                            if bgm_tracks and any(track in sounds for track in bgm_tracks):
                                current_bgm = random.choice([t for t in bgm_tracks if t in sounds])
                                bgm_channel = sounds[current_bgm].play(-1)
                        elif pause_buttons[2].is_clicked(event):
                            pygame.mixer.stop()
                            return_to_menu = True
                    
                    if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                        if game_over_buttons[0].is_clicked(event):
                            pygame.mixer.stop()
                            game = SnakeGame(WIDTH, HEIGHT)
                            game_over = False
                            death_time = None
                            game_over_sound_played = False
                            if bgm_tracks and any(track in sounds for track in bgm_tracks):
                                current_bgm = random.choice([t for t in bgm_tracks if t in sounds])
                                bgm_channel = sounds[current_bgm].play(-1)
                        elif game_over_buttons[1].is_clicked(event):
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
                
                patched_flip(current_quality_setting)
                clock.tick(60)
            
            pygame.mixer.stop()
            
            started = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
