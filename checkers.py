from chess import Figure, Board, Game


class Checker(Figure):
    """
    Класс для шашки.

    Атрибуты:
        color (str): Цвет шашки ("белые" или "негры").
        symbol (str): Символ, представляющий шашку на доске.
    """

    def __init__(self, color, symbol=None):
        if symbol is None:
            symbol = "Б" if color == "белые" else "Н"
        super().__init__(color, symbol)

    def get_possible_moves(self, board, start_row, start_col, is_killer):
        """
        Возвращает список возможных ходов для шашки.

        Аргументы:
            board (CheckersBoard): Игровая доска.
            start_row (int): Строка начальной позиции.
            start_col (int): Столбец начальной позиции.
            is_killer (bool): Указывает, выполняется ли захват.

        Возвращает:
            list: Список возможных позиций для хода.
        """

        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        # проверяю, могу ли я съесть кого-нибудь
        for dr, dc in directions:
            if self.check_pos(start_row + dr, start_col + dc):
                position = board.get_figure(start_row + dr, start_col + dc)
                if (
                    position is not None
                    and position.color != self.color
                    and self.check_pos(start_row + 2 * dr, start_col + 2 * dc)
                    and board.get_figure(start_row + 2 * dr, start_col + 2 * dc) is None
                ):
                    moves.append((start_row + 2 * dr, start_col + 2 * dc))

        # если противников рядом нет, значит я просто хожу вперёд
        if not (is_killer or moves):
            dir = -1 if self.color == "белые" else 1
            for dr, dc in [(dir, 1), (dir, -1)]:
                if self.check_pos(start_row + dr, start_col + dc):
                    moves.append((start_row + dr, start_col + dc))

        return moves

    def is_valid_move(self, board, start_row, start_col, end_row, end_col, is_killer):
        """
        Проверяет, является ли заданный ход допустимым.

        Аргументы:
            board (CheckersBoard): Игровая доска.
            start_row (int): Строка начальной позиции.
            start_col (int): Столбец начальной позиции.
            end_row (int): Строка конечной позиции.
            end_col (int): Столбец конечной позиции.
            is_killer (bool): Указывает, убивала ли фигура на этом ходу.

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """

        if not self.check_pos(end_row, end_col):
            return False

        if board.get_figure(end_row, end_col) is not None:
            return False

        possible_moves = self.get_possible_moves(board, start_row, start_col, is_killer)
        if (end_row, end_col) not in possible_moves:
            return False

        return True


class KingChecker(Checker):
    """
    Класс для дамки в шашках.

    Атрибуты:
        color (str): Цвет дамки ("белые" или "негры").
        symbol (str): Символ, представляющий дамку на доске.
    """

    def __init__(self, color):
        symbol = "К" if color == "белые" else "к"  # Символ для дамки
        super().__init__(color, symbol)

    def get_possible_moves(self, board, start_row, start_col, is_killer):
        """
        Возвращает список возможных ходов для дамки.

        Аргументы:
            board (CheckersBoard): Игровая доска.
            start_row (int): Строка начальной позиции.
            start_col (int): Столбец начальной позиции.
            is_killer (bool): Указывает, выполняется ли захват.

        Возвращает:
            list: Список возможных позиций для хода.
        """

        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Все диагонали

        for dr, dc in directions:
            row, col = start_row + dr, start_col + dc
            while self.check_pos(row, col):
                piece = board.get_figure(row, col)
                if piece is None:
                    moves.append((row, col))
                else:
                    if piece.color != self.color:
                        # Проверка возможности прыжка через фигуру
                        jump_row, jump_col = row + dr, col + dc
                        if (
                            self.check_pos(jump_row, jump_col)
                            and board.get_figure(jump_row, jump_col) is None
                        ):
                            moves.append((jump_row, jump_col))
                    break
                row += dr
                col += dc

        return moves


class CheckersBoard(Board):
    """
    Класс для доски шашек.

    Атрибуты:
        board (list): Двумерный список, представляющий игровую доску.
    """

    def initialize_board(self):
        """
        Расставляет шашки в начальную позицию.
        """

        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row][col] = Checker("негры")
                    elif row > 4:
                        self.board[row][col] = Checker("белые")

    def move_figure(self, start_row, start_col, end_row, end_col, is_killer):
        """
        Перемещает фигуру с одной позиции на другую и удаляет съеденную шашку.

        Аргументы:
            start_row (int): Строка начальной позиции.
            start_col (int): Столбец начальной позиции.
            end_row (int): Строка конечной позиции.
            end_col (int): Столбец конечной позиции.
            is_killer (bool): Указывает, убивала ли фигура на этом ходу.

        Возвращает:
            объект шашку (дамку) или None или False, если фигуры нет.
        """
        figure = self.get_figure(start_row, start_col)

        if not figure:
            return False

        if figure.is_valid_move(
            self, start_row, start_col, end_row, end_col, is_killer
        ):
            # Удаление съеденной шашки
            delta_row = end_row - start_row
            delta_col = end_col - start_col
            dr = 1 if delta_row > 0 else -1
            dc = 1 if delta_col > 0 else -1
            if abs(delta_row) >= 2:
                captured_figure = self.get_figure(end_row - dr, end_col - dc)
                self.board[end_row - dr][end_col - dc] = None
            else:
                captured_figure = None

            # Перемещение фигуры
            self.board[end_row][end_col] = figure
            self.board[start_row][start_col] = None

            # Проверка на превращение в дамку
            if isinstance(figure, Checker):
                if (figure.color == "белые" and end_row == 0) or (
                    figure.color == "негры" and end_row == 7
                ):
                    self.board[end_row][end_col] = KingChecker(figure.color)

            return captured_figure

        return False


class CheckersGame(Game):
    """
    Класс для управления игрой в шашки.

    Атрибуты:
        board (CheckersBoard): Игровая доска.
        current_turn (str): Текущий игрок ("белые" или "негры").
        move_count (float): Счетчик ходов.
    """

    def __init__(self):
        self.board = CheckersBoard()
        self.current_turn = "белые"
        self.move_count = 1

    def play(self):
        """
        Запускает игровой цикл.
        """

        while True:
            self.board.display([])
            print(f"Ход номер: {int(self.move_count)}, Ход {self.current_turn}")

            # 1. Получаю позицию фигуры
            command, start_row, start_col = self.choose_figure()

            # 2. Показываю подсказки
            is_killer = False
            while True:
                figure = self.board.get_figure(start_row, start_col)
                moves = figure.get_possible_moves(
                    self.board, start_row, start_col, is_killer
                )
                self.board.display(moves)

                # 3. Получаю ввод целевой позиции
                if moves:
                    end_row, end_col = self.get_target_position()
                    captured_figure = self.board.move_figure(
                        start_row, start_col, end_row, end_col, is_killer
                    )
                    if captured_figure is False:
                        print("Недопустимый ход")
                    elif isinstance(captured_figure, Checker) or isinstance(
                        captured_figure, KingChecker
                    ):
                        start_row, start_col = end_row, end_col
                        is_killer = True
                    else:
                        self.move_count += 0.5
                        self.current_turn = ("негры" if self.current_turn == "белые" else "белые")
                        break
                else:
                    self.move_count += 0.5
                    self.current_turn = ("негры" if self.current_turn == "белые" else "белые")
                    break


if __name__ == "__main__":
    checkers_game = CheckersGame()
    checkers_game.play()
