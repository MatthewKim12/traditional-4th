import pygame
from pygame.locals import *
from .games.fallen import main as fallen
from .util import Util as util
from .saves import Saves as saves
from PIL import Image, ImageFilter
pygame.init()

LANG_LIST = ['en_us', 'ko_kr', 'zh_tw']

def blur(surface, radius=5):
    image = Image.frombytes("RGBA", surface.get_size(), pygame.image.tostring(surface, "RGBA"))
    image = image.filter(ImageFilter.GaussianBlur(radius))
    return pygame.image.frombytes(image.tobytes(), image.size, "RGBA")

SCROLL_BG = util.get_texture(['scenes', 'main_scene'])
SCROLL_BG_BLUR = blur(SCROLL_BG, 25)

def main():
    def editSettings(scr):
        font = pygame.font.SysFont(
            ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
            36
        )
        screen = pygame.display.set_mode((750, 500))
        clk = pygame.time.Clock()
        stats = saves.loadFromSaves()
        finish = False
        maxFpsBox = pygame.Rect(25, 25, 325, 50)
        langBox = pygame.Rect(400, 25, 325, 50)
        while not finish:
            for event in pygame.event.get():
                if event.type == QUIT:
                    finish = True
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    if langBox.collidepoint(event.pos):
                        stats.lang = LANG_LIST[(LANG_LIST.index(stats.lang) + 1) % len(LANG_LIST)]

            mx, my = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and maxFpsBox.collidepoint(mx, my):
                stats.max_fps = int((mx - maxFpsBox.left) / maxFpsBox.width * 255)

            scr = (scr + 1) % 750
            screen.blit(SCROLL_BG_BLUR, (scr, 0))
            screen.blit(SCROLL_BG_BLUR, (scr - 750, 0))
            pygame.draw.rect(screen, (255, 127, 0) if maxFpsBox.collidepoint(mx, my) else (127, 64, 0), maxFpsBox)
            max_fps_txt = font.render(
                f'{util.get_translation(stats.lang, 'traditional.fourth.settings.max_fps')}: {stats.max_fps}', 
                True, 
                (255, 255, 255)
            )
            screen.blit(max_fps_txt, (maxFpsBox.centerx - max_fps_txt.get_width() // 2, maxFpsBox.centery - max_fps_txt.get_height() // 2))
            fps_bar = maxFpsBox.left + int(stats.max_fps / 255 * maxFpsBox.width)
            pygame.draw.line(screen, (0, 0, 0), (fps_bar, maxFpsBox.top), (fps_bar, maxFpsBox.bottom))
            pygame.draw.rect(screen, (255, 127, 0) if langBox.collidepoint(mx, my) else (127, 64, 0), langBox)
            langtext = font.render(
                f'{util.get_translation(stats.lang, 'traditional.fourth.settings.lang')}: {util.get_translation(stats.lang, 'traditional.fourth.langname')}', 
                True, 
                (255, 255, 255)
            )
            screen.blit(langtext, (langBox.centerx - langtext.get_width() // 2, langBox.centery - langtext.get_height() // 2))

            pygame.display.flip()
            clk.tick(stats.max_fps)
        saves.saveToFile(stats)
        return scr
    
    font = pygame.font.SysFont(
        ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
        12
    )
    pygame.display.set_caption('Traditional 4th')
    pygame.display.set_icon(util.get_texture(['icon', 'icon']))
    screen = pygame.display.set_mode((750, 500))
    clk = pygame.time.Clock()
    scr = 0
    finish = False
    stats = saves.loadFromSaves()
    fallenBox = pygame.Rect(50, 50, 100, 50)
    settingsBox = pygame.Rect(600, 400, 100, 50)
    while not finish:
        for event in pygame.event.get():
            if event.type == QUIT:
                finish = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if fallenBox.collidepoint(event.pos):
                    fallen.main()
                    stats = saves.loadFromSaves()
                if settingsBox.collidepoint(event.pos):
                    scr = editSettings(scr)
                    stats = saves.loadFromSaves()

        scr = (scr + 1) % 750
        screen.blit(SCROLL_BG, (scr, 0))
        screen.blit(SCROLL_BG, (scr - 750, 0))
        fpstext = font.render(f'{round(clk.get_fps())} FPS/{stats.max_fps} FPS', True, (0, 0, 0))
        screen.blit(fpstext, (0, 0))
        langtext = font.render(util.get_translation(stats.lang, 'traditional.fourth.langname'), True, (0, 0, 0))
        screen.blit(langtext, (750 - langtext.get_width(), 0))
        pygame.draw.rect(screen, (255, 127, 0), fallenBox)
        fallentxt = font.render(util.get_translation(stats.lang, 'fallen.title'), True, (255, 255, 255))
        screen.blit(fallentxt, (fallenBox.centerx - fallentxt.get_width() // 2, fallenBox.centery - fallentxt.get_height() // 2))
        pygame.draw.rect(screen, (127, 64, 0), settingsBox)
        settingtxt = font.render(util.get_translation(stats.lang, 'traditional.fourth.settings'), True, (0, 0, 0))
        screen.blit(settingtxt, (settingsBox.centerx - settingtxt.get_width() // 2, settingsBox.centery - settingtxt.get_height() // 2))

        pygame.display.flip()
        clk.tick(stats.max_fps)
    saves.saveToFile(stats)