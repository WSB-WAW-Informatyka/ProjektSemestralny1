import pygame


def get_scale_from_quality(q):
    if q == "low":
        return 0.4
    return 1.0


_original_flip = pygame.display.flip
_cached_small_surf = None
_cached_size = None
_cached_quality = None


def patched_flip(quality_setting):
    global _cached_small_surf, _cached_size, _cached_quality
    
    scale = get_scale_from_quality(quality_setting)

    if scale == 1:
        _original_flip()
        # Clear cache when switching to high quality
        _cached_small_surf = None
        _cached_size = None
        _cached_quality = None
        return

    screen_surf = pygame.display.get_surface()
    w, h = screen_surf.get_size()
    current_size = (w, h)
    
    # Clear cache if quality changed (forces recalculation)
    if quality_setting != _cached_quality:
        _cached_small_surf = None
        _cached_quality = quality_setting
    
    # Recalculate if resolution changed or cache is empty
    if current_size != _cached_size or _cached_small_surf is None:
        _cached_size = current_size
        # Copy the surface to avoid modifying the display surface directly
        screen_copy = screen_surf.copy()
        _cached_small_surf = pygame.transform.smoothscale(screen_copy, (int(w * scale), int(h * scale)))
    
    # Use cached small surface and scale it back up
    if _cached_small_surf is not None:
        big = pygame.transform.scale(_cached_small_surf, (w, h))
        pygame.display.get_surface().blit(big, (0, 0))
    
    pygame.display.update()
