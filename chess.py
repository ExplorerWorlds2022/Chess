from random import randint
from termcolor import colored


class Figure:
    """
    Базовый класс для шахматных фигур.

    Args:
        color (str): Цвет фигуры ('белые' или 'негры').
        symbol (str): Символ для отображения фигуры на доске.
    """

    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def get_possible_moves(self, board, start_row, start_col):
        """
        Возвращает список возможных ходов для фигуры.  В базовом классе возвращает пустой список.
        Подклассы должны переопределить этот метод.

        Args:
            board (Board): Объект доски.
            start_row (int): Начальная строка фигуры.
            start_col (int): Начальный столбец фигуры.

        Returns:
            list: Список возможных ходов из кортежей (row, col).
        """

        return []

    def check_pos(self, end_row, end_col):
        return 0 <= end_row < 8 and 0 <= end_col < 8

    def is_valid_move(self, board, start_row, start_col, end_row, end_col):
        """
        Проверяет, является ли ход допустимым.

        Args:
            board (Board): Объект доски.
            start_row (int): Начальная строка фигуры.
            start_col (int): Начальный столбец фигуры.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, False в противном случае.
        """

        if not self.check_pos(end_row, end_col):
            return False

        # Проверка, что на конечной позиции нет фигуры того же цвета.
        target_figure = board.get_figure(end_row, end_col)
        if target_figure and target_figure.color == self.color:
            return False

        # Проверка, что ход входит в список возможных ходов.
        get_possible_moves = self.get_possible_moves(board, start_row, start_col)
        if (end_row, end_col) not in get_possible_moves and type(self) != Mage:
            return False

        return True


class Pawn(Figure):
    """
    Класс для пешки.
    """

    def __init__(self, color):
        symbol = "P" if color == "белые" else "p"
        super().__init__(color, symbol)

    def get_possible_moves(self, board, start_row, start_col):
        moves = []
        direction = -1 if self.color == "белые" else 1

        # Ход на одну клетку вперед
        new_row = start_row + direction
        if (
            self.check_pos(new_row, start_col)
            and board.get_figure(new_row, start_col) is None
        ):
            moves.append((new_row, start_col))

            # Ход на две клетки вперед (только для первого хода)
            if (
                self.color == "белые"
                and start_row == 6
                or self.color == "негры"
                and start_row == 1
            ):
                new_row = start_row + 2 * direction
                if (
                    self.check_pos(new_row, start_col)
                    and board.get_figure(new_row, start_col) is None
                ):
                    moves.append((new_row, start_col))

        # Атака по диагонали
        for col in [start_col - 1, start_col + 1]:
            new_row = start_row + direction
            if self.check_pos(new_row, col):
                target_figure = board.get_figure(new_row, col)
                if target_figure and target_figure.color != self.color:
                    moves.append((new_row, col))

        return moves


class Rook(Figure):
    """
    Класс для ладьи.
    """

    def __init__(self, color):
        symbol = "R" if color == "белые" else "r"
        super().__init__(color, symbol)

    def get_possible_moves(self, board, start_row, start_col):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Вверх, вниз, влево, вправо

        for y, x in directions:
            row, col = start_row + y, start_col + x
            while self.check_pos(row, col):
                piece = board.get_figure(row, col)
                if piece is None:
                    moves.append((row, col))
                else:
                    if piece.color != self.color:
                        moves.append((row, col))
                    break
                row += y
                col += x

        return moves


class Knight(Figure):
    """
    Класс для коня.
    """

    def __init__(self, color):
        symbol = "H" if color == "белые" else "h"
        super().__init__(color, symbol)

    def get_possible_moves(self, board, start_row, start_col):
        moves = []
        get_possible_moves = [
            (start_row - 2, start_col - 1),
            (start_row - 2, start_col + 1),
            (start_row - 1, start_col - 2),
            (start_row - 1, start_col + 2),
            (start_row + 1, start_col - 2),
            (start_row + 1, start_col + 2),
            (start_row + 2, start_col - 1),
            (start_row + 2, start_col + 1),
        ]
        for row, col in get_possible_moves:
            if self.check_pos(row, col):
                if (
                    board.get_figure(row, col) is None
                    or board.get_figure(row, col).color != self.color
                ):
                    moves.append((row, col))
        return moves


