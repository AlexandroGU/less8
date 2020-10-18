from random import randint
class Card:
    rows = 3
    cols = 7
    nums_in_row = 6
    data = ()
    emptynum = 2
    crossednum = -1
    def __init__(self):
        uniques_count = self.nums_in_row * self.rows
        uniques = generate_unique_numbers(uniques_count, 1, 90)
        self.data = []
        for i in range(0,self.rows):
            tmp = sorted(uniques[self.nums_in_row * i: self.nums_in_row * (i + 1)])
            empty_nums_count = self.cols - self.nums_in_row
            for j in range(0, empty_nums_count):
                index = randint(0, len(tmp))
                tmp.insert(index,self.emptynum)
            self.data += tmp
    def __str__(self):
        delimiter = '********************'
        ret = delimiter + '\n'
        for index, num in enumerate(self.data):
            if num == self.emptynum:
                ret += '  '
            elif num == self.crossednum:
                ret += ' -'
            elif num < 10:
               ret += f' {str(num)}'
            else:
                ret += str(num)
            if (index + 1) % self.cols == 0:
               ret += '\n'
            else:
                ret += ' '
        return ret + delimiter
    def __contains__(self, item):
        return item in self.data
    def cross_num(self, num):
        for index, item in enumerate(self.data):
            if item == num:
                self.data[index] = self.crossednum
                return
        raise ValueError(f'Number not in card: {num}')
    def closed(self) -> bool:
        return set(self.data) == {self.emptynum,self.crossednum}
def generate_unique_numbers(count, minbound, maxbound):
    if count > maxbound - minbound + 1:
        raise ValueError('Incorrect input parameters')
    ret = []
    while len(ret) < count:
        new = randint(minbound, maxbound)
        if new not in ret:
            ret.append(new)
    return ret
class Game:
    usercard = None
    compcard = None
    numkegs = 90
    kegs = []
    gameover = False
    def __init__(self):
        self.usercard = Card()
        self.compcard = Card()
        self.kegs = generate_unique_numbers(self.numkegs,1,90)
    def play_round(self) -> int:

        keg = self.kegs.pop()
        print(f'Новый бочонок: {keg} (осталось {len(self.kegs)})')
        print(f' Ваш Билет \n{self.usercard}')
        print(f'Билет Компьютера\n{self.compcard}')
        useranswer = input('Зачеркнуть цифру? (да/нет)').lower().strip()
        if useranswer == 'да' and not keg in self.usercard or \
           useranswer != 'да' and keg in self.usercard:
            return 2
        if keg in self.usercard:
            self.usercard.cross_num(keg)
            if self.usercard.closed():
                return 1
        if keg in self.compcard:
            self.compcard.cross_num(keg)
            if self.compcard.closed():
                return 2
        return 0
class Keg:
    __num = None
    def __init__(self):
        self.__num = randint(1, 90)

    @property
    def num(self):
        return self.__num
    def __str__(self):
        return str(self.__num)
game = Game()
while True:
    score = game.play_round()
    if score == 1:
        print('ты победил')
        break
    elif score == 2:
        print('ты проиграл')
        break