from flask import Flask, request, jsonify
from RubiksSolver import solver, move  # 패키지 이름에 맞게 조정

app = Flask(__name__)

@app.route('/solve', methods=['GET', 'POST'])
def solve():
    if request.method == 'GET':
        return '✅ Server is awake and ready!'  # 간단 응답 (모니터링용)
        
    if request.method == 'POST':    
    data = request.get_json()
    scramble = data['scramble']
    print("서버에서 받은 스크램블:", scramble)

    # 기본 (노란색 위 기준)
    solution_yellow = solver.solve_F2L(
        scramble=scramble,
        rotation="",
        solve_BL=False,
        solve_BR=False,
        solve_FR=False,
        solve_FL=False,
        max_length=8,
        full_search=False,
        sol_index=1,
        name="yellow_top_cross",
        move_restrict=move.move_UDLRFB
    )

    # 흰색이 위, 초록색이 앞 기준
    solution_white = solver.solve_F2L(
        scramble=scramble,
        rotation="x2 y2",
        solve_BL=False,
        solve_BR=False,
        solve_FR=False,
        solve_FL=False,
        max_length=8,
        full_search=False,
        sol_index=1,
        name="white_top_cross",
        move_restrict=move.move_UDLRFB
    )

    return jsonify({
        'yellow_top': solution_yellow,
        'white_top': solution_white,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