class Bishop(Figure):
    """
    Класс для слона.
    """

    def __init__(self, color):
        symbol = "B" if color == "белые" else "b"
        super().__init__(color, symbol)

    def get_possible_moves(self, board, start_row, start_col):
        moves = []
        directions = [
            (-1, -1),  # Вверх-влево
            (-1, 1),  # Вверх-вправо
            (1, -1),  # Вниз-влево
            (1, 1),  # Вниз-вправо
        ]

        for y, x in directions:
            row, col = start_row + y, start_col + x
            while self.check_pos(row, col):
                piece = board.get_figure(row, col)
                if piece is None:
                    moves.append((row, col))
                else:
                    if piece.color != self.color:
                        moves.append((row, col))
                    break
                row += y
                col += x

        return moves


class Queen(Figure):
    """
    Класс для королевы.
    """

    def __init__(self, color):
        symbol = "Q" if color == "белые" else "q"
        super().__init__(color, symbol)

    def get_possible_moves(self, board, start_row, start_col):
        return Rook(self.color).get_possible_moves(
            board, start_row, start_col
        ) + Bishop(self.color).get_possible_moves(board, start_row, start_col)


class King(Figure):
    """
    Класс для короля.
    """

    def __init__(self, color):
        symbol = "K" if color == "белые" else "k"
        super().__init__(color, symbol)

    def get_possible_moves(self, board, start_row, start_col):
        moves = []
        get_possible_moves = [
            (start_row - 1, start_col - 1),
            (start_row - 1, start_col),
            (start_row - 1, start_col + 1),
            (start_row, start_col - 1),
            (start_row, start_col + 1),
            (start_row + 1, start_col - 1),
            (start_row + 1, start_col),
            (start_row + 1, start_col + 1),
        ]

        for row, col in get_possible_moves:
            if self.check_pos(row, col):
                if (
                    board.get_figure(row, col) is None
                    or board.get_figure(row, col).color != self.color
                ):
                    moves.append((row, col))

        return moves


class Mage(Figure):
    """
    Класс для мага. Ходит на случайную клетку
    """

    def __init__(self, color):
        symbol = "M" if color == "белые" else "m"
        super().__init__(color, symbol)


class Spearman(Figure):
    """
    Класс для копейщика. Ходит на 1 из 3 передних клеток
    """

    def __init__(self, color):
        symbol = "S" if color == "белые" else "s"
        super().__init__(color, symbol)

    def get_possible_moves(self, board, start_row, start_col):
        moves = []
        direction = -1 if self.color == "белые" else 1
        get_possible_moves = [
            (start_row + direction, start_col - 1),
            (start_row + direction, start_col),
            (start_row + direction, start_col + 1),
        ]
        for row, col in get_possible_moves:
            if self.check_pos(row, col):
                if (
                    board.get_figure(row, col) is None
                    or board.get_figure(row, col).color != self.color
                ):
                    moves.append((row, col))
        return moves


class Demon(Figure):
    """
    Класс для демона. Фигура ходит также, как и последняя съеденная фигура (по умолчанию как король)
    """

    def __init__(self, color):
        symbol = "D" if color == "белые" else "d"
        self.power = "King"
        super().__init__(color, symbol)

    def get_possible_moves(self, board, start_row, start_col):
        Power = globals()[self.power]
        return Power(self.color).get_possible_moves(board, start_row, start_col)


