import pygame


def get_scale_from_quality(q):
    if q == "low":
        return 0.4
    return 1.0


_original_flip = pygame.display.flip


def patched_flip(quality_setting):
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
