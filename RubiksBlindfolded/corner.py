class Corner:

    def getCornerSequence(self):
        return self.cornerSequence

    def __init__(self):
        self.cornerSequence = []
        self.target_order = [                                                           # ('U', 0, 'B', 2, 'L', 0), ('L', 0, 'U', 0, 'B', 2), ('B', 2, 'L', 0, 'U', 0),  제거
            ('U', 2, 'R', 2, 'B', 0), ('U', 8, 'F', 2, 'R', 0), ('U', 6, 'L', 2, 'F', 0),
            ('L', 2, 'F', 0, 'U', 6), ('L', 8, 'D', 0, 'F', 6), ('L', 6, 'B', 8, 'D', 6),
            ('F', 0, 'U', 6, 'L', 2), ('F', 2, 'R', 0, 'U', 8), ('F', 8, 'D', 2, 'R', 6), ('F', 6, 'L', 8, 'D', 0, ),
            ('R', 0, 'U', 8, 'F', 2), ('R', 2, 'B', 0, 'U', 2), ('R', 8, 'D', 8, 'B', 6), ('R', 6, 'F', 8, 'D', 2, ),
            ('B', 0, 'U', 2, 'R', 2), ('B', 8, 'D', 6, 'L', 6), ('B', 6, 'R', 8, 'D', 8),
            ('D', 0, 'F', 6, 'L', 8), ('D', 2, 'R', 6, 'F', 8), ('D', 8, 'B', 6, 'R', 8), ('D', 6, 'L', 6, 'B', 8)
        ]

        self.skip_once = True              # 처음엔 한 바퀴 건너뛰기
        self.last_buffer_color = None    # 이전 버퍼 색상 기억

    def get_buffer_colors(self, sides):
        return [sides['L'][0], sides['U'][0], sides['B'][2]]

    def get_center_color(self, sides, face):
        return sides[face][4]

    def is_corner_solved(self, sides, f1, i1, f2, i2, f3, i3):                     # 코너가 이미 맞았는지 체크 (양쪽 색상 비교)
        c1 = sides[f1][i1]        # ㄱㄴㄷ 색상 White, orange 등...
        c2 = sides[f2][i2]
        c3 = sides[f3][i3]
        expected1_color = self.get_center_color(sides, f1)  
        expected2_color = self.get_center_color(sides, f2)
        expected3_color = self.get_center_color(sides, f3)

        if c1 == expected1_color and sorted([c2, c3]) == sorted([expected2_color, expected3_color]):
            print(f"✅ 이미 맞은 코너: {f1}{i1}, {f2}{i2}, {f3}{i3}")
            print(f"      ✅ 갖고있는색상 {c1}, {c2}, {c3}")
            print(f"      ✅ 중심:  {[expected1_color, expected2_color, expected3_color]}")
            return True
        else:
            print(f"❌ 불일치 코너: {f1}{i1}, {f2}{i2}, {f3}{i3}")
            print(f"    ▶ 색상: {[c1, c2, c3]}")
            print(f"    ▶ 중심: {[expected1_color, expected2_color, expected3_color]}")
            return False


    def find_piece(self, current_colors, sides):          # 색상에 맞는 코너를 찾아서 반환 (이미 맞은 엣지는 제외), 이건 이미 버퍼가 다 맞았을때 기준
        for f1, i1, f2, i2, f3, i3 in self.target_order:       # ㄱ,ㄴ,ㄷ 순서대로 (f1i1..)에 불러넣기
            if self.is_corner_solved(sides, f1, i1, f2, i2, f3, i3):              #  ㄱ,ㄴ,ㄷ들이 가운데 색상과 일치하는가?
                continue                                                              # 이미 맞은 코너는 건너뛰기

            t1, t2, t3 = current_colors                           # current_color=self.get_buffer_colors(sides) 버퍼에 있는 색상들+
            expected1_color = self.get_center_color(sides, f1)  
            expected2_color = self.get_center_color(sides, f2)
            expected3_color = self.get_center_color(sides, f3)

            print(f"🧩 중앙의 색깔은 {expected1_color}, {expected2_color}, {expected3_color} // 현재버퍼의 색상 {t1}, {t2}, {t3}")   

            if sorted([t1, t2, t3]) == sorted(["y", "b", "r"]):       # 버퍼에 이미 올바른 버퍼가 있을 경우
                print("💡 버퍼가 UBL입니다.")
                for tf1, ti1, tf2, ti2, tf3, ti3 in self.target_order:

                    if self.is_corner_solved(sides, tf1, ti1, tf2, ti2, tf3, ti3):
                        print("이미 풀린 코너가 있어여")
                        continue

                    if sorted([(tf1, ti1), (tf2, ti2), (tf3, ti3)]) == sorted([('U', 0), ('L', 0), ('B', 2)]):
                        print("⏭️ 버퍼 위치는 건너뜀")
                        continue

                    tc1, tc2 = sides[tf1][ti1], sides[tf2][ti2]    # ㄱ,ㄴ,ㄷ 중에서 차례로 임의의 것을 불러옴
                    tc3 = sides[tf3][ti3]
                    expected1 = self.get_center_color(sides, tf1)
                    expected2 = self.get_center_color(sides, tf2)
                    expected3 = self.get_center_color(sides, tf3)
                    print(f"🔍 검사 중 엣지: {tf1}{ti1},{tf2}{ti2},{tf3}{ti3} / 색상: {tc1}, {tc2}, {tc3} / 중심: {expected1}, {expected2}, {expected3}")

                    return tf1, ti1, tf2, ti2, tf3, ti3
 
            if t1 == expected1_color and sorted([t2, t3]) == sorted([expected2_color, expected3_color]):   # 원래에 있어야하는 색상과 같을때
                print(f"출력하려는 색상: {f1}{i1}, {f2}{i2}, {f3}{i3}")
                return f1, i1, f2, i2, f3, i3                                                       # ㄱ,ㄴ,ㄷ 들이 버퍼의 색상과 동일하면 값을 돌려준다.
        return None




    def all_corners_solved(self, sides):
        for f1, i1, f2, i2, f3, i3 in self.target_order:
            if not self.is_corner_solved(sides, f1, i1, f2, i2, f3, i3):
                colors = [sides[f1][i1], sides[f2][i2], sides[f3][i3]]
                centers = [self.get_center_color(sides, f1),
                                self.get_center_color(sides, f2),
                                self.get_center_color(sides, f3)]
                print(f"🚨 [불일치] 코너 위치: {f1}{i1}, {f2}{i2}, {f3}{i3} / 색상: {colors} / 중심색: {centers}")
                return False
        return True


    def solveCorner(self, sides, corner):                 # 메인 함수
        visited = set()
        loop_count = 0
        loop_limit = 20                                        # 최대 반복 횟수

        while loop_count < loop_limit:                    # 20번 동안 아래의 상황을 반복한다.
            loop_count += 1

            current_colors = self.get_buffer_colors(sides)            # 불러지는 값은 버퍼색상
            next_target = self.find_piece(current_colors, sides)


            

            if not next_target:
                continue

            f1, i1, f2, i2, f3, i3 = next_target
            target_colors = [sides[f1][i1], sides[f2][i2], sides[f3][i3]]


            if not next_target:   # 모두 코너가 맞아서 다음 타겟이 없으면 break
                break

            f1, i1, f2, i2, f3, i3 = next_target
            target_colors = [sides[f1][i1], sides[f2][i2], sides[f3][i3]]

            print(f"\n🔄 Swap 전 버퍼: {current_colors}, 타겟: {target_colors}")
            print(f"📍 타겟 위치: {f1}{i1}, {f2}{i2}, {f3}{i3}")

            # swap: 버퍼 <-> 타겟
            self.cornerSequence.append((f1, i1, f2, i2, f3, i3))


            sides['L'][0], sides['U'][0], sides['B'][2], sides[f1][i1], sides[f2][i2], sides[f3][i3] = \
                target_colors[0], target_colors[1], target_colors[2], current_colors[0], current_colors[1], current_colors[2]

            if self.all_corners_solved(sides):
                print("✅ 모든 코너 solve 완료", flush=True)
                break

        print("🧠 OP cornerSequence =", self.cornerSequence, flush=True)
        return sides


# ✅ 꼭 있어야 하는 부분
cubeCorners = Corner()