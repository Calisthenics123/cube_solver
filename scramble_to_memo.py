from rubik.cube import Cube
import requests
import json

def scramble_to_sides(scramble):
    cube = Cube()
    cube.sequence(scramble)
    faces = cube.faces

    face_names = ['U', 'R', 'F', 'D', 'B', 'L']
    sides = {}
    for i, face in enumerate(face_names):
        sides[face] = [faces[i][j] for j in range(9)]
    return sides

def send_to_server(sides):
    url = "http://127.0.0.1:5000/get_memo"
    headers = {"Content-Type": "application/json"}
    data = {"sides": sides}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    scramble = input("스크램블을 입력하세요 (예: R U R' U'): ")
    sides = scramble_to_sides(scramble)
    result = send_to_server(sides)
    print("\n✅ 결과:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
