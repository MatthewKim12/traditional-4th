import pygame
from pygame.locals import *
from ...util import Util as util
from ...saves import Saves as saves
from .checkbox.fps import checkbox as checkbox_fps
from .checkbox.lang import checkbox as checkbox_lang
from .checkbox.ear import checkbox as checkbox_ear
from .play.select import select
from .play.pvp import game as pvp
from .play.pve import game as pve

MAIN_SCENE = util.get_texture(['fallen', 'scenes', 'main_scene'])

def main():
    screen = pygame.display.set_mode((750, 500))
    clk = pygame.time.Clock()
    font = pygame.font.SysFont(
        ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
        64
    )
    font_small = pygame.font.SysFont(
        ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
        12
    )
    stats = saves.loadFromSaves()
    finish = False
    hitbox_fps_btn = pygame.Rect(675, 450, 50, 50)
    hitbox_lang_btn = pygame.Rect(0, 0, 50, 50)
    hitbox_start_btn = pygame.Rect(120, 400, 50, 50)
    hitbox_ear_btn = pygame.Rect(150, 20, 50, 50)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                finish = True
            if event.type == MOUSEBUTTONUP and event.button == BUTTON_LEFT:
                if hitbox_fps_btn.collidepoint(event.pos):
                    checkbox_fps(screen)
                    stats = saves.loadFromSaves()
                elif hitbox_lang_btn.collidepoint(event.pos):
                    checkbox_lang(screen)
                    stats = saves.loadFromSaves()
                elif hitbox_ear_btn.collidepoint(event.pos):
                    checkbox_ear(screen)
                    stats = saves.loadFromSaves()
                elif hitbox_start_btn.collidepoint(event.pos):
                    mode = select()
                    if mode is not None:
                        if mode == 'pvp':
                            pvp()
                        elif mode == 'pve':
                            pve()

        screen.blit(MAIN_SCENE, (0, 0))
        title = font.render(util.get_translation(stats.lang, 'fallen.title'), True, (149, 52, 9))
        title = pygame.transform.rotate(title, 30)
        screen.blit(title, (500 - title.get_width() / 2, 150 - title.get_height() / 2))
        fps = font_small.render(f'{int(clk.get_fps())} FPS', True, (255, 255, 255))
        screen.blit(fps, (714 - fps.get_width() / 2, 477 - fps.get_height() / 2))
        lang = font_small.render(util.get_translation(stats.lang, 'traditional.fourth.langname'), True, (255, 255, 255))
        screen.blit(lang, (40 - lang.get_width() / 2, 32 - lang.get_height() / 2))
        start_btn = font_small.render(util.get_translation(stats.lang, 'fallen.button.start'), True, (255, 255, 255))
        screen.blit(start_btn, (145 - start_btn.get_width() / 2, 425 - start_btn.get_height() / 2))
        pygame.draw.circle(screen, (255, 255, 255), hitbox_ear_btn.center, hitbox_ear_btn.height // 2)
        ear_txt = font_small.render(util.get_translation(stats.lang, 'fallen.setting.ear.name'), True, (255, 255, 255))
        screen.blit(ear_txt, (hitbox_ear_btn.centerx - ear_txt.get_width() // 2, hitbox_ear_btn.bottom + 10))

        pygame.display.flip()
        clk.tick(stats.max_fps)

        if finish:
            break
    saves.saveToFile(stats)