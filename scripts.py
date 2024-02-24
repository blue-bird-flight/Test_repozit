import time
matrix = ([" ", "1", "2", "3"],
          ["1", "-", "-", "-"],
          ["2", "-", "-", "-"],
          ["3", "-", "-", "-"])
counter = 1  # счетчик ходов для определения очередности хода
# xy = " "  # хранится Х или О для записи в поле вывода по координатам


# функция проверки выгрышных комбинаций
def check_win():
    # проверка выигрышных комбинаций для О
    # по строкам
    if matrix[1] == ['1', 'O', 'O', 'O'] or matrix[2] == ['2', 'O', 'O', 'O'] or matrix[3] == ['3', 'O', 'O', 'O']:
        return "*** выиграл О ***"
        # по столбцам
    if (matrix[1])[1] + (matrix[2])[1] + (matrix[3])[1] == "OOO":
        return "*** выиграл О ***"
    if (matrix[1])[2] + (matrix[2])[2] + (matrix[3])[2] == "OOO":
        return "*** выиграл О ***"
    if (matrix[1])[3] + (matrix[2])[3] + (matrix[3])[3] == "OOO":
        return "*** выиграл О ***"
        # по диагоналям
    if (matrix[1])[1] + (matrix[2])[2] + (matrix[3])[3] == "OOO":
        return "*** выиграл О ***"
    if (matrix[3])[1] + (matrix[2])[2] + (matrix[1])[3] == "OOO":
        return "*** выиграл О ***"
    # проверка выигрышных комбинаций для X
    # по строкам
    if matrix[1] == ['1', 'X', 'X', 'X'] or matrix[2] == ['2', 'X', 'X', 'X'] or matrix[3] == ['3', 'X', 'X', 'X']:
        return "*** выиграл X ***"
    # по столбцам
    if (matrix[1])[1] + (matrix[2])[1] + (matrix[3])[1] == "XXX":
        return "*** выиграл X ***"
    if (matrix[1])[2] + (matrix[2])[2] + (matrix[3])[2] == "XXX":
        return "*** выиграл X ***"
    if (matrix[1])[3] + (matrix[2])[3] + (matrix[3])[3] == "XXX":
        return "*** выиграл X ***"
        # по диагоналям
    if (matrix[1])[1] + (matrix[2])[2] + (matrix[3])[3] == "XXX":
        return "*** выиграл X ***"
    if (matrix[3])[1] + (matrix[2])[2] + (matrix[1])[3] == "XXX":
        return "*** выиграл X ***"
    # проверка положения "ничья", только один вариант когда все клетки заняты но никто не выиграл
    if "-" not in matrix[1] and "-" not in matrix[2] and "-" not in matrix[3]:
        return "*** НИЧЬЯ ***"


# печать игрового поля
def print_filed(x, y, xy):
    if xy == "O":
        (matrix[x])[y] = xy
    else:
        (matrix[x])[y] = xy
    for i in range(len(matrix)):
        print(*matrix[i])


# печать пустого игрового поля
print_filed(0, 0, " ")


# игровой цикл
while True:
    winner = ""
    if counter % 2 == 0:
        xy = "O"
    else:
        xy = "X"
    print(f'сейчас ходит {xy}')
    motion_koord = list(input('введите координаты через пробел ').split(' '))
    if motion_koord[0] == "stop":  # если стало больно проигрывать то можно ввести стоп-слово :)
        break
# проверка правильности формата ввода
    if len(motion_koord) == 2 and (motion_koord[0] in ['1', '2', '3']) and (motion_koord[1] in ['1', '2', '3']):
        if (matrix[int(motion_koord[0])])[int(motion_koord[1])] != "-":
            print('Клетка занята')
            continue
        counter += 1
        # вызов функции печати поля
        print_filed(int(motion_koord[0]), int(motion_koord[1]), xy)
        winner = check_win()  # вызов проверки выигрышных комбинаций
        # проверка есть ли победитель и вывод сообщения о победителе вывод пустого игрового поля
        if winner == "*** выиграл X ***" or winner == "*** выиграл О ***" or winner == "*** НИЧЬЯ ***":
            counter = 1
            print(winner)
            matrix = ([" ", "1", "2", "3"],
                      ["1", "-", "-", "-"],
                      ["2", "-", "-", "-"],
                      ["3", "-", "-", "-"])
            time.sleep(5)
            print()
            print()
            print_filed(0, 0, " ")
    else:
        print('неверный формат ввода!')
