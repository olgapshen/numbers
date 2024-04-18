import numpy as np
import pandas as pd
from abaqrow import Row

class Abaq():
    def __init__(self, shape, name='a'):
        assert(type(shape) == tuple)
        assert(len(shape) == 2)
        periods = shape[0]
        period = shape[1]
        assert(periods > 0)
        assert(period > 0)
        self.name = name
        self.shape = shape
        self.maxValue = (period ** periods) - 1
        self.rows = [Row(period, name) for i in range(periods)]
        self.stack = []

    def preserve(self):
        state = Abaq(self.shape, self.name)
        assert(state.isEmpty())
        state.apply(self)
        self.stack.append(state)

    def restore(self):
        assert(len(self.stack) > 0)
        state = self.stack.pop()
        self.apply(state)
    
    # Принимаем значение переданной досточки
    def apply(self, abak):
        assert(isinstance(abak, Abaq))
        assert(self is not abak)
        assert(self.shape[0] >= abak.shape[0])
        assert(self.shape[1] == abak.shape[1])
        self.clear()
        self.add(abak)
    
    # Больше чем переданная таблица
    def isBigger(self, abak):
        assert(isinstance(abak, Abaq))
        assert(self is not abak)
        assert(self.shape[1] == abak.shape[1])

        periodSelf = self.shape[0] - 1
        periodOther = abak.shape[0] - 1
        
        while(self.rows[periodSelf].isEmpty() and periodSelf >= 0):
            periodSelf = periodSelf - 1
        while(abak.rows[periodOther].isEmpty() and periodOther >= 0):
            periodOther = periodOther - 1
        
        if (periodSelf < 0 and periodOther < 0):
            return False
        elif (periodSelf > periodOther):
            return True
        elif (periodSelf < periodOther):
            return False
        else:
            rowSelf = self.rows[periodSelf]
            rowOther = abak.rows[periodOther]
            return rowSelf.isBigger(rowOther)

    def isEquals(self, abak):
        assert(isinstance(abak, Abaq))
        assert(self is not abak)
        assert(self.shape[0] >= abak.shape[0])
        assert(self.shape[1] == abak.shape[1])

        for i in range(abak.shape[0]):
            if (not self.rows[i].isEquals(abak.rows[i])):
                return False
        if (self.shape[0] == abak.shape[0]):
            return True
        for j in range(i + 1, self.shape[0]):
            if (self.rows[j].hasItems()):
                return False
        return True
    
    def hasItems(self):
        for i in range(self.shape[0]):
            if (self.rows[i].hasItems()):
                return True
        return False
    
    def isEmpty(self):
        for i in range(self.shape[0]):
            if (self.rows[i].hasItems()):
                return False
        return True

    def clear(self):
        for i in range(self.shape[0]):
            self.rows[i].clear()

    def clearCarry(self):
        for i in range(self.shape[0]):
            self.rows[i].clearCarry()
    
    def push(self):
        i = 0
        self.clearCarry()
        self.rows[i].pushOrCarry()
        while(self.rows[i].isCarry()):
            i = i + 1
            assert(i < self.shape[0])
            self.rows[i].pushOrCarry()
        assert(not self.rows[i].isCarry())
        
    def pop(self):
        i = 0
        self.clearCarry()
        self.rows[i].popOrCarry()
        while(self.rows[i].isCarry()):
            i = i + 1
            assert(i < self.shape[0])
            self.rows[i].popOrCarry()
        assert(not self.rows[i].isCarry())

    # Добавление строки со стороны менее значащих позиций
    def append(self, row):
        assert(type(row) == Row)
        assert(self.shape[1] == row.period)
        self.shl()
        self.rows[0].apply(row)
    
    # Сдвиг влево относительно написания десятичного числа
    # Направление сдвига: от менее значащих разрядов к более значащим
    def shl(self, abak=None):
        if (abak):
            assert(isinstance(abak, Abaq))
            assert(self.shape[0] >= abak.shape[0])
            assert(self.shape[1] == abak.shape[1])

        # Относительно модели стека, самый значащий разряд у нас сверху
        row = self.rows.pop()
        if (abak):
            abak.append(row)

        row.clear()
        self.rows.insert(0, row)

    # Сдвиг вправо относительно написания десятичного числа
    # Направление сдвига: от более значащих разрядов к менее значащим
    def shr(self, abak=None):
        if (abak):
            assert(isinstance(abak, Abaq))
            assert(self.shape[0] >= abak.shape[0])
            assert(self.shape[1] == abak.shape[1])

        # Относительно модели стека, наименее значащий разряд у нас снизу
        row = self.rows.pop(0)
        if (abak):
            abak.append(row)

        row.clear()
        self.rows.append(row)
    
    def add(self, abak):
        assert(isinstance(abak, Abaq))
        assert(self.shape[0] >= abak.shape[0])
        assert(self.shape[1] == abak.shape[1])

        self.clearCarry()
        periods = abak.shape[0]
        isCarry = False
        for i in range(periods):
            if (isCarry):
                # Переход в состояние заёма из состояния нулевого баланса
                self.rows[i].pushOrCarry()
            # Переход в состояние заёма из состояния нулевого баланса
            self.rows[i].add(abak.rows[i])
            isCarry = self.rows[i].isCarry()
        for j in range(i + 1, self.shape[0]):
            if (isCarry):
                self.rows[j].pushOrCarry()
                isCarry = self.rows[j].isCarry()
            else:
                break
        assert(not isCarry)
    
    def sub(self, abak):
        assert(isinstance(abak, Abaq))
        assert(self.shape[0] >= abak.shape[0])
        assert(self.shape[1] == abak.shape[1])
        assert(not abak.isBigger(self))

        self.clearCarry()
        periods = abak.shape[0]
        isCarry = False
        for i in range(periods):
            if (isCarry):
                # Переход в состояние заёма из состояния нулевого баланса
                self.rows[i].popOrCarry()
            # Переход в состояние заёма из состояния нулевого баланса
            self.rows[i].sub(abak.rows[i])
            isCarry = self.rows[i].isCarry()
        for j in range(i + 1, self.shape[0]):
            if (isCarry):
                self.rows[j].popOrCarry()
                isCarry = self.rows[j].isCarry()
            else:
                break
        assert(not isCarry)

    def inc(self, right):
        assert(type(right) == Abaq)
        assert(self.shape[0] >= right.shape[0])
        assert(self.shape[1] == right.shape[1])
        
        # Умножаем большее на меньшее, или возводим в квадрат
        assert(not right.isBigger(self))
        
        state = Abaq(self.shape, self.name)
        assert(state.isEmpty())
        state.apply(self)
        
        right.preserve()
        right.pop()
        while(right.hasItems()):
            self.add(state)
            right.pop()
        right.restore()

    def dec(self, right, rest):
        assert(isinstance(right, Abaq))
        assert(isinstance(rest, Abaq))
        assert(self.shape[0] >= right.shape[0])
        assert(self.shape[1] == right.shape[1])
        assert(self.shape[0] >= rest.shape[0])
        assert(self.shape[1] == rest.shape[1])
        
        # Делим на себя
        if (self.isEquals(right)):
            self.clear()
            self.push()
            return

        # Делим большее на меньшее
        assert(self.isBigger(right))
        
        rest.apply(self)
        self.clear()
        
        while(rest.isBigger(right)):
            rest.sub(right)
            self.push()

        assert(rest.hasItems())
        if (rest.isEquals(right)):
            rest.sub(right)
            self.push() 

    # Записать к себе ранк входного значения
    def rank(self, abak):
        assert(isinstance(abak, Abaq))
        assert(self.shape[0] >= abak.shape[0])
        assert(self.shape[1] == abak.shape[1])

        self.clear()
        periods = abak.shape[0]
        for i in range(periods):
            self.push()
        
        state = Abaq(abak.shape, abak.name)
        abak.preserve()
        while(state.isEmpty()):
            abak.shl(state)
            if (state.isEmpty()):
                self.pop()
        abak.restore()

    
    def toFrame(self):
        rows = self.shape[0]
        cols = self.shape[1] - 1
        table = np.zeros((rows, cols), dtype=int)
        for i in range(rows):
            table[i] = self.rows[i].toArray()
        return pd.DataFrame(
            table,
            columns=[str(i + 1) for i in range(cols)]) 

    def setDecimal(self, num):
        assert(type(num) == int)
        assert(num > 0)
        assert(num <= self.maxValue)

        periods = self.shape[0]
        for i in range(periods):
            self.rows[i].clear()
            
        if (num == 0):
            return

        i = 0
        period = self.shape[1]
        # Ищем граничный период
        while((period ** i) <= num):
            i = i + 1

        for j in reversed(range(i)):
            amount = period ** j
            while((num - amount) >= 0):
                self.rows[j].push()
                num = num - amount

    def getDecimal(self):
        periods = self.shape[0]
        period = self.shape[1]

        num = 0
        for i in range(periods):
            amount = self.rows[i].getDecimal()
            num = num + (period ** i) * amount

        return num