from flask import Flask, request, jsonify
import RubiksBlindfolded
from RubiksBlindfolded.utils.color_to_face_mapper import map_colors_to_faces 
from RubiksBlindfolded.utils.scramble_to_sides import scramble_to_sides
from flask import Response
import json

app = Flask(__name__)

# 한글 매핑 딕셔너리
edge_map = {
    'U1B1': 'ㄱ', 'U5R1': 'ㄴ', 'U7F1': 'ㄷ', 'U3L1': 'ㄹ',
    'L1U3': 'ㅁ', 'L5F3': 'ㅂ', 'L7D3': 'ㅅ', 'L3B5': 'ㅇ',
    'F1U7': 'ㅈ', 'F5R3': 'ㅊ', 'F7D1': 'ㅌ', 'F3L5': 'ㅎ',
    'R1U5': "ㄱ'", 'R5B3': "ㄴ'", 'R7D5': "ㄷ'", 'R3F5': "ㄹ'",
    'B1U1': "ㅁ'", 'B5L3': "ㅂ'", 'B7D7': "ㅅ'", 'B3R5': "ㅇ'",
    'D1F7': "ㅈ'", 'D5R7': "ㅊ'", 'D7B7': "ㅌ'", 'D3L7': "ㅎ'"
}

corner_map = {
    'U0B2L0': 'ㄱ', 'U2R2B0': 'ㄴ', 'U8F2R0': 'ㄷ', 'U6L2F0': 'ㄹ',
    'L0U0B2': 'ㅁ', 'L2F0U6': 'ㅂ', 'L8D0F6': 'ㅅ', 'L6B8D6': 'ㅇ',
    'F0U6L2': 'ㅈ', 'F2R0U8': 'ㅊ', 'F8D2R6': 'ㅌ', 'F6L8D0': 'ㅎ',
    'R0U8F2': "ㄱ'", 'R2B0U2': "ㄴ'", 'R8D8B6': "ㄷ'", 'R6F8D2': "ㄹ'",
    'B0U2R2': "ㅁ'", 'B2L0U0': "ㅂ'", 'B8D6L6': "ㅅ'", 'B6R8D8': "ㅇ'",
    'D0F6L8': "ㅈ'", 'D2R6F8': "ㅊ'", 'D8B6R8': "ㅌ'", 'D6L6B8': "ㅎ'"
}


@app.route('/get_memo', methods=['POST'])
def get_memo():
    print("✅ 요청 도착!", flush=True)
    data = request.get_json()
    scramble = data.get("scramble")
    sides = data.get("sides")
    color_map = data.get("color_map")

    if scramble:
        face_sides = scramble_to_sides(scramble)

    else:
        return jsonify({"error": "❌ 'scramble'만 지원 중입니다. sides/color_map은 현재 비활성화 상태입니다."}), 400


    RubiksBlindfolded.reset()
    RubiksBlindfolded.setCube(face_sides)

    print("🧪 [app.py] RubiksBlindfolded.solveEdges() 호출 직전", flush=True)
    edges = RubiksBlindfolded.solveEdges()
    print("📤 [app.py] edges 리턴 =", edges, flush=True)

    print("🧪 [app.py] RubiksBlindfolded.solveCorners() 호출 직전", flush=True)
    corners = RubiksBlindfolded.solveCorners()
    print("📤 [app.py] corners 리턴 =", corners, flush=True)

    edge_memo = [''.join(map(str, e)) for e in edges] if edges else []
    corner_memo = [''.join(map(str, c)) for c in corners] if corners else []

    edge_hangul = [edge_map.get(e, e) for e in edge_memo]
    corner_hangul = [corner_map.get(c, c) for c in corner_memo]

    return Response(
        json.dumps({
            "edges": edge_memo,
            "corners": corner_memo,
            "edges_hangul": edge_hangul,
            "corners_hangul": corner_hangul
        }, ensure_ascii=False, indent=2),
        content_type='application/json'
    )


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)
