from fractions import Fraction

# 행렬 출력
def printMatrix(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            print(f"{mat[i][j]:.2f}", end = ' ')
        print()
        
def printFracMatrix(mat):
    for i in range(len(mat)):
            for j in range(len(mat[0])):
                a = mat[i][j]
                if a.denominator == 1:
                    print(f"{a.numerator}", end=' ')
                else:
                    print(f"{a.numerator}/{a.denominator}", end=' ')
            print()

# 소행렬 제작
def makeMinorMatrix(i, j, mat):
    return [row[:j] + row[j + 1:] for row in (mat[:i] + mat[i + 1:])]

# 전치행렬 제작
def makeTransposedMatrix(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]

# 행렬식 계산
def calculateDeterminant(mat):
    if len(mat) == 1:
        return mat[0][0]
    if len(mat) == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
    
    det = 0
    for c in range(len(mat)):
        det += ((-1) ** c) * mat[0][c] * calculateDeterminant(makeMinorMatrix(0, c, mat))
    return det

# 역행렬 존재 확인(행렬식 이용)
def hasInverse(mat):
    det = calculateDeterminant(mat)
    if abs(det) < 1e-7:
        print("해당 행렬의 행렬식은 0입니다.")
        print("역행렬이 존재하지 않습니다.")
        return False
    return True

def hasFracInverse(mat):
    det = calculateDeterminant(mat)
    if abs(det) == 0:
        print("해당 행렬의 행렬식은 0입니다.")
        print("역행렬이 존재하지 않습니다.")
        return False
    return True

# 행렬식을 이용한 역행렬 구하기
def determinantInv(mat):
    det = calculateDeterminant(mat)

    if(len(mat) == 1):
        return [[1.0 / mat[0][0]]]
    if(len(mat) == 2):
        return [[mat[1][1] / det, (-1) * mat[0][1] / det],
                [(-1) * mat[1][0] / det, mat[0][0] / det]]
    
    inv = []
    
    for i in range(len(mat)):
        invRow = []
        for j in range(len(mat)):
            invRow.append(((-1) ** (i + j)) * calculateDeterminant(makeMinorMatrix(i, j, mat)) / det)
        inv.append(invRow)
    inv = makeTransposedMatrix(inv)
    return inv
        
def swapRow(r1, r2, mat):
    temp = mat[r1]
    mat[r1] = mat[r2]
    mat[r2] = temp

# 가우스-조던 소거법을 이용한 역행렬 구하기
def gausJordanInv(n, mat):
    aug = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(mat)]
    
    for i in range(n):
        isPivot = False
        for row in range(i, n):
            if abs(aug[row][i]) > 1e-7:
                isPivot = True
                swapRow(i, row, aug)
                pivot = aug[i][i]
                for j in range(2 * n):
                    aug[i][j] /= pivot
                for k in range(i + 1, n):
                    mul = aug[k][i]
                    for j in range(2 * n):
                        aug[k][j] -= mul * aug[i][j]    
                break    
        if(not isPivot):
            print("역행렬이 존재하지 않습니다.")
            return False
            
    
    for i in range(n - 1, -1, -1):
        for k in range(i - 1, -1, -1):
            mul = aug[k][i]
            for j in range(2 * n):
                aug[k][j] -= mul * aug[i][j]   
    inv = [row[n:] for row in aug]
    
    return inv

def fracGausJordanInv(n, mat):
    aug = [[Fraction(x) for x in row] + [Fraction(1) if i == j else Fraction(0) for j in range(n)] for i, row in enumerate(mat)]
    
    for i in range(n):
        isPivot = False
        for row in range(i, n):
            if aug[row][i] != 0:
                isPivot = True
                swapRow(i, row, aug)
                pivot = aug[i][i]
                for j in range(2 * n):
                    aug[i][j] /= pivot
                for k in range(i + 1, n):
                    mul = aug[k][i]
                    for j in range(2 * n):
                        aug[k][j] -= mul * aug[i][j]    
                break    
        if(not isPivot):
            print("역행렬이 존재하지 않습니다.")
            return False
            
    
    for i in range(n - 1, -1, -1):
        for k in range(i - 1, -1, -1):
            mul = aug[k][i]
            for j in range(2 * n):
                aug[k][j] -= mul * aug[i][j]   
    inv = [row[n:] for row in aug]
    
    return inv

