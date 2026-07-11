from dataclasses import dataclass

from model.artista import Artista


@dataclass
class Arco:
    a1: Artista
    a2: Artista
    peso: int
