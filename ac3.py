def sudokuToNode(sudoku: list, n: int) -> list:
    node = []
    domain = {}
    existing = []
    for i in range(n):
        for j in range(n):
            if sudoku[i][j] == 0:
                node.append([i, j])
                domain[(i, j)] = [i for i in range(1, n+1)]
            else:
                existing.append([sudoku[i][j], i, j])
    c = 0
    #nodo consistencia
    for i, j in domain:
        fila = [n for n, i2, j2 in existing if i2 == i]
        columna = [n for n, i2, j2 in existing if j2 == j]
        #diagonal = [n for n, i2, j2 in existing if checkDiagonal((i, j), (i2, j2))]
        cuadrante = [n for n, i2, j2 in existing if checkSquare((i, j), (i2, j2))]
        domain[(i, j)] = [n for n in domain[(i, j)] if n not in fila and n not in columna and n not in cuadrante]

    if any(len(domain[(i, j)]) == 0 for i, j in domain):
        return "Fallo nodo consistencia"

    arrayDomain = []
    arrayRestrict = []

    buf = list(domain.items())

    for i in range(len(buf)):
        pos, l = buf[i]
        arrayDomain.append(l)
        arrayRestrict.append([])
        x, y = pos
        for i2 in range(i, len(buf)):
            pos, l = buf[i2]
            x2, y2 = pos
            if (checkSquare((x, y), (x2, y2)) or x == x2 or y == y2) and (x, y) != (x2, y2):
                arrayRestrict[i].append(i2)

    newArrayRestrict = []
    for i in range(len(arrayRestrict)-1, 0-1, -1):
        for j in range(i, 0-1, -1):
            if i in arrayRestrict[j]:
                newArrayRestrict.append([i, j])

    arrayRestrict = newArrayRestrict

    return arrayDomain, arrayRestrict


def checkDiagonal(ij1:tuple, ij2:tuple) -> bool:
    i, j = ij1
    x, y = ij2
    return i-x == j-y

def getQuadrant(i: int, j: int) -> int:
    quadrant = [1, 2, 3, 4]
    if i == 0 or i == 1:
        if 3 in quadrant:
            quadrant.remove(3)
        if 4 in quadrant:
            quadrant.remove(4)
    else:
        if 1 in quadrant:
            quadrant.remove(1)
        if 2 in quadrant:
            quadrant.remove(2)
    if j == 0 or j == 1:
        if 2 in quadrant:
            quadrant.remove(2)
        if 4 in quadrant:
            quadrant.remove(4)
    else:
        if 1 in quadrant:
            quadrant.remove(1)
        if 3 in quadrant:
            quadrant.remove(3)
    return quadrant[0]

def checkSquare(pos1: tuple, pos2: tuple) -> bool:
    return getQuadrant(pos1[0], pos1[1]) == getQuadrant(pos2[0], pos2[1])
    
def revise(dI, dJ):
    delete = False
    remove = []
    for a in dI:
        if not any(a != b for b in dJ):
            delete = True
            remove.append(a)
    for a in remove:
        dI.remove(a)
    return delete

def addReverse(arrayRestrict:list) -> list:
    new = []
    for x, y in arrayRestrict:
        new.append([x, y])
        new.append([y, x])
    return new


def ac3(arrayDomain:list, arrayRestrict:list) -> list:
    queue = arrayRestrict.copy()
    queue.reverse()
    while queue:
        old = len(queue)
        #print([[x+1, y+1] for x, y in queue])
        x, y = queue.pop(0)
        b = revise(arrayDomain[x], arrayDomain[y])
        if b:
            if any(x2 == x for x2, y2 in arrayRestrict if [x2, y2] not in queue):
                buf = [[x2, y2] for x2, y2 in arrayRestrict if [x2, y2] not in queue and x2 == x]
                if buf:
                    queue.extend(buf)
    return arrayDomain
            

fp = open("sudoku.txt", "r")
s = []
for l in fp:
    l = l.strip().split(" ")
    l = [int(i) for i in l]
    s.append(l)
fp.close()

n = len(s) #Asumimos que el sudoku es cuadrado

arrayDomain, arrayRestrict = sudokuToNode(s, n)
arrayRestrict = addReverse(arrayRestrict)
print(ac3(arrayDomain, arrayRestrict))