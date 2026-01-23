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
    
    language_button = Button(bx, height // 2, button_w, button_h, "language", button_color, button_hover_color)
    video_button = Button(bx, height // 2 + 100, button_w, button_h, "video", button_color, button_hover_color)
    settings_exit_button = Button(bx, height // 2 + 200, button_w, button_h, "exit", button_color, button_hover_color)
    
    return [language_button, video_button, settings_exit_button]


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


def create_resolution_buttons(width, height, button_color, button_hover_color):
    button_w, button_h = 300, 60
    bx = (width - button_w) // 2
    
    res_720p = Button(bx, height // 2 - 140, button_w, button_h, "720p", button_color, button_hover_color)
    res_800p = Button(bx, height // 2 - 70, button_w, button_h, "800p", button_color, button_hover_color)
    res_900p = Button(bx, height // 2, button_w, button_h, "900p", button_color, button_hover_color)
    res_1080p = Button(bx, height // 2 + 70, button_w, button_h, "1080p", button_color, button_hover_color)
    res_1200p = Button(bx, height // 2 + 140, button_w, button_h, "1200p", button_color, button_hover_color)
    res_exit = Button(bx, height // 2 + 210, button_w, button_h, "exit", button_color, button_hover_color)
    
    return [res_720p, res_800p, res_900p, res_1080p, res_1200p, res_exit]


def create_fullscreen_buttons(width, height, button_color, button_hover_color):
    button_w, button_h = 300, 60
    bx = (width - button_w) // 2
    
    fullscreen_on = Button(bx, height // 2, button_w, button_h, "fullscreen_on", button_color, button_hover_color)
    fullscreen_off = Button(bx, height // 2 + 100, button_w, button_h, "fullscreen_off", button_color, button_hover_color)
    fullscreen_exit = Button(bx, height // 2 + 200, button_w, button_h, "exit", button_color, button_hover_color)
    
    return [fullscreen_on, fullscreen_off, fullscreen_exit]


def create_video_quality_buttons(width, height, button_color, button_hover_color):
    button_w, button_h = 300, 60
    bx = (width - button_w) // 2
    
    quality_low = Button(bx, height // 2, button_w, button_h, "low", button_color, button_hover_color)
    quality_high = Button(bx, height // 2 + 100, button_w, button_h, "high", button_color, button_hover_color)
    quality_exit = Button(bx, height // 2 + 200, button_w, button_h, "exit", button_color, button_hover_color)
    
    return [quality_low, quality_high, quality_exit]


def create_video_menu_buttons(width, height, button_color, button_hover_color):
    button_w, button_h = 300, 60
    bx = (width - button_w) // 2
    
    resolution_button = Button(bx, height // 2 - 70, button_w, button_h, "resolution", button_color, button_hover_color)
    fullscreen_button = Button(bx, height // 2 + 30, button_w, button_h, "fullscreen", button_color, button_hover_color)
    quality_button = Button(bx, height // 2 + 130, button_w, button_h, "quality", button_color, button_hover_color)
    video_exit_button = Button(bx, height // 2 + 230, button_w, button_h, "exit", button_color, button_hover_color)
    
    return [resolution_button, fullscreen_button, quality_button, video_exit_button]
