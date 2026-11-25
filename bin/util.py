import json
from pathlib import Path
from typing import Iterable
import pygame

class Util:
    @staticmethod
    def get_translation(lang: str, key: str) -> str:
        langdir = Path(__file__).parent / 'assets' / 'lang'
        with open(langdir / (lang + '.json'), 'r', encoding = 'utf-8') as f:
            return json.load(f).get(key, key)

    @staticmethod
    def get_texture(path: Iterable[str]) -> pygame.Surface:
        texture = Path(__file__).parent / 'assets' / 'textures'
        for part in path:
            texture /= part
        texture = texture.parent / (path[-1] + '.png')
        return pygame.image.load(texture)