class Board:
    """
    Класс для представления и управления шахматной доской.
    """

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()

    def initialize_board(self):
        """
        Расставляет фигуры в начальную позицию.
        """

        self.board[7][0] = Rook("белые")
        self.board[7][1] = Knight("белые")
        self.board[7][2] = Bishop("белые")
        self.board[7][3] = Queen("белые")
        self.board[7][4] = King("белые")
        self.board[7][5] = Bishop("белые")
        self.board[7][6] = Knight("белые")
        self.board[7][7] = Rook("белые")
        for pos in range(8):
            self.board[6][pos] = Pawn("белые")

        self.board[0][0] = Rook("негры")
        self.board[0][1] = Knight("негры")
        self.board[0][2] = Bishop("негры")
        self.board[0][3] = Queen("негры")
        self.board[0][4] = King("негры")
        self.board[0][5] = Bishop("негры")
        self.board[0][6] = Knight("негры")
        self.board[0][7] = Rook("негры")
        for pos in range(8):
            self.board[1][pos] = Pawn("негры")

    def get_figure(self, row, col):
        """
        Возвращает фигуру на заданной позиции.

        Args:
            row (int): Строка.
            col (int): Столбец.

        Returns:
            Figure: Фигура на позиции (row, col) или None, если клетка пуста.
        """

        return self.board[row][col]

    def move_figure(self, start_row, start_col, end_row, end_col):
        """
        Перемещает фигуру с одной позиции на другую.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            Figure: Съеденная фигура или None, если фигура не была съедена. False, если фигура
                с такими координатами отсутсвует.
        """
        
        figure = self.get_figure(start_row, start_col)

        if not figure:
            return False

        if figure.is_valid_move(self, start_row, start_col, end_row, end_col):
            captured_figure = self.get_figure(end_row, end_col)
            self.board[end_row][end_col] = figure
            self.board[start_row][start_col] = None
            return captured_figure

        return False

    def display(self, get_possible_moves):
        """
        Выводит доску в консоль с подсказками для возможных ходов.
        """

        print("\n    a b c d e f g h")
        for row in range(8):
            begin = f"{8 - row}  "
            row_str = ""
            for pos in range(8):
                if (row, pos) in get_possible_moves:
                    figure = self.board[row][pos]
                    if figure:
                        row_str += colored(figure, "red") + " "
                    else:
                        row_str += "* "  # Символ '*' для пустых клеток
                else:
                    figure = self.board[row][pos]
                    if figure:
                        row_str += f"{figure} "
                    else:
                        row_str += ". "
            print(begin, row_str, begin)
        print("\n    a b c d e f g h")


class NewBoard(Board):
    def initialize_board(self):
        """
        Расставляет фигуры в начальную позицию.
        """
        self.board[7][0] = Rook("белые")
        self.board[7][1] = Knight("белые")
        self.board[7][2] = Bishop("белые")
        self.board[7][3] = Mage("белые")
        self.board[7][4] = King("белые")
        self.board[7][5] = Bishop("белые")
        self.board[7][6] = Knight("белые")
        self.board[7][7] = Rook("белые")
        self.board[4][6] = Demon("белые")
        for pos in range(8):
            self.board[6][pos] = Spearman("белые")

        self.board[0][0] = Rook("негры")
        self.board[0][1] = Knight("негры")
        self.board[0][2] = Bishop("негры")
        self.board[0][3] = Mage("негры")
        self.board[0][4] = King("негры")
        self.board[0][5] = Bishop("негры")
        self.board[0][6] = Knight("негры")
        self.board[0][7] = Rook("негры")
        self.board[3][1] = Demon("негры")
        for pos in range(8):
            self.board[1][pos] = Spearman("негры")


class Move:
    """
    Класс для представления хода. Содержит информацию о начальной и конечной позициях,
    а также о фигуре, которая была съедена.
    """

    def __init__(self, start_row, start_col, end_row, end_col, captured_figure):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.captured_figure = captured_figure


