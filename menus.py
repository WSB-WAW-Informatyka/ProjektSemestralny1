import pygame
from ui import Button


def create_main_buttons(width, height, button_color, button_hover_color):
    button_w, button_h = 300, 60
    bx = (width - button_w) // 2
    
    start_button = Button(bx, height // 2, button_w, button_h, "start", button_color, button_hover_color)
    settings_button = Button(bx, height // 2 + 100, button_w, button_h, "settings", button_color, button_hover_color)
    quit_button = Button(bx, height // 2 + 200, button_w, button_h, "quit", button_color, button_hover_color)
    
    return [start_button, settings_button, quit_button]


def create_settings_buttons(width, height, button_color, button_hover_color):
    button_w, button_h = 300, 60
    bx = (width - button_w) // 2
    
    quality_button = Button(bx, height // 2, button_w, button_h, "quality", button_color, button_hover_color)
    language_button = Button(bx, height // 2 + 100, button_w, button_h, "language", button_color, button_hover_color)
    settings_exit_button = Button(bx, height // 2 + 200, button_w, button_h, "exit", button_color, button_hover_color)
    
    return [quality_button, language_button, settings_exit_button]


def create_quality_buttons(width, height, button_color, button_hover_color):
    button_w, button_h = 300, 60
    bx = (width - button_w) // 2
    
    quality_low = Button(bx, height // 2, button_w, button_h, "low", button_color, button_hover_color)
    quality_high = Button(bx, height // 2 + 100, button_w, button_h, "high", button_color, button_hover_color)
    quality_exit = Button(bx, height // 2 + 200, button_w, button_h, "exit", button_color, button_hover_color)
    
    return [quality_low, quality_high, quality_exit]


def create_language_buttons(width, height, button_color, button_hover_color):
    button_w, button_h = 300, 60
    bx = (width - button_w) // 2
    
    lang_pl_btn = Button(bx, height // 2, button_w, button_h, "pl", button_color, button_hover_color)
    lang_en_btn = Button(bx, height // 2 + 100, button_w, button_h, "en", button_color, button_hover_color)
    lang_exit_btn = Button(bx, height // 2 + 200, button_w, button_h, "exit", button_color, button_hover_color)
    
    return [lang_pl_btn, lang_en_btn, lang_exit_btn]


def create_pause_buttons(width, height, button_color, button_hover_color):
    button_w, button_h = 300, 60
    bx = (width - button_w) // 2
    
    pause_continue = Button(bx, height // 2, button_w, button_h, "continue", button_color, button_hover_color)
    pause_restart = Button(bx, height // 2 + 100, button_w, button_h, "restart", button_color, button_hover_color)
    pause_menu = Button(bx, height // 2 + 200, button_w, button_h, "main_menu", button_color, button_hover_color)
    
    return [pause_continue, pause_restart, pause_menu]


def create_game_over_buttons(width, height, button_color, button_hover_color):
    button_w, button_h = 300, 60
    bx = (width - button_w) // 2
    
    game_over_retry = Button(bx, height // 2, button_w, button_h, "retry", button_color, button_hover_color)
    game_over_menu = Button(bx, height // 2 + 100, button_w, button_h, "main_menu", button_color, button_hover_color)
    
    return [game_over_retry, game_over_menu]
