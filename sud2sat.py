import sys

#Turns a string of literals into a clause by zero terminating it
def clause(c):
    return str(c + ' 0\n')

#Turns a base 9 xyz number into a string literal
def lit(n):
    return str(n+1)

#Accepts a sudoku puzzle in the form of a list of 9 9 digit strings
#Returns a string containing the clauses formatted as minisat input
def build(puzzle):
    clauses = ''
    clause_count = 0

    #Builds unit clauses based on content of original puzzle
    clauses += 'c unit clauses\n'
    #i and j are x,y indices of predefined numbers in sudoku puzzle
    for i in range(0, 9):
        for j in range(0, 9):
            if puzzle[i][j] != '0':
                clauses += clause(str(i * 81 + j * 9 + int(puzzle[i][j])))
                clause_count += 1

    #Builds 81 ninary clauses ensuring each cell has at least one number
    clauses += 'c cells\n'
    #x and y are indices of each cell in sudoku puzzle
    for x in range(0, 9):
        for y in range(0, 9):
            #z is value of each possible digit, range 0-8
            for z in range(0, 9):
                clauses += lit(x * 81 + y * 9 + z) + ' '
            clauses += '0\n'
            clause_count += 1

    #Builds 2916 binary clauses ensuring each number appears in a column at most once
    clauses += 'c columns\n'
    #x, y and z are as above. i is y index of second cell in column
    for x in range (0, 9):
        for y in range (0, 9):
            for z in range(0, 9):
                for i in range(x+1, 9):
                        clauses += '-' + lit(x * 81 + y * 9 + z * 1) + ' '
                        clauses += '-' + lit(i * 81 + y * 9 + z * 1) + ' 0\n'
                        clause_count += 1

    #Builds 2916 binary clauses ensuring each number appears in a row at most once
    clauses += 'c rows\n'
    #x, y and z are as above. i is x index of second cell in row
    for x in range (0, 9):
        for y in range (0, 9):
            for z in range(0, 9):
                for i in range(y+1, 9):
                        clauses += '-' + lit(x * 81 + y * 9 + z * 1) + ' '
                        clauses += '-' + lit(x * 81 + i * 9 + z * 1) + ' 0\n'
                        clause_count += 1

    #Builds 2916 binary clauses ensuring each number appears in a subgrid at most once
    clauses += 'c subgrids\n'
    #z is as above
    for z in range(0, 9):
        #i and j are index 3x3 of subgrid
        for i in range(0, 3):
            for j in range(0, 3):
                #x and y are index of first cell within subgrid
                for x in range(0, 3):
                    for y in range(0, 3):
                        #k and l are index of second cell within subgrid
                        for k in range(x, 3):
                            for l in range(0, 3):
                                #clauses are only generated for second cells that come after the first cell,
                                #to avoid some duplicate clauses
                                if k > x or l > y:
                                    clauses += '-' + lit((3*i + x) * 81 + (3*j + y) * 9 + z * 1) + ' '
                                    clauses += '-' + lit((3*i + k) * 81 + (3*j + l) * 9 + z * 1) + ' 0\n'
                                    clause_count += 1

    #print(clause_count)
    return clause_count, clauses

def main():
    if(len(sys.argv)) > 1:
        input = sys.argv[1]
        print('Attempting to read puzzles from ' + input)
    else:
        input = 'p096_sudoku.txt'
        print('Attempting to read puzzles from p096_sudoku.txt. If puzzles elsewhere, please specify.')
    if(len(sys.argv)) > 2:
        output = sys.argv[2]
    else:
        output = 'in.in'
    if(len(sys.argv)) > 3:
        puz_num = int(sys.argv[3])
    else:
        puz_num = 1
    #Opens first argument as file to read puzzle
    f = open(sys.argv[1], 'r')
    lines = []
    for line in f:
        #only grabs numerical lines
        if line[0].isdigit():
            #indexed to remove new line symbol
            lines += [line[:9]]
    f.close()
    start = 9 * (puz_num - 1)
    #Checks if arguments include puzzle number
    #Reads first 9 numeric lines in as sudoku puzzle
    puzzle = lines[start:start+9]
    #Calls build() to translate puzzle into clauses
    clause_count, clauses = build(puzzle)
    #Saves clauses from build() into file specified by second argument

    f = open(sys.argv[2], 'w')
    f.write('p cnf 729 ' + str(clause_count) + '\n')
    f.write(clauses)
    f.close()
    print('Output saved to ' + output)

if __name__ == '__main__':
    main()
