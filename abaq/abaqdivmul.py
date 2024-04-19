import numpy as np
import pandas as pd
from abaq import Abaq

class DivMul(Abaq):
    def mul(self, abak):
        assert(isinstance(abak, Abaq))
        assert(self.shape[0] >= abak.shape[0])
        assert(self.shape[1] == abak.shape[1])

        # Умножаем большее на меньшее, или возводим в квадрат
        assert(not abak.isBigger(self))

        shape = (1, self.shape[1])
        cell = Abaq(shape, self.name)
        state = Abaq(self.shape, self.name)
        state.apply(self)

        abak.preserve()
        abak.shr(cell)
        self.inc(cell)

        while(abak.hasItems()):
            self.preserve()
            state.shl()
            self.apply(state)
            cell.clear()
            abak.shr(cell)
            self.inc(cell)

        abak.restore()
        abak.preserve()

        state.apply(self)
        cell.clear()
        abak.shr(cell)

        while(abak.hasItems()):
            self.restore()
            state.add(self)
            abak.shr(cell)

        self.apply(state)
        abak.restore()

    def div(self, abak, rest):
        assert(isinstance(abak, Abaq))
        assert(isinstance(rest, Abaq))
        assert(self.shape[0] >= abak.shape[0])
        assert(self.shape[1] == abak.shape[1])
        assert(self.shape[0] >= rest.shape[0])
        assert(self.shape[1] == rest.shape[1])

        # Делим большее на меньшее, или на себя
        assert(not abak.isBigger(self))

        rank = Abaq(self.shape, self.name)
        cell = Abaq(self.shape, self.name)
        state = Abaq(self.shape, self.name)

        rank.rank(self)
        self.preserve()
        while(rank.hasItems()):
            while(abak.isBigger(cell)):
                self.shl(cell)
                rank.pop()

            cell.dec(abak, rest)
            state.shl()
            state.add(cell)
            cell.apply(rest)

        self.restore()
        self.apply(state)
