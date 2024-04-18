import numpy as np
import pandas as pd

class Row():
    def __init__(self, period, name='a'):
        # Размер порядка системы счисления
        # Для десятичной системы нужно передать число 10
        # При этом максимальное количество элементов будет 9
        self.period = period
        self.data = []
        self.stack = []
        self.carry = False
        self.name = name

    def preserve(self):
        self.stack.append(self.data.copy())

    def restore(self):
        assert(len(self.stack) > 0)
        self.data = self.stack.pop()
    
    def hasItems(self):
        assert(len(self.data) < self.period)
        # Длина по идее не может быть меньше нуля
        # Стоит проверять только в случае, если длина
        # ожидается более нуля
        # assert(len(self.data) >= 0)        
        return len(self.data) > 0

    def hasSpace(self):
        assert(len(self.data) < self.period)
        # assert(len(self.data) >= 0)        
        return len(self.data) < self.period - 1
    
    def isEmpty(self):
        assert(len(self.data) < self.period)
        return len(self.data) == 0

    def isFull(self):
        assert(len(self.data) < self.period)
        return len(self.data) == self.period - 1

    def isCarry(self):
        return self.carry
    
    # Больше чем переданная строка
    def isBigger(self, row):
        assert(type(row) == Row)
        assert(self is not row)
        assert(self.period == row.period)

        row.clearCarry()
        row.preserve()
        row.sub(self)
        row.restore()

        return row.isCarry()

    def isEquals(self, row):
        assert(type(row) == Row)
        assert(self is not row)
        assert(self.period == row.period)

        row.clearCarry()
        row.preserve()
        row.sub(self)
        row.restore()

        if (row.isCarry()):
            return False

        self.clearCarry()
        self.preserve()
        self.sub(row)
        self.restore()

        return not self.isCarry()
    
    def clear(self):
        self.data.clear()
        self.carry = False

    def clearCarry(self):
        self.carry = False
    
    def fill(self):
        assert(len(self.data) < self.period)
        assert(not self.carry)
        self.carry = True
        while(not self.isFull()):
            self.data.append(1)

    def take(self):
        assert(len(self.data) < self.period)
        assert(not self.carry)
        self.carry = True
        self.data.clear()

    def apply(self, row):
        assert(type(row) == Row)
        assert(self is not row)
        assert(self.period == row.period)

        self.clear()
        row.preserve()
        while(row.hasItems()):
            row.pop()
            self.push()
        row.restore()

    def push(self):
        assert(len(self.data) < self.period - 1)
        self.data.append(1)
    
    def pop(self):
        assert(len(self.data) < self.period)
        assert(len(self.data) > 0)
        # На счётах могут быть только камушки
        assert(self.data.pop() == 1)

    def pushOrCarry(self):
        assert(len(self.data) < self.period)
        assert(not self.carry)

        if (self.hasSpace()):
            self.push()
        else:
            self.take()
    
    def popOrCarry(self):
        assert(len(self.data) < self.period)
        assert(not self.carry)

        if (self.hasItems()):
            self.pop()
        else:
            self.fill()

    # Эта операция может произойти в состоянии заёма
    # При повторном заёме произойдёт ошибка
    def add(self, row):
        assert(type(row) == Row)
        assert(self is not row)
        assert(self.period == row.period)
        assert(len(self.data) < self.period)

        if (row.isEmpty()):
            return
        
        row.preserve()
        while(row.hasItems()):
            row.pop()
            if (self.isFull()):
                self.take()
            else:
                self.push()
        row.restore()

    # Эта операция может произойти в состоянии заёма
    # При повторном заёме произойдёт ошибка
    def sub(self, row):
        assert(type(row) == Row)
        assert(self is not row)
        assert(self.period == row.period)
        assert(len(self.data) < self.period)

        if (row.isEmpty()):
            return
        
        row.preserve()
        while(row.hasItems()):
            row.pop()
            
            if (self.hasItems()):
                self.pop()
            else:
                self.fill()
        row.restore()
    
    def toArray(self):
        assert(len(self.data) < self.period)
        # assert(len(self.data) >= 0)
        arr = np.zeros(self.period - 1, dtype=int)
        self.preserve()
        i = 0
        while(self.hasItems()):
            self.pop()
            arr[i] = 1
            i = i + 1
        self.restore()
        return arr
    
    def setDecimal(self, num):
        assert(type(num) == int)
        # Не будем здесь поднимать флаг заёма
        assert(num < self.period)

        self.clear()
        for i in range(num):
            self.push()

    def getDecimal(self):
        return len(self.data)