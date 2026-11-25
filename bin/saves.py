from dataclasses import dataclass
import pathlib
import copy

@dataclass
class FallenReserves:
    ear: int # Environment Accident Rate

@dataclass
class GeneralGameStatus:
    lang: str
    max_fps: int
    fallen: FallenReserves

_NONEXIST_FALLBACK = GeneralGameStatus('en_us', 60, FallenReserves(10))
PATH = pathlib.Path(__file__).parent.parent / 'saves.dat'

class Saves:
    @staticmethod
    def loadFromSaves() -> GeneralGameStatus:
        if not PATH.exists(): return copy.copy(_NONEXIST_FALLBACK)
        with open(PATH, 'rb') as f:
            return GeneralGameStatus(f.read(5).rstrip(b'\0').decode(), int.from_bytes(f.read(1)), 
                                     FallenReserves(int.from_bytes(f.read(1))))

    @staticmethod
    def saveToFile(status: GeneralGameStatus) -> None:
        with open(PATH, 'wb') as f:
            f.write(status.lang.encode() + int.to_bytes(status.max_fps) + int.to_bytes(status.fallen.ear))