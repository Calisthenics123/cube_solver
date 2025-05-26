import pycuber as pc

def get_kociemba_string(scramble):
    # 각 face에 대한 색상 문자 지정
    color_map = {
        'U': 'U', 'R': 'R', 'F': 'F',
        'D': 'D', 'L': 'L', 'B': 'B',
    }

    cube = pc.Cube()
    formula = pc.Formula(scramble)
    cube(formula)

    face_order = ['U', 'R', 'F', 'D', 'L', 'B']
    facelets = ''

    for face in face_order:
        face_matrix = cube.get_face(face)
        for row in face_matrix:
            for sticker in row:
                  facelets += color_map[face]

    print("🎯 최종 facelets:", facelets)
    print("길이:", len(facelets))
    color_count = {c: facelets.count(c) for c in "URFDLB"}
    print("색상 개수:", color_count)

    if len(facelets) != 54 or any(count != 9 for count in color_count.values()):
        raise ValueError("🚨 큐브 문자열 형식 오류")

    return facelets
