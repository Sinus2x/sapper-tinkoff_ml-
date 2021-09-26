import pickle as pkl
import numpy as np


def coord(a, b):
    x, y = map(int, input().split())
    while not (x>=0 and y>=0 and y<a and x<b):
        print("Таких координат не существует, введите ещё раз.")
        x, y = map(int, input().split())
        # a=3,b=4,x=1,y=2, defactox=a-y-1=0, defactoy = x = 1
        """переводим координаты в привычный формат. Если будем пользоваться индексацией  
        field[defacto_x, defacto_y], будем получать ожидаемую ячейку поля.
        Начало координат располагается в левом нижнем углу."""
    defacto_x, defacto_y = a - y - 1, x
    return (defacto_x, defacto_y)


def choice(a, b):
    """Ход делается в виде [X,Y,Action]
    Action: 'flag' (поставить флажок), 'open' (открыть клетку), остальные варианты ввода (без учёта регистра)
            будут интерпретированы как ошибки.
    X,Y - координаты клетки"""
    print("Введите координаты клетки (координаты начинаются с нуля, начало координат в левом нижнем углу): ")
    x, y = coord(a, b)
    print('Поставить флажок (flag) или открыть клетку (open)?')
    action = input().lower()
    while not (action=='flag' or action=='open'):
        print("Такого действия не существует. Введите ещё раз.")
        action = input().lower()
    return [x, y, action]


def save(field, user, opened, marked, a, b, mines):
    print("Как вы хотите назвать сохранение: ")
    path = input()
    data = {'field': field, 'user': user, 'opened': opened, 'marked': marked, 'a': a, \
            'b': b, 'mines': mines}
    file = open(rf'{path}.txt', 'wb')
    pkl.dump(data, file)
    file.close()


def load():
    print("Введите название сохранения: ")
    path = input()
    f = open(rf'{path}.txt', 'rb')
    data = pkl.load(f)
    f.close()
    return data


def nmines(field, x, y):
    a, b = field.shape
    field = np.concatenate((field, np.zeros(a).reshape(-1, 1)), axis=1)  # обрамляем нулями справа
    field = np.concatenate((np.zeros(a).reshape(-1, 1), field), axis=1)  # обрамляем нулями слева
    field = np.concatenate((np.zeros(b+2).reshape(1, b+2), field))  # обрамляем сверху
    field = np.concatenate((field, np.zeros(b+2).reshape(1, b+2))).astype('int64')  # обрамляем снизу и приводим \
                                                                                                  # к целому числу
    x, y = x+1, y+1  # координаты сместились из-за обрамления нулями
    return field[x, y+1] + field[x, y-1] + field[x+1, y] + field[x-1, y] + field[x+1, y+1] + field[x-1, y-1] + \
           field[x-1, y+1] + field[x+1, y-1]

#
# def open_zero(user, field, x, y, a, b, opened, marked):
#     if (x == 0):
#         if (y==0):
#             neighbours = [(x+1, y), (x+1, y+1), (x, y+1)]
#         elif y==a-1:
#             neighbours = [(x + 1, y), (x + 1, y - 1), (x, y - 1)]
#         else:
#             neighbours = [(x + 1, y), (x + 1, y - 1), (x+1, y+1), (x, y - 1), (x, y+1)]
#     elif x == b-1:
#         if (y == 0):
#             neighbours = [(x-1, y), (x-1, y+1), (x, y+1)]
#         elif y==a-1:
#             neighbours = [(x - 1, y), (x - 1, y - 1), (x, y - 1)]
#         else:
#             neighbours = [(x - 1, y), (x - 1, y - 1), (x-1, y+1), (x, y - 1), (x, y+1)]
#     else:
#         if y == 0:
#             neighbours = [(x-1, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y)]
#         elif y==a-1:
#             neighbours = [(x - 1, y), (x - 1, y - 1), (x, y - 1), (x+1, y-1), (x+1, y)]
#         else:
#             neighbours = [(x - 1, y), (x - 1, y - 1), (x-1, y + 1), (x, y+1), (x, y-1), (x+1, y), (x+1, y+1), \
#                           (x+1, y-1)]
#     for coord in neighbours:
#         if (not coord in opened) and (coord not in marked):
#             n = nmines(field, *coord)
#             opened.add(coord)
#             user[coord[0]][coord[1]] = str(nmines(field, *coord))
#             if n == 0:
#                 open_zero(user, field, *coord, a, b, opened, marked)
#     return (user, opened)


def output(user_field):
    for row in user_field:
        print('  '.join(row))


# class Field:
#     def __init__(self, a=5, b=5, mines=3, x=0, y=0):
#         self.a, self.b, self.mines = a, b, mines
#         self.start_x, self.start_y = x, y
#         self.user = [['?' for i in range(b)] for j in range(a)]
#         self.opened, self.marked = set([(x, y)]), set()
#         mine_set = set()
#         while len(mine_set) < mines:
#             x1, y1 = np.random.randint(0, a), np.random.randint(0, b)
#             if (x1, y1) != (x, y):  # в стартовой клетке не должно быть мины
#                 mine_set.add((x1, y1))
#         self.field = np.zeros((a, b))
#         for pair in mine_set:
#             self.field[pair[0], pair[1]] = 1
#
#     def neighbours(self, x, y):
#         if (x == 0):
#             if (y == 0):
#                 neighbours = [(x + 1, y), (x + 1, y + 1), (x, y + 1)]
#             elif y == self.a - 1:
#                 neighbours = [(x + 1, y), (x + 1, y - 1), (x, y - 1)]
#             else:
#                 neighbours = [(x + 1, y), (x + 1, y - 1), (x + 1, y + 1), (x, y - 1), (x, y + 1)]
#         elif x == self.b - 1:
#             if (y == 0):
#                 neighbours = [(x - 1, y), (x - 1, y + 1), (x, y + 1)]
#             elif y == self.a - 1:
#                 neighbours = [(x - 1, y), (x - 1, y - 1), (x, y - 1)]
#             else:
#                 neighbours = [(x - 1, y), (x - 1, y - 1), (x - 1, y + 1), (x, y - 1), (x, y + 1)]
#         else:
#             if (y == 0):
#                 neighbours = [(x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y)]
#             elif y == self.a - 1:
#                 neighbours = [(x - 1, y), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y)]
#             else:
#                 neighbours = [(x - 1, y), (x - 1, y - 1), (x - 1, y + 1), (x, y + 1), (x, y - 1), (x + 1, y),
#                               (x + 1, y + 1), (x + 1, y - 1)]
#         return neighbours
#
#     def save(self):
#         print("Как вы хотите назвать сохранение: ")
#         path = input()
#         data = {'field': self.field, 'user': self.user, 'opened': self.opened, 'marked': marked, 'a': self.a, \
#                 'b': self.b, 'mines': self.mines}
#         file = open(rf'{path}.txt', 'wb')
#         pkl.dump(data, file)
#         file.close()
#
#     def load(self):
#         print("Введите название сохранения: ")
#         path = input()
#         f = open(rf'{path}.txt', 'rb')
#         data = pkl.load(f)
#         f.close()
#         self.field, self.user, self.opened, self.marked, self.a, self.b, self.mines = data.values()
#
#     def output(self):
#         for row in self.user:
#             print('  '.join(row))
#
#     def nmines(self, x, y):
#         pass