class Game:
    """
    Класс для управления игрой.

    Args:
        mode (str): режим игры classic или special
    """

    def __init__(self, mode):
        if mode == "classic":
            self.board = Board()
        else:
            self.board = NewBoard()
        self.current_turn = "белые"
        self.move_count = 1
        self.moves = []

    def choose_figure(self):
        """
        Запрашивает у пользователя выбор фигуры для хода
        """

        while True:
            try:
                pos_str = input(
                    f"Выберите фигуру для хода {self.current_turn}: (например, a2, undo) "
                )
                if pos_str == "undo":
                    return "undo", None, None

                start_col = ord(pos_str[0]) - ord("a")
                start_row = 8 - int(pos_str[1])

                if not (0 <= start_row < 8 and 0 <= start_col < 8):
                    print("Некорректный ввод. Позиции должны быть в пределах доски.")
                    continue

                piece = self.board.get_figure(start_row, start_col)
                if piece is None or piece.color != self.current_turn:
                    print("Это не ваша фигура или сейчас не ваш ход")
                    continue

                return "select", start_row, start_col

            except (ValueError, IndexError):
                print("Некорректный ввод. Пожалуйста, используйте формат: a2, undo")

    def get_target_position(self):
        """
        Запрашивает у пользователя ввод целевой позиции.
        """

        while True:
            try:
                end_pos = input("Введите целевую позицию: (например, a4) ")
                end_col = ord(end_pos[0]) - ord("a")
                end_row = 8 - int(end_pos[1])

                if not (0 <= end_row < 8 and 0 <= end_col < 8):
                    print("Некорректный ввод. Позиции должны быть в пределах доски.")
                    continue

                return end_row, end_col

            except (ValueError, IndexError):
                print("Некорректный ввод. Пожалуйста, используйте формат: a4")

    def undo_move(self):
        """
        Отменяет последний ход.
        """

        if self.moves:
            last_move = self.moves.pop()
            self.board.board[last_move.start_row][last_move.start_col] = (
                self.board.get_figure(last_move.end_row, last_move.end_col)
            )
            self.board.board[last_move.end_row][
                last_move.end_col
            ] = last_move.captured_figure

            self.current_turn = "негры" if self.current_turn == "белые" else "белые"
            self.move_count -= 0.5
        else:
            print("Нечего отменять")

    def play(self):
        """
        Запускает игровой цикл
        """

        while True:
            self.board.display([])
            print(f"Ход номер: {int(self.move_count)}, Ход {self.current_turn}")

            # Получаю позицию фигуры
            command, start_row, start_col = self.choose_figure()
            if command == "undo":
                self.undo_move()
                continue

            # Показываю подсказки и получаю конечную позицию
            figure = self.board.get_figure(start_row, start_col)
            if type(figure) == Mage:
                end_row, end_col = randint(0, 7), randint(0, 7)
            else:
                self.board.display(
                    figure.get_possible_moves(self.board, start_row, start_col)
                )
                end_row, end_col = self.get_target_position()

            captured_figure = self.board.move_figure(
                start_row, start_col, end_row, end_col
            )
            if captured_figure is False:
                print("Недопустимый ход")
            else:
                move = Move(
                    start_row,
                    start_col,
                    end_row,
                    end_col,
                    captured_figure,
                )
                self.moves.append(move)
                self.move_count += 0.5

                if type(figure) == Demon and captured_figure != None:
                    figure.power = type(captured_figure).__name__
                if type(captured_figure) == King:
                    print(
                        f"Игра окончена! {self.current_turn} победили за {int(self.move_count)} ходов!"
                    )
                    self.board.display([])
                    break
                self.current_turn = "негры" if self.current_turn == "белые" else "белые"


if __name__ == "__main__":
    mode = input("Введите режим (classic, special): ")
    while mode not in ["classic", "special"]:
        mode = input("Введите режим (classic, special): ")

    game = Game(mode)
    game.play()