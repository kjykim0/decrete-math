import time

# 행렬 출력
def printMatrix(mat):
    for i in range(5):
        for j in range(5):
            print(mat[i][j], end=" ")
        print()

# 행렬 부울곱
def boolProduct(mat1, mat2):
    boolMat = [[0 for _ in range(5)] for _ in range (5)]
    for i in range(5):
        for j in range(5):
            for k in range(5):
                if mat1[i][k] == 1 and mat2[k][j] == 1:
                    boolMat[i][j] = 1
                    break
    return boolMat
                    
# 반사 관계 판별
def judgeReflect(mat):
    for i in range(5):
        if(mat[i][i] == 0):
            return False
    return True

# 대칭 관계 판별
def judgeSymmetry(mat):
    for i in range(5):
        for j in range(i + 1, 5):
            if(mat[i][j] != mat[j][i]):
                return False
    return True
    
# 추이 관계 판별
def judgeTransitive(mat):
    matSquare = boolProduct(mat, mat)
    for i in range(5):
        for j in range(5):
            if matSquare[i][j] == 1 and mat[i][j] == 0:
                return False
    return True

# 동치 판별
def judgeEqual(mat):
    return judgeReflect(mat) and judgeSymmetry(mat) and judgeTransitive(mat)

# 동치류 구하기
def findEquvalanceClass(mat):
    print("동치류:")
    for i in range(5):
        print(f"[{i + 1}]: {{", end="")
        equvalance = []
        for j in range(5):
            if mat[i][j] == 1:
                equvalance.append(j + 1)
        for j in range(len(equvalance)):
            print(equvalance[j], end="")
            if j < len(equvalance) - 1:
                print(", ", end="")
        print("}")
    
# 반사폐포 구하기
def reflectionClosure(mat):
    reflectionMat = [row[:] for row in mat]
    for i in range(5):
        reflectionMat[i][i] = 1
    return reflectionMat
        
# 대칭폐포 구하기
def symmetricClosure(mat):
    symmetricMat = [row[:] for row in mat]
    for i in range(5):
        for j in range(5):
            if mat[i][j] == 1:
                symmetricMat[j][i] = mat[i][j]
    return symmetricMat

# 와샬 알고리즘을 이용한 추이폐포 구하기
def transitiveClosureWarshall(mat):
    start = time.perf_counter()
    transitiveMat = [row[:] for row in mat]
    for k in range(5):
        for i in range(5):
            for j in range(5):
                if(transitiveMat[i][j] == 0 and transitiveMat[i][k] == 1 and transitiveMat[k][j] == 1):
                    transitiveMat[i][j] = 1
    end = time.perf_counter()
    print(f"소요 시간: {(end - start) * 1000:.3f}ms")
    return transitiveMat

# 합집합
def unionMat(mat1, mat2):
    for i in range(5):
        for j in range(5):
            if(mat1[i][j] == 1 or mat2[i][j] == 1):
                mat1[i][j] = 1

# 연결관계를 이용한 추이폐포 구하기
def transitiveClosureConnection(mat):
    start = time.perf_counter()
    transitiveMat = [row[:] for row in mat]
    for i in range(5):
        connectionMat = boolProduct(transitiveMat, mat)
        unionMat(transitiveMat, connectionMat)
    end = time.perf_counter()
    print(f"소요 시간: {(end - start) * 1000:.3f}ms")
    return transitiveMat

# 관계행렬 비교
def compareMatrix(mat1, mat2):
    for i in range(5):
        for j in range(5):
            if(mat1[i][j] != mat2[i][j]):
                return False
    return True

# main함수
def main():
    mat = []
    print("집합 A{1, 2, 3, 4, 5} 에 대한 관계 R의 관계행렬을 입력하세요. (5x5)")
    for i in range(5):
        mat.append(list(map(int, input().split())))
    if judgeEqual(mat):
        print("관계 R은 동치관계입니다.")
        findEquvalanceClass(mat)
    
    else:
        print("관계 R은 동치관계가 아닙니다.")
        
    if judgeReflect(mat):
        print("관계 R은 반사관계입니다.")
    else:
        print("관계 R은 반사관계가 아닙니다.")
        print("폐포 변환 전:")
        printMatrix(mat)
        reflectMat = reflectionClosure(mat)
        print("반사폐포:")
        printMatrix(reflectMat)
        if judgeEqual(reflectMat):
            print("관계 R의 반사폐포는 동치관계입니다.")
            findEquvalanceClass(reflectMat)
        else:
            print("관계 R의 반사폐포는 동치관계가 아닙니다.")
        
    if judgeSymmetry(mat):
        print("관계 R은 대칭관계입니다.")
    else:
        print("관계 R은 대칭관계가 아닙니다.")
        print("폐포 변환 전:")
        printMatrix(mat)
        symmetricMat = symmetricClosure(mat)
        print("대칭폐포:")
        printMatrix(symmetricMat)
        if judgeEqual(symmetricMat):
            print("관계 R의 대칭폐포는 동치관계입니다.")
            findEquvalanceClass(symmetricMat)
        else:
            print("관계 R의 대칭폐포는 동치관계가 아닙니다.")
        
    if judgeTransitive(mat):
            print("관계 R은 추이관계입니다.")
    else:
        print("관계 R은 추이관계가 아닙니다.")
        print("폐포 변환 전:")
        printMatrix(mat)
        print("와샬 알고리즘으로 구한 추이폐포:")
        transitiveMatWarshall = transitiveClosureWarshall(mat)
        printMatrix(transitiveMatWarshall)
        if judgeEqual(transitiveMatWarshall):
            print("관계 R의 추이폐포는 동치관계입니다.")
            findEquvalanceClass(transitiveMatWarshall)
        else:
            print("관계 R의 추이폐포는 동치관계가 아닙니다.")
        print("연결관계를 통해 구한 추이폐포:")
        transitiveMatConnection = transitiveClosureConnection(mat)
        printMatrix(transitiveMatConnection)
        if compareMatrix(transitiveMatWarshall, transitiveMatConnection):
            print("와샬 알고리즘을 통해 구한 추이폐포는 연결관계를 통해 구한 추이폐포와 같습니다.")
        else:
            print("와샬 알고리즘을 통해 구한 추이폐포는 연결관계를 통해 구한 추이폐포와 다릅니다.")
    
main()