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


def draw_hunger_bar(surface, hunger, width, lang_dict):
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
    
    font = pygame.font.SysFont("arial", 18, bold=True)
    label_text = lang_dict["hunger"].upper()
    
    label_x = bar_x + (bar_width) // 2
    label_y = bar_y + (bar_height - 18) // 2
    
    outline_color = (0, 0, 0)
    for offset_x in [-1, 0, 1]:
        for offset_y in [-1, 0, 1]:
            if offset_x != 0 or offset_y != 0:
                outline_label = font.render(label_text, True, outline_color)
                surface.blit(outline_label, (label_x - outline_label.get_width() // 2 + offset_x, label_y + offset_y))
    
    label = font.render(label_text, True, (240, 240, 240))
    surface.blit(label, (label_x - label.get_width() // 2, label_y))