# 행렬식을 이용하여 역행렬과 가우스-조던 소거법을 이용하여 구한 역행렬 비교
def compareMatrix(mat1, mat2):
    if len(mat1) != len(mat2):
        return False
    n = len(mat1)
    for i in range(n):
        for j in range(n):
            if abs(mat1[i][j] - mat2[i][j]) > 1e-7:
                return False
    return True

def compareFracMatrix(mat1, mat2):
    if len(mat1) != len(mat2):
        return False
    n = len(mat1)
    for i in range(n):
        for j in range(n):
            if mat1[i][j] != mat2[i][j]:
                return False
    return True

# 행렬 복구
def fixMatrix(mat1, mat2, n):
    fixed = [[0] * n for i in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                fixed[i][j] += mat1[i][k] * mat2[k][j]
    return fixed

def checkUnit(mat):
    for i in range(len(mat)):
        for j in range(len(mat)):
            if i == j and mat[i][j] != 1:
                return False
            elif i != j and mat[i][j] != 0:
                return False
    return True
                

# main함수
def main():
    n = int(input("정방행렬의 차수를 입력하세요: "))
    mat = []
    fracMat = []
    for i in range(n):
        row = input(f'{i + 1}행: ').split()
        mat.append([float(x) for x in row]) 
        fracMat.append([Fraction(x) for x in row])
    
    existDetInv = False
    existGausInv = False
    existFracDetInv = False
    existFracGausInv = False
    
    # 행렬식을 이용하여 역행렬 구하기
    print("행렬식을 이용하여 구한 역행렬:")
    if(hasInverse(mat)):
        existDetInv = True
        inv1 = determinantInv(mat)
        printMatrix(inv1)
    print()
    
    # 가우스-조던 소거법을 이용하여 역행렬 구하기
    print("가우스-조던 소거법을 이용하여 구한 역행렬:")
    inv2 = gausJordanInv(n, mat)
    if(inv2):    
        existGausInv = True
        printMatrix(inv2)
    print()
    
    # 두 방법 결과 비교    
    if not existDetInv or not existGausInv:
            if existDetInv == existGausInv:
                print("두 방법의 결과가 동일합니다.")
            else:
                print("두 방법의 결과가 동일하지 않습니다.")
    else:
        if compareMatrix(inv1, inv2):
            print("두 방법의 결과가 동일합니다.")
        else:
            print("두 방법의 결과가 동일하지 않습니다.")
            
    print("분수를 이용한 역행렬 구하기")
    
# 행렬식을 이용하여 역행렬 구하기
    print("행렬식을 이용하여 구한 역행렬:")
    if(hasFracInverse(fracMat)):
        existFracDetInv = True
        fracInv1 = determinantInv(fracMat)
        printFracMatrix(fracInv1)
    print()
    
    # 가우스-조던 소거법을 이용하여 역행렬 구하기
    print("가우스-조던 소거법을 이용하여 구한 역행렬:")
    fracInv2 = fracGausJordanInv(n, fracMat)
    if(fracInv2):    
        existFracGausInv = True
        printFracMatrix(fracInv2)
    print()
    
    # 두 방법 결과 비교    
    if not existFracDetInv or not existFracGausInv:
            if existFracDetInv == existFracGausInv:
                print("두 방법의 결과가 동일합니다.")
            else:
                print("두 방법의 결과가 동일하지 않습니다.")
    else:
        if compareFracMatrix(fracInv1, fracInv2):
            print("두 방법의 결과가 동일합니다.")
        else:
            print("두 방법의 결과가 동일하지 않습니다.")
            
         # 역행렬 체크
        fixed1 = fixMatrix(fracMat, fracInv1, n)
        if checkUnit(fixed1):
            printFracMatrix(fixed1)
            print("원본행렬과 방법 1로 구한 행렬의 곱은 단위행렬입니다.")
            print("방법 1로 구한 행렬은 역행렬이 맞습니다.")
        fixed2 = fixMatrix(fracMat, fracInv2, n)
        if checkUnit(fixed2):
            printFracMatrix(fixed1)
            print("원본행렬과 방법 2로 구한 행렬의 곱은 단위행렬입니다.")
            print("방법 2로 구한 행렬은 역행렬이 맞습니다.")
        
# 프로그램 시작
if __name__ == "__main__":
    main()
    