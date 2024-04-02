from random import randint
import time


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'



class BoardException(Exception):  # создаем класс исключений наследуемый от Exception
    pass


class BoardOutException(BoardException):  # создаем класс исключений наследуемый от BoardException
    def __str__(self):  # выбрасывается когда игрок пытается выстрелить за пределы поля
        return 'АУТ'


class BoardOccupiedPlace(BoardException):  # создаем класс исключений наследуемый от BoardException
    def __str__(self):  # выбрасывается при попытке выстрелить в одно и тоже место
        return 'сюда уже стреляли'


class BoardWrongShipException(BoardOutException):  # создаем пустое исключение которое будет выбрасываться
    pass   # при попытке установить корабль за пределы поля


class Dot:  # создаем класс для точек
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # используем метод __eq__ для последующего сравнения объектов класса Dot
        return self.x == other.x and self.y == other.y

    def __str__(self):  # задаем формат вывода объектов класса Dot
        return f'Dot: {self.x, self.y}'


class Ship:  # создаем класс Ship имеющий свойства
    def __init__(self, long, start, direction):
        self.long = long  # длина корабля
        self.start = start  # координаты начальной точки
        self.direction = direction  # направление корабля
        self.lives = long  # количество жизней


    @property
    def dots(self):  # свойство dots возвращает координаты всех точек корабля
        ship_dots = []  # создаем пустой список для записи точек корабля
        for i in range(self.long):  # для каждой точки получаем
            cur_x = self.start.x  # координату Х
            cur_y = self.start.y  # координату Y
            if self.direction == 0:  # если корабль вертикальный
                cur_x += i  # увеличиваем Х на i
            elif self.direction == 1:  # если корабль горизонтальный
                cur_y += i  # увеличиваем Y на i
            ship_dots.append(Dot(cur_x, cur_y))  # добавляем точки в словарь
        return ship_dots

    def shooten(self, shot):  # проверка попадания
        return shot in self.dots  # если координаты выстрела входят в координаты корабля от True


class Board:  # создаем класс Board имеющий свойства
    def __init__(self, hide=False, size=6):
        self.size = size  # размер поля
        self.hide = hide  # флаг hide для определния скрывать корабли или нет
        self.count = 0  # счетчик уничтоженых кораблей
        self.field = [["0"] * size for _ in range(size)]  # заполнение поля
        self.busy = []  # список занятых точек поля
        self.ships = []  # список кораблей поля

    def __str__(self):  # метод определяющий формат вывода доски
        res = ""
        res += "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1}  | " + " | ".join(row) + " |"

        if self.hide:
            res = res.replace("■", "0")
        return res

    def out(self, d):  # задаем метод out для проверки выхода координат точки за пределы поля
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]  # создаем список с координатами контура
        for d in ship.dots:  # для каждой точки корабля
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)  # получаем координаты контура точки
                if not (self.out(cur)) and cur not in self.busy:  # проверяем занята точка или выходит за пределы поля
                    if verb:  # если нет
                        self.field[cur.x][cur.y] = "."  # записываем в поле точки знак занято
                    self.busy.append(cur)  # записываем координаты точки в список busy

    def add_ship(self, ship):
        for d in ship.dots:  # для каждой точки корабля
            if self.out(d) or d in self.busy:  # проверяем выход за пределы поля и занята ли точка
                raise BoardWrongShipException()  # выбрасываем исключение во внешнюю логику
        for d in ship.dots:  # после проверки для каждой точки корабля
            self.field[d.x][d.y] = "■"  # записываем в поле значок корабля
            self.busy.append(d)  # записываем координаты каждой точки корабля в список busy

        self.ships.append(ship)  # добаляем точки корабля в список ships
        self.contour(ship)  # вызываем метод contour для нахождения контура корабля

    def shot(self, d):
        if self.out(d):  # проверяем что полученные координаты точки в пределах поля
            raise BoardOutException()  # если да то выбрасываем исключение

        if d in self.busy:  # проверяем что точка с полученными координатами уже занята
            raise BoardOccupiedPlace() # если да то выбрасываем исключение

        self.busy.append(d)  # при отсутствии исключений добавляет точку в список busy

        for ship in self.ships:  # для каждого корабля проверяем
            if ship.shooten(d):  # попадание
                ship.lives -= 1  # уменьшаем количество жизней на 1
                self.field[d.x][d.y] = color.RED + "X" + color.END  # ставим Х в точку с координатами выстрела
                if ship.lives == 0:  # если корабль уничтожен
                    self.count += 1
                    self.contour(ship, verb=True)  # передаем в contour verb=True для отображения контура
                    print(color.RED + "Корабль уничтожен!" + color.END)  # уничтоженного корабля
                    return False  # возвращаем False для определения необходимости повторного хода
                else:
                    print(color.RED + "Корабль повреждён!" + color.END)
                    return True  # возвращаем True для определения необходимости повторного хода

        self.field[d.x][d.y] = color.RED + "✸" + color.END  # ставим знак промаха в точку с координатами выстрела
        print("Промах!")
        return False  # возвращаем False для определения необходимости повторного хода

    def begin(self):  # создаем метод для
        self.busy = []  # обнуления списка занятых точеек

    def defeat(self):  # создаем метод определения поражения
        return self.count == len(self.ships)  # если счетчик пораженных кораблей равен списку кораблей на доске


