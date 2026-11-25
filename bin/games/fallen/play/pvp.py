from enum import Enum, auto
import math
import pygame
from pygame.locals import *
from dataclasses import dataclass
from ....saves import Saves as saves
from ....util import Util as util
from PIL import Image, ImageFilter

def blur(surface, radius=5):
    image = Image.frombytes("RGBA", surface.get_size(), pygame.image.tostring(surface, "RGBA"))
    image = image.filter(ImageFilter.GaussianBlur(radius))
    return pygame.image.frombytes(image.tobytes(), image.size, "RGBA")

AMBIENT = blur(util.get_texture(['fallen', 'scenes', 'main_scene']))
ACTIONMSG_WHITE_WIN = util.get_texture(['fallen', 'actionmsg', 'gameover', 'white_win'])
ACTIONMSG_BLACK_WIN = util.get_texture(['fallen', 'actionmsg', 'gameover', 'black_win'])

@dataclass
class Piece:
    isWhite: bool
    x: float
    y: float
    velx: float
    vely: float
    trait_isFallenOff: bool
    hit: bool

class UiState(Enum):
    SelectPiece = auto()
    DirectVelocity1 = auto()
    DirectVelocity2 = auto()
    Idle = auto()

def game():
    screen = pygame.display.set_mode((750, 500))
    clk = pygame.time.Clock()
    finish = False
    pieces = []
    turnIsWhite = False
    boardArea = pygame.Rect(125, 0, 500, 500)
    stats = saves.loadFromSaves()
    font = pygame.font.SysFont(
        ["sans-serif", "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans CJK KR"],
        12
    )

    while not finish:
        for event in pygame.event.get():
            if event.type == QUIT:
                finish = True
            if event.type == KEYUP and event.key == K_ESCAPE:
                finish = True
            if event.type == MOUSEBUTTONUP and event.button == BUTTON_LEFT and boardArea.collidepoint(event.pos):
                pieces.append(Piece(event.pos[1] > 250, event.pos[0] - 125, event.pos[1], 0, 0, False, False))

        mx, my = pygame.mouse.get_pos()
        screen.blit(AMBIENT, (0, 0))
        screen.fill((127, 127, 127), special_flags=BLEND_RGBA_MULT)
        screen.fill((154, 116, 33), boardArea)
        if boardArea.collidepoint(mx, my):
            text = font.render(
                util.get_translation(stats.lang, 'fallen.game.piece.black' if my < 250 else 'fallen.game.piece.white'),
                True,
                (0, 0, 0) if my < 250 else (255, 255, 255)
            )
            screen.blit(text, (mx, my - text.get_height()))

        for sq1 in range(125, 625, 25):
            for sq2 in range(0, 500, 25):
                pygame.draw.rect(screen, (101, 77, 22), (sq1, sq2, 25, 25), width=1)

        for piece in pieces:
            pygame.draw.circle(screen, (255, 255, 255) if piece.isWhite else (0, 0, 0), (round(piece.x + 125), round(piece.y)), 10)

        pygame.display.flip()
        clk.tick(stats.max_fps)

    ui_state = UiState.SelectPiece
    ui_states = {}
    pending_attacks = []
    finish = False

    while not finish:
        for event in pygame.event.get():
            if event.type == QUIT:
                finish = True

            if event.type == KEYUP and event.key == K_ESCAPE:
                finish = True

            if ui_state == UiState.SelectPiece:
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    x, y = event.pos
                    x -= 125

                    for i, piece in enumerate(pieces):
                        if piece.isWhite != turnIsWhite or piece.trait_isFallenOff or piece.hit:
                            continue

                        if (x - piece.x) ** 2 + (y - piece.y) ** 2 < 10 ** 2:
                            ui_states["targi"] = i
                            ui_state = UiState.DirectVelocity1
                            break

            elif ui_state == UiState.DirectVelocity1:
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    x, y = event.pos
                    x -= 125
                    if ((x - pieces[ui_states['targi']].x) ** 2 + (y - pieces[ui_states['targi']].y - 25) ** 2) < (25 ** 2):
                        ui_states['pd1'] = (x, y)
                        ui_state = UiState.DirectVelocity2
                        continue

            elif ui_state == UiState.DirectVelocity2:
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    x, y = event.pos
                    x -= 125
                    if ((x - pieces[ui_states['targi']].x) ** 2 + (y - pieces[ui_states['targi']].y - 25) ** 2) < (25 ** 2):
                        pd2 = (x, y)
                        pieces[ui_states['targi']].velx = pd2[0] - ui_states['pd1'][0]
                        pieces[ui_states['targi']].vely = pd2[1] - ui_states['pd1'][1]
                        ui_state = UiState.Idle
                        ui_states.clear()
                        continue

        stopped = True

        for i, piece in enumerate(pieces):
            piece.x += piece.velx
            piece.y += piece.vely

            piece.velx = (math.floor if piece.velx > 0 else math.ceil)(piece.velx * 0.95)
            piece.vely = (math.floor if piece.vely > 0 else math.ceil)(piece.vely * 0.95)

            if piece.velx:
                stopped = False
            if piece.vely:
                stopped = False

            if not boardArea.collidepoint(round(piece.x + 125), round(piece.y)):
                piece.trait_isFallenOff = True
                piece.velx = 0
                piece.vely = 0

            for other in pieces[i + 1:]:
                dx = other.x - piece.x
                dy = other.y - piece.y
                dist_sq = dx * dx + dy * dy

                if dist_sq < 20 ** 2:
                    if piece.isWhite != other.isWhite:
                        attacker = piece if piece.isWhite == turnIsWhite else other
                        victim = other if attacker is piece else piece

                        if not any(a is attacker and v is victim for a, v in pending_attacks):
                            pending_attacks.append((attacker, victim))

                    dist = math.sqrt(dist_sq) if dist_sq else 0.001
                    nx = dx / dist
                    ny = dy / dist

                    overlap = 20 - dist
                    piece.x -= nx * overlap / 2
                    piece.y -= ny * overlap / 2
                    other.x += nx * overlap / 2
                    other.y += ny * overlap / 2

                    relative_velocity = (other.velx - piece.velx) * nx + (other.vely - piece.vely) * ny

                    if relative_velocity < 0:
                        piece.velx += relative_velocity * nx
                        piece.vely += relative_velocity * ny
                        other.velx -= relative_velocity * nx
                        other.vely -= relative_velocity * ny

        if stopped and ui_state == UiState.Idle:
            turnIsWhite = not turnIsWhite

            replacements = []

            for attacker, victim in pending_attacks:
                if victim.trait_isFallenOff:
                    replacements.append((attacker.x, attacker.y, victim.isWhite))
                    attacker.hit = True
                else:
                    victim.hit = True

            for piece in pieces.copy():
                if piece.trait_isFallenOff or piece.hit:
                    pieces.remove(piece)

            for x, y, isWhite in replacements:
                pieces.append(Piece(isWhite, x, y, 0, 0, False, False))

            pending_attacks.clear()
            ui_state = UiState.SelectPiece

        whitecount = sum(piece.isWhite for piece in pieces)
        blackcount = sum(not piece.isWhite for piece in pieces)
        gameover = not whitecount or not blackcount

        if gameover:
            if whitecount:
                screen.blit(ACTIONMSG_WHITE_WIN, (375 - ACTIONMSG_WHITE_WIN.get_width() // 2, 250 - ACTIONMSG_WHITE_WIN.get_height() // 2))
            if blackcount:
                screen.blit(ACTIONMSG_BLACK_WIN, (375 - ACTIONMSG_BLACK_WIN.get_width() // 2, 250 - ACTIONMSG_BLACK_WIN.get_height() // 2))
            splash_gameover(clk)
            finish = True

        screen.blit(AMBIENT, (0, 0))
        screen.fill((154, 116, 33), boardArea)
        turntext = font.render(
            util.get_translation(stats.lang, 'fallen.game.specifier.turn') + ': ' + util.get_translation(stats.lang, 'fallen.game.piece.white' if turnIsWhite else 'fallen.game.piece.black'),
            True,
            (255, 255, 255) if turnIsWhite else (0, 0, 0)
        )
        screen.blit(turntext, (0, 0))

        for sq1 in range(125, 625, 25):
            for sq2 in range(0, 500, 25):
                pygame.draw.rect(screen, (101, 77, 22), (sq1, sq2, 25, 25), width=1)

        for piece in pieces:
            pygame.draw.circle(screen, (255, 255, 255) if piece.isWhite else (0, 0, 0), (round(piece.x + 125), round(piece.y)), 10)

        if ui_state == UiState.DirectVelocity1 or ui_state == UiState.DirectVelocity2:
            pygame.draw.circle(screen, (255, 0, 0), (pieces[ui_states['targi']].x + 125, pieces[ui_states['targi']].y + 25), 25)
            if ui_state == UiState.DirectVelocity2:
                screen.set_at((ui_states['pd1'][0] + 125, ui_states['pd1'][1]), (0, 0, 255))

        pygame.display.flip()
        clk.tick(stats.max_fps)

def splash_gameover(clk):
    stats = saves.loadFromSaves()
    finish = False
    for _ in range(stats.max_fps * 3):
        for event in pygame.event.get():
            if event.type == QUIT:
                finish = True

        pygame.display.flip()
        clk.tick(stats.max_fps)

        if finish: break