import pycuber as pc

def solve_white_cross(scramble):
    cube = pc.Cube()
    formula = pc.Formula(scramble)
    cube(formula)

    moves = []

    def apply(m):
        nonlocal cube, moves
        cube(pc.Formula(m))
        moves.append(m)

    def move_white_edge_to_down(face_name, pos):
        color = str(cube.get_face(face_name)[pos[0]][pos[1]])
        if color != 'W':
            return

        if face_name == 'U':
            if pos == (0, 1): apply("U'"); apply("L'"); apply("D"); apply("L")
            elif pos == (1, 0): apply("U"); apply("B'"); apply("D"); apply("B")
            elif pos == (1, 2): apply("U'"); apply("F'"); apply("D"); apply("F")
            elif pos == (2, 1): apply("U"); apply("R'"); apply("D"); apply("R")
        elif face_name == 'F':
            if pos == (0, 1): apply("F'"); apply("U'"); apply("R'"); apply("U"); apply("R"); apply("F")
            elif pos == (1, 0): apply("L'"); apply("U"); apply("L")
            elif pos == (1, 2): apply("R"); apply("U'"); apply("R'")
            elif pos == (2, 1): apply("F"); apply("F")
        elif face_name == 'R':
            if pos == (0, 1): apply("R'"); apply("U'"); apply("B'"); apply("U"); apply("B"); apply("R")
            elif pos == (1, 0): apply("F'"); apply("U"); apply("F")
            elif pos == (1, 2): apply("B"); apply("U'"); apply("B'")
            elif pos == (2, 1): apply("R"); apply("R")
        elif face_name == 'L':
            if pos == (0, 1): apply("L'"); apply("U'"); apply("F'"); apply("U"); apply("F"); apply("L")
            elif pos == (1, 0): apply("B'"); apply("U"); apply("B")
            elif pos == (1, 2): apply("F"); apply("U'"); apply("F'")
            elif pos == (2, 1): apply("L"); apply("L")
        elif face_name == 'B':
            if pos == (0, 1): apply("B'"); apply("U'"); apply("L'"); apply("U"); apply("L"); apply("B")
            elif pos == (1, 0): apply("R'"); apply("U"); apply("R")
            elif pos == (1, 2): apply("L"); apply("U'"); apply("L'")
            elif pos == (2, 1): apply("B"); apply("B")

    # Step 1: 엣지를 D면으로 이동
    for face in ['U', 'F', 'R', 'L', 'B']:
        for pos in [(0, 1), (1, 0), (1, 2), (2, 1)]:
            move_white_edge_to_down(face, pos)

    # Step 2: D면에서 옆면 센터와 정렬
    d_face = cube.get_face('D')
    centers = {
        'F': str(cube.get_face('F')[1][1]),
        'R': str(cube.get_face('R')[1][1]),
        'B': str(cube.get_face('B')[1][1]),
        'L': str(cube.get_face('L')[1][1]),
    }

    # D면 edge 위치별 색상 확인 → 회전 정렬
    def rotate_d_until_match():
        for _ in range(4):
            front = str(cube.get_face('F')[2][1])
            if front == centers['F']:
                return
            apply("D")

    for _ in range(4):
        front = str(cube.get_face('F')[2][1])
        if front != centers['F']:
            rotate_d_until_match()
        apply("F"); apply("F")  # 올려주기
        apply("D")

    return ' '.join(moves)
