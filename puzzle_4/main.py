import functools

# PART 1

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def read_input(lines):
    first = [int(x) for x in lines[0].split(',')]
    lines = lines[1:]
    lines = [int(x) for l in lines for x in l.split(' ') if x != ""]
    second = list(chunks(lines, 5*5))
    return (first, second)

def get_position(board, number):
    if number not in board:
        return None
    i = board.index(number)
    return (i % 5, int(i / 5))

def check_on_baord(checker_board, pos):
    return [1 if pos[0] + 5 * pos[1] == xi else x for xi, x in enumerate(checker_board)]

def is_winner(checker_board):
    for i in range(5):
        if sum(checker_board[i * 5:i * 5 + 5]) == 5:
            return True
        if sum(checker_board[i:21+i:5]) == 5:
            return True
    return False

def sum_unchecked(board, checker_board):
    return sum([x for xi, x in enumerate(board) if checker_board[xi] == 0])

lines = [x.strip() for x in list(open('input.txt', 'r'))]
numbers, boards = read_input(lines)

# board = boards[0]
# print(empty_pos)
# print(board)
# print(check_on_baord([0] * 25, get_position(board, 8)))

checker_boards = [[0]*25]*len(boards)

def p1():
    for n in numbers:
        for bi, b in enumerate(boards):
            p = get_position(b, n)
            if p is None:
                continue
            checker_boards[bi] = check_on_baord(checker_boards[bi], p)
            if is_winner(checker_boards[bi]):
                s = sum_unchecked(b, checker_boards[bi])
                print(s * n)
                return

p1()

# PART 2


def p2():
    numbers, boards = read_input(lines)
    checker_boards = [[0]*25]*len(boards)
    
    for n in numbers:
        boards = [b for bi, b in enumerate(boards) if not is_winner(checker_boards[bi])]
        checker_boards = [c for c in checker_boards if not is_winner(c)]

        for bi, b in enumerate(boards):
            p = get_position(b, n)
            if p is None:
                continue
            checker_boards[bi] = check_on_baord(checker_boards[bi], p)
            if is_winner(checker_boards[bi]) and len(boards) == 1:
                s = sum_unchecked(b, checker_boards[bi])
                print(s * n)
                return                
p2()