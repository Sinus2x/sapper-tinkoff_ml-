import numpy as np
from funcs import coord, choice, save, load, nmines, output

print('Загрузить партию (y/n)?')
if input() == 'y':
    data = load()
    field, user, opened, marked, a, b, mines = data.values()
else:
    print('Введите через пробел размеры поля AxB (высота х ширина) и количество мин: ')
    a, b, mines = map(int, input().split())
    """a - высота (коор-та по y), b - ширина (коор-та x), 
       a и b не меньше 5 (вроде сапёр не играется с меньшими размерами поля"""

    while mines >= a*b:
        print("В поле должна быть хотя бы одна клетка без мин. Введите количество мин ещё раз: ")
        mines = int(input())

    print('Введите коор-ты клетки, с которой хотите начать игру (координаты начинаются с нуля, начало коор-т в левом',\
          end=' ')
    print('нижнем углу):')
    x, y = coord(a, b)

    mine_set = set()
    while len(mine_set) < mines:
        x1, y1 = np.random.randint(0, a), np.random.randint(0, b)
        if (x1, y1) != (x, y):  # в стартовой клетке не должно быть мины
            mine_set.add((x1, y1))
    field = np.zeros((a, b))
    for pair in mine_set:
        field[pair[0], pair[1]] = 1

    user = [['?' for i in range(b)] for j in range(a)]  # поле для вывода в консоль
    opened = set([(x, y)])  # открытые клетки
    marked = set()  # клетки с флажком

    user[x][y] = str(nmines(field, x, y))  # открываем стартовую клетку
    data = {'field': field, 'user': user, 'opened': opened, 'marked': marked, 'a': a, 'b': b, 'mines': mines}

print(f"Число мин: {mines}")
output(user)

while len(opened) < a*b-mines:  # пок не открыли все клетки без мин, делаем ход
    print("Выйти из игры (с сохранением)? (y/n)")
    if input() == 'y':
        save(*data.values())
        exit()
    x, y, action = choice(a, b)
    if action == 'open':
        if field[x, y] == 1:
            print('Мина! Game over.')
            for i in range(a):
                for j in range(b):
                    if field[i, j] == 1:
                        user[i][j] = '*'
            output(user)
            exit()
        else:
            if not (x, y) in opened:
                n = nmines(field, x, y)
                user[x][y] = str(n)
                if n == 0:
                    pass
                output(user)
                opened.add((x, y))  # обновили список открытых клеток
            else:
                print("Клетка уже открыта.")
    else:
        if (x, y) in opened:
            print("Клетка уже открыта.")
        elif (x, y) in marked:
            user[x][y] = '?'  # Флажок снят
            output(user)
            marked.remove((x, y))  # удалили клетку из списка помеченных
            print("Флажок снят.")
        else:
            user[x][y] = 'F'
            output(user)
            marked.add((x, y))
print('Победа!')







