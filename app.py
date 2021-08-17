import flask
from flask import Flask, request, jsonify, render_template, url_for, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', message=" Fill The Board With Numbers You Have")


@app.route('/solved', methods=['GET'])
def solved(board):
    return render_template('solved.html', board=board)


@app.route('/solve', methods=['POST'])
def set_sudoku():
    data = request.form['board']
    print("Data received")
    print(data)
    data = data.replace(",", "")
    if len(data) > 81:
        return redirect(url_for('index'))

    board = [[], [], [], [], [], [], [], [], []]
    x = 0

    for i in range(9):
        for j in range(9):
            if 10 > int(data[x]) >= 0:
                board[i].append(int(data[x]))
            else:
                board[i].append(0)
            x = x + 1
    if not check_valid_input_board(board):
        return render_template('index.html', message="Error : !!!! The Board You entered is invalid !!!!")
    print(board)
    solve(board)
    print(board)
    return render_template('solved.html', board=board)


def check_valid_input_board(board):
    for i in range(9):
        for j in range(9):
            set_of_row = set()
            if board[i][j] != 0 and board[i][j] in set_of_row:
                return False
            else:
                set_of_row.add(board[i][j])
    return True


def find_empty(board):
    for i in range(len(board)):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def is_valid(board, number, position):
    for i in range(len(board)):
        if board[position[0]][i] == number and position[1] != i:
            return False

    for i in range(len(board)):
        if board[i][position[1]] == number and position[0] != i:
            return False

    square_x = position[1] // 3
    square_y = position[0] // 3

    for i in range(square_y * 3, square_y * 3 + 3):
        for j in range(square_x * 3, square_x * 3 + 3):
            if board[i][j] == number and (i, j) != position:
                return False

    return True


def solve(board):
    empty = find_empty(board)

    if not empty:
        return True
    else:
        row, column = empty

    for i in range(1, 10):
        if is_valid(board, i, (row, column)):
            board[row][column] = i

            if solve(board):
                return True

            board[row][column] = 0
    return False


if __name__ == '__main__':
    app.run()
