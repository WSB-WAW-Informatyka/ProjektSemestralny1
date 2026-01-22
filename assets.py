import os
import pygame


def load_background(width, height):
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
            background = pygame.transform.smoothscale(img.convert_alpha(), (width, height))
            print(f"Loaded background (pygame): {path}")
            break
        except Exception as e:
            print(f"pygame failed to load '{path}': {e}")
            try:
                from PIL import Image
                pil = Image.open(path).convert("RGBA")
                data = pil.tobytes()
                surf = pygame.image.frombuffer(data, pil.size, "RGBA")
                background = pygame.transform.smoothscale(surf.convert_alpha(), (width, height))
                print(f"Loaded background via Pillow: {path}")
                break
            except Exception as e2:
                print(f"Pillow fallback also failed for '{path}': {e2}")
                background = None
                continue
    
    return background


def load_game_over_bg(width, height):
    base_dir = os.path.dirname(__file__)
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
            game_over_bg = pygame.transform.smoothscale(img.convert_alpha(), (width, height))
            print(f"Loaded game over background: {path}")
            break
        except Exception as e:
            print(f"Failed to load game over background '{path}': {e}")
            continue
    
    return game_over_bg


def load_sounds():
    base_dir = os.path.dirname(__file__)
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
    
    return sounds
