import math
n=22
board = {}
count=0
def Backtracking_Nqueen(q):
    for a in range(1, n+1):
        if count < 4:
            clear_board(q)
            if is_solvable(q, a):
                board[q]= a
                if (q==n):
                    print_result(board)
                else:
                    Backtracking_Nqueen(q+1)
def is_solvable(q, a):
    if (a in board.values()):
        return False
    for b in range(1,q):
        if abs(board[b]-a) == abs(b-q):
            return False
    return True
def clear_board(q):
    for a in range(q,n+1):
       board[a]=0
def print_result(result):
    for i in result:
        print (i-1, result[i]-1)
    print ('*******************')
    for i in result:
        print(i-1, result[n + 1 - i]-1)
    print ('*******************')
    global count
    count = count + 2
def main():
    Backtracking_Nqueen(1)
if __name__ == '__main__':
    main()
