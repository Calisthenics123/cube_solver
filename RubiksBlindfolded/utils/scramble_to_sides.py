import pycuber as pc

def scramble_to_sides(scramble):
    # 1. 큐브 생성 및 스크램블 적용
    cube = pc.Cube()
    formula = pc.Formula(scramble)
    cube(formula)

    # 2. 각 면을 순서대로 추출
    sides = {}
    for face_name in ["U", "L", "F", "R", "B", "D"]:
        face = cube.get_face(face_name)
        # 3x3 행렬에서 각 Sticker의 색상 첫 글자 (ex: 'W', 'R') 추출
        flat_colors = [str(sticker)[1] for row in face for sticker in row]
        sides[face_name] = flat_colors

    return sides
