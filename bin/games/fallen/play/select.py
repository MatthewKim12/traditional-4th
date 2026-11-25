from typing import Literal
import pygame
from pygame.locals import *
from ....util import Util as util
from ....saves import Saves as saves
from PIL import Image, ImageFilter

def blur(surface, radius=5):
    image = Image.frombytes("RGBA", surface.get_size(), pygame.image.tostring(surface, "RGBA"))
    image = image.filter(ImageFilter.GaussianBlur(radius))
    return pygame.image.frombytes(image.tobytes(), image.size, "RGBA")

AMBIENT = blur(util.get_texture(['fallen', 'scenes', 'main_scene']))

def select() -> Literal['pvp', 'pve'] | None:
    screen = pygame.display.set_mode((750, 500))
    clk = pygame.time.Clock()
    finish = False
    stats = saves.loadFromSaves()
    pvpBox = pygame.Rect(175, 225, 50, 50)
    pveBox = pygame.Rect(525, 225, 50, 50)
    font = pygame.font.SysFont(
        ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
        64
    )
    font_mid = pygame.font.SysFont(
        ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
        36
    )
    font_small = pygame.font.SysFont(
        ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
        12
    )
    while not finish:
        for event in pygame.event.get():
            if event.type == QUIT:
                finish = True
            if event.type == MOUSEBUTTONUP and event.button == 1 and pvpBox.collidepoint(event.pos):
                return 'pvp'
            if event.type == MOUSEBUTTONUP and event.button == 1 and pveBox.collidepoint(event.pos):
                return 'pve'
        
        screen.blit(AMBIENT, (0, 0))
        title = font.render(
            util.get_translation(stats.lang, 'fallen.play.select.title'), 
            True, 
            (0, 0, 0)
        )
        screen.blit(title, (375 - title.get_width() // 2, 100 - title.get_height() // 2))
        pygame.draw.rect(screen, (0, 127, 255), pvpBox)
        pygame.draw.rect(screen, (0, 127, 255), pveBox)
        pvptext = font_mid.render(util.get_translation(stats.lang, 'fallen.play.pvp'), True, (0, 0, 0))
        pvetext = font_mid.render(util.get_translation(stats.lang, 'fallen.play.pve'), True, (0, 0, 0))
        screen.blit(pvptext, (pvpBox.centerx - pvptext.get_width() // 2, pvpBox.centery - pvptext.get_height() // 2))
        screen.blit(pvetext, (pveBox.centerx - pvetext.get_width() // 2, pveBox.centery - pvetext.get_height() // 2))
        # if pveBox.collidepoint(mx, my):
        #     info = font_small.render(util.get_translation(stats.lang, 'fallen.lock.pve.info'), True, (0, 0, 0))
        #     screen.blit(info, (mx, my - info.get_height()))
        # ^^^^^^^^^^^^^^^^^^^^^^^ PvE now supported

        pygame.display.flip()
        clk.tick(stats.max_fps)