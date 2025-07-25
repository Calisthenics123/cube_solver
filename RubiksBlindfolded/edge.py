class Edge:

    def getEdgeSequence(self):
        return self.edgeSequence

    def __init__(self):
        self.edgeSequence = []
        # 목표 엣지 순서 (순서대로 해결해야 할 엣지의 위치들)
        self.target_order = [                                                             # ('F', 7, 'D', 1),    ('D', 1, 'F', 7),  제거
            ('U', 1, 'B', 1), ('U', 5, 'R', 1), ('U', 7, 'F', 1), ('U', 3, 'L', 1),
            ('L', 1, 'U', 3), ('L', 5, 'F', 3), ('L', 7, 'D', 3), ('L', 3, 'B', 5),
            ('F', 1, 'U', 7), ('F', 5, 'R', 3),  ('F', 3, 'L', 5),
            ('R', 1, 'U', 5), ('R', 5, 'B', 3), ('R', 7, 'D', 5), ('R', 3, 'F', 5),
            ('B', 1, 'U', 1), ('B', 5, 'L', 3), ('B', 7, 'D', 7), ('B', 3, 'R', 5),
            ('D', 5, 'R', 7), ('D', 7, 'B', 7), ('D', 3, 'L', 7)
        ]
        self.skip_once = True              # 처음엔 한 바퀴 건너뛰기
        self.last_buffer_color = None    # 이전 버퍼 색상 기억

    def get_buffer_colors(self, sides):
        # 버퍼 색상 얻기
        return [sides['D'][1], sides['F'][7]]
    

    def get_center_color(self, sides, face):      # 면 이름 → 해당 면의 중심 색상 (예: 'U' -> 'W')
        return sides[face][4]  # 각 면의 중심은 항상 index 4


    def is_edge_solved(self, sides, f1, i1, f2, i2, corners):          # 엣지가 이미 맞았는지 체크 (양쪽 색상 비교)
        c1 = sides[f1][i1]        # 실제 색상
        c2 = sides[f2][i2]

        expected1_color = self.get_center_color(sides, f1)  
        expected2_color = self.get_center_color(sides, f2)
        print(f"🧪 검사 중: {f1}{i1}={c1} vs {expected1_color}, {f2}{i2}={c2} vs {expected2_color}")

        if len(corners) % 2 == 0:
            if c1 == expected1_color and c2 == expected2_color:    
                print(f"✅ 이미 맞은 엣지: {f1}{i1}, {f2}{i2}")
                return True
            return False

        else:
            if (f1, i1, f2, i2) == ('U', 1, 'B', 1):
                if c1 == 'y' and c2 == 'r':
                    return True
                else:
                    return False

            if (f1, i1, f2, i2) == ('U', 3, 'L', 1):
                if c1 == 'y' and c2 == 'b':
                    return True
                else:
                    return False

            if (f1, i1, f2, i2) == ('L', 1, 'U', 3):
                if c1 == 'b' and c2 == 'y':
                    return True
                else:
                    return False

            if (f1, i1, f2, i2) == ('B', 1, 'U', 1):
                if c1 == 'r' and c2 == 'y':
                    return True
                else:
                    return False

        return c1 == expected1_color and c2 == expected2_color



    def find_piece(self, current_colors, sides, corners):            # 색상에 맞는 엣지를 찾아서 반환 (이미 맞은 엣지는 제외), 이건 이미 버퍼가 다 맞았을때 기준
        for f1, i1, f2, i2 in self.target_order:                      # ㄱ,ㄴ,ㄷ 순서대로 (f1i1..)에 불러넣기
            if self.is_edge_solved(sides, f1, i1, f2, i2, corners):                #  ㄱ,ㄴ,ㄷ들이 가운데 색상과 일치하는가?
                continue                                                        # 이미 맞은 엣지는 건너뛰기

            t1, t2 = current_colors                                           # current_color=self.get_buffer_colors(sides) 버퍼에 있는 색상들+
            expected1_color = self.get_center_color(sides, f1)  
            expected2_color = self.get_center_color(sides, f2)

            print(f"🧩 중앙의 색깔은 {expected1_color}, {expected2_color} // 현재버퍼의 색상 {t1}, {t2}")     

            if sorted([t1, t2]) == sorted(["g", "w"]):       # 버퍼에 이미 올바른 버퍼가 있을 경우
                print("💡 버퍼가 DF입니다.")
                for tf1, ti1, tf2, ti2 in self.target_order:

                    if self.is_edge_solved(sides, tf1, ti1, tf2, ti2, corners):
                        print("이미 풀린 엣지가 있어여")
                        continue 
                    tc1, tc2 = sides[tf1][ti1], sides[tf2][ti2]    # ㄱ,ㄴ,ㄷ 중에서 차례로 임의의 것을 불러옴
                    expected1 = self.get_center_color(sides, tf1)
                    expected2 = self.get_center_color(sides, tf2)
                    print(f"🔍 검사 중 엣지: {tf1}{ti1},{tf2}{ti2} / 색상: {tc1}, {tc2} / 중심: {expected1}, {expected2}")

                    return tf1, ti1, tf2, ti2  # 실제 위치 리턴

            if len(corners) % 2 == 0:
                if t1 == expected1_color and t2 == expected2_color:         # 원래에 있어야하는 색상과 같을때
                    #print(f"출력하려는 색상: {f1}{i1}, {f2}{i2}")
                    return f1, i1, f2, i2                                                        # ㄱ,ㄴ,ㄷ 들이 버퍼의 색상과 동일하면 값을 돌려준다.
            else:
                # 🔵 코너 홀수: 특수 조각 수동 처리
                if sorted([t1, t2]) == ['b', 'y']:
                    if t1 == 'y' and t2 == 'b':
                        return ('U', 3, 'L', 1)
                    if t1 == 'b' and t2 == 'y':
                        return ('L', 1, 'U', 3)

                if sorted([t1, t2]) == ['r', 'y']:
                    if t1 == 'y' and t2 == 'r':
                        return ('U', 1, 'B', 1)
                    if t1 == 'r' and t2 == 'y':
                        return ('B', 1, 'U', 1)

                # 🔁 위 조건에 해당하지 않으면 기본 방식으로 진행
                if t1 == expected1_color and t2 == expected2_color:
                    # print(f"✅ 홀수코너: 정답 위치 {f1}{i1}, {f2}{i2}")
                    return f1, i1, f2, i2

    def all_edges_solved(self, sides, corners):      # 모든 엣지가 맞는지 확인하는 함수
        for f1, i1, f2, i2 in self.target_order:
            if not self.is_edge_solved(sides, f1, i1, f2, i2, corners):
                return False
        return True



    def solveEdge(self, sides, edge, corners):         # 메인 함수
        visited = set()
        loop_count = 0
        loop_limit = 20  # 최대 반복 횟수

        while loop_count < loop_limit:     # 20번 동안 아래의 상황을 반복한다.
            loop_count += 1

            current_colors = self.get_buffer_colors(sides)     # 불러지는 값은 [sides['D'][1], sides['F'][7]]
            next_target = self.find_piece(current_colors, sides, corners)

            if not next_target:
                continue

            f1, i1, f2, i2 = next_target
            target_colors = [sides[f1][i1], sides[f2][i2]]

            if not next_target:   # 모두 엣지가 맞아서 다음 타겟이 없으면 break
                break

           # print(f"\n🔄 Swap 전 버퍼: {current_colors}, 타겟: {target_colors}")
           # print(f"📍 타겟 위치: {f1}{i1}, {f2}{i2}")
            # swap: 버퍼 <-> 타겟

            self.edgeSequence.append((f1, i1, f2, i2))
            sides['D'][1], sides['F'][7], sides[f1][i1], sides[f2][i2] = \
                target_colors[0], target_colors[1], current_colors[0], current_colors[1]
          #  print(f"🎯 Swap 이후 버퍼 상태: {self.get_buffer_colors(sides)}")

            # 해결된 엣지를 확인
            if self.all_edges_solved(sides, corners):
                # print("✅ 모든 엣지 solve 완료", flush=True)
                break

     #   print("✅ M2 edgeSequence =", self.edgeSequence, flush=True)
        return sides


cubeEdges = Edge()
