import pygame
from pygame.locals import *
from ....saves import Saves as saves
from ....util import Util as util
import pathlib

LANG_LIST = ['en_us', 'ko_kr', 'zh_tw']

def checkbox(screen: pygame.Surface):
    font = pygame.font.SysFont(
        ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
        24
    )
    clk = pygame.time.Clock()
    finish = False
    stats = saves.loadFromSaves()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                finish = True
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    stats.lang = LANG_LIST[LANG_LIST.index(stats.lang) - 1]
                    # doesn't need the funky modulo thingy, -1 is the last index
                elif event.key == K_RIGHT:
                    stats.lang = LANG_LIST[(LANG_LIST.index(stats.lang) + 1) % len(LANG_LIST)]
            elif event.type == MOUSEWHEEL:
                stats.lang = LANG_LIST[(LANG_LIST.index(stats.lang) + event.y) % len(LANG_LIST)]

        pygame.draw.rect(screen, (255, 255, 255), (250, 125, 250, 250))
        name = font.render(util.get_translation(stats.lang, 'fallen.checkbox.lang.name'), True, (0, 0, 0))
        screen.blit(name, (375 - name.get_width() / 2, 175 - name.get_height() / 2))
        langname = font.render(util.get_translation(stats.lang, 'traditional.fourth.langname'), True, (0, 0, 0))
        screen.blit(langname, (375 - langname.get_width() / 2, 350 - langname.get_height() / 2))

        pygame.display.flip()
        clk.tick(stats.max_fps)

        if finish:
            break
    saves.saveToFile(stats)