class Player:  # создаем класс Player
    def __init__(self, board, enemy):  # задаем для объектов Player свойства board и enemy в которых будет
        self.board = board  # храниться состояние своей доски
        self.enemy = enemy  # и доски протовника

    def ask(self):  # задаем метод ask для получения координат выстрела вводом для игрока и рандомно для компьютера
        raise NotImplementedError()  # узываем что метод будет опредлен в потомках класса

    def move(self):  # задаем метод для совершения хода
        while True:
            try:
                target = self.ask()  # target получает координаты выстрела
                repeat = self.enemy.shot(target)  # получаем True или False
                return repeat  # возвращаем True или False
            except BoardException as e:  # отлавливаем исключение и записываем в e
                print(e)  # выводим исключение


class AI(Player):
    def ask(self):  # запрос координат выстрела AI через случайное число
        d = Dot(randint(0, 5), randint(0, 5))
        print(color.YELLOW + f"Ход компьютера: {d.x + 1} {d.y + 1}" + color.END)
        time.sleep(5)
        return d  # возврат объекта класса Dot с получеными координатами


class User(Player):
    def ask(self):  # запрос координат выстрела игрока через ввод с клавиатуры
        while True:
            cords = input(color.PURPLE + "Ваш ход: " + color.END).split()
# проверка правильности формата ввода
            if len(cords) != 2:
                print(color.RED + "Введите 2 координаты! " + color.END)
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print(color.RED + "Введите числа! " + color.END)
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)  # возврат объекта класса Dot с введенными координатами


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()  # создание доски игрока
        co = self.random_board()  # создание доски компьютера
        co.hide = True  # определение парпметра hide для скрытия кораблей компьютера

        self.ai = AI(co, pl)   # в объект класса Game с методомами  ai и us передается
        self.us = User(pl, co)  # объект класса player имеющий свою доску и доску врага

#  попытка создания доски
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]  # создаем список с длинами кораблей
        board = Board(size=self.size)  # создаем объект Board с размером size
        attempts = 0  # количество попыток создания случайной доски
        for l in lens:  # для каждой длины корабля
            while True:  # в бесконечном цикле
                attempts += 1  # увеличивая счетчик попыток
                if attempts > 2000:  # до 2000 раз
                    return None  # после 2000 попыток возвращаем None в random_board и начинем с начала
                # создаем объект Ship
                ship = Ship(l, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.add_ship(ship)  # пытаемся установить корабль на доске
                    break  # если не выброшено исключение переходим к следующему кораблю
                except BoardWrongShipException:  # отлавливаем исключение из add_ship
                    pass  # делаем следующую попытку поставить этот корабль
        board.begin()  # обнуляем список занятых точек
        return board  # возвращаем доску

    def random_board(self):  # метод проверки создания случайной доски
        board = None  # создаем пустую доску
        while board is None:  # пока доска пустая
            board = self.try_board()  # вызываем метод try_board
        return board

    def greet(self):  # выводим приветствие 4
        print(color.PURPLE + "------------------------")
        print("    Приветствуем вас    ")
        print("         в игре         ")
        print("       морской бой      ")
        print("------------------------" + color.END)
        print(color.YELLOW + "    формат ввода: x y   ")
        print("    x - номер строки    ")
        print("    y - номер столбца   " + color.END)

    def print_boards(self):
        print(color.PURPLE + "-" * 20)
        print("Доска пользователя:" + color.END)
        print(self.us.board)  # печатаем доску игрока(вызываем метод us с параметром board)
        print(color.YELLOW + "-" * 20)
        print("Доска компьютера:" + color.END)
        print(self.ai.board)  # печатаем доску игрока(вызываем метод со с параметром board)
        print(color.RED + "-" * 20 + color.END)

    def loop(self):  # игровой цикл
        num = 0  # переменная для определения очередности хода чет/нечет
        while True:  # запускаем бесконечный цикл
            self.print_boards()  # вызываем метод print_boards для печати игровых полей

            if num % 2 == 0:  # если num четное ходит игрок
                print(color.PURPLE + "✅ Ходит пользователь!" + color.END)
                repeat = self.us.move()  # вызываем метод move для игрока
            else:  # если num нечетное ходит компьютер

                print(color.YELLOW + "✅ Ходит компьютер!" + color.END)
                repeat = self.ai.move()  # вызываем метод move для компьютера
            if repeat:  # если попал repeat имеет значение True
                num -= 1  # уменьшаем num для повторения хода

            if self.ai.board.defeat():  # проверяем проигрыш компьютера
                self.print_boards()  # выводим доски
                print(color.PURPLE + "-" * 20)
                print("✸✸✸Пользователь выиграл!✸✸✸" + color.END)  # и сообщение о выигрыше
                break

            if self.us.board.defeat():  # проверяем проигрыш игрока
                self.print_boards()
                print(color.YELLOW + "-" * 20)
                print("✸✸✸Компьютер выиграл!✸✸✸" + color.END) # и сообщение о выигрыше
                break
            num += 1

    def start(self):
        self.greet()  # метод greet для Game
        self.loop()  # запускаем метод loop - игровой цикл


g = Game()  # создаем объект класса Game
g.start()  # вызываем объект Game с методом start
