import pygame
from pygame.locals import *
from ....saves import Saves as saves
from ....util import Util as util

def checkbox(screen: pygame.Surface) -> None:
    font = pygame.font.SysFont(
        ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
        24
    )
    font_small = pygame.font.SysFont(
        ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
        12
    )
    clk = pygame.time.Clock()
    finish = False
    stats = saves.loadFromSaves()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                finish = True

        if pygame.mouse.get_pressed()[0]:
            xclamp = min(490, max(260, pygame.mouse.get_pos()[0]))
            stats.fallen.ear = round(1 + 44 * (xclamp - 260) / 230)

        pygame.draw.rect(screen, (255, 255, 255), (250, 125, 250, 250))
        name = font.render(util.get_translation(stats.lang, 'fallen.checkbox.ear.name'), True, (0, 0, 0))
        screen.blit(name, (375 - name.get_width() / 2, 175 - name.get_height() / 2))
        pygame.draw.rect(screen, (127, 127, 127), (260, 200, 230, 25))
        linepos = round(260 + 230 * (stats.fallen.ear - 1) / 44)
        pygame.draw.line(screen, (255, 0, 0), (linepos, 175), (linepos, 250))
        fpstext = font_small.render(f'{stats.fallen.ear}', True, (0, 0, 0))
        screen.blit(fpstext, (375 - fpstext.get_width() / 2, round(162.5 - fpstext.get_height() / 2)))

        pygame.display.flip()
        clk.tick(stats.max_fps)

        if finish:
            break
    saves.saveToFile(stats)