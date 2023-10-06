from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.processors.abstract_core import AbstractCore

from m5.objects import SubSystem, RubySystem

from .MeshDescriptor import Coordinate
from .Tile import Tile

class CoreTile(Tile):
    def __init__(self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        core: AbstractCore,
        l1i_size: str,
        l1i_associativity: int,
        l1d_size: str,
        l1d_associativity: int,
        l2_size: str,
        l2_associativity: int,
        coordinate: Coordinate
    ) -> None:
        Tile.__init__(self=self, board=board, ruby_system=ruby_system, cache_line_size=board.cache_line_size)

        self._board = board
        self._core = core
        self._l1i_size = l1i_size
        self._l1i_associativity = l1i_associativity
        self._l1d_size = l1d_size
        self._l1d_associativity = l1d_associativity
        self._l2_size = l2_size
        self._l2_associativity = l2_associativity
        self._coordinate = coordinate
