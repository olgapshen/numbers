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

        cell = Abaq(self.shape, self.name)
        rest = Abaq(self.shape, self.name)
        state = Abaq(self.shape, self.name)
        reg = Abaq(self.shape, self.name)

        #print('----')
        #print(self.getDecimal())
        #print(cell.getDecimal())
        #print(abak.getDecimal())
        #print(state.getDecimal())
        
        self.preserve()
        while(self.hasItems()):
            while(abak.isBigger(cell)):
                self.shl(cell)
    
            print('----')
            print('self: ' + str(self.getDecimal()))
            print('cell: ' + str(cell.getDecimal()))
            print('rest: ' + str(rest.getDecimal()))
            print('abak: ' + str(abak.getDecimal()))
            print('state: ' + str(state.getDecimal()))
            print('reg: ' + str(reg.getDecimal()))

            cell.dec(abak, rest)
            reg.shl()
            reg.add(cell)

            print('----')
            print('self: ' + str(self.getDecimal()))
            print('cell: ' + str(cell.getDecimal()))
            print('rest: ' + str(rest.getDecimal()))
            print('abak: ' + str(abak.getDecimal()))
            print('state: ' + str(state.getDecimal()))
            print('reg: ' + str(reg.getDecimal()))
        
        self.restore()
        
        #abak.preserve()
        #abak.shr(cell)
        #self.inc(cell)

        #while(abak.hasItems()):
        #    self.preserve()
        #    state.shl()
        #    self.apply(state)
        #    abak.shr(cell)            
        #    self.inc(cell)

        #abak.restore()
        #abak.preserve()

        #state.apply(self)
        #cell.clear()        
        #abak.shr(cell)
        
        #while(abak.hasItems()):
        #    self.restore()
        #    state.add(self)
        #    abak.shr(cell)

        #self.apply(state)
        #abak.restore()