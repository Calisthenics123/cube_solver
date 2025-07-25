# RubiksBlindfolded/utils/color_to_face_mapper.py

def map_colors_to_faces(sides, color_map):
    """
    Convert a cube's color-based representation to face-based (U, D, F, B, L, R)

    Args:
        sides (dict): Dictionary with color stickers (e.g., 'W', 'G', etc.)
        color_map (dict): {'W': 'U', 'Y': 'D', 'G': 'F', 'B': 'B', 'O': 'L', 'R': 'R'}

    Returns:
        dict: Converted dictionary with face letters instead of color codes
    """
    face_sides = {}
    for face, stickers in sides.items():
        converted = []
        for color in stickers:
            if color not in color_map:
                raise ValueError(f"❗변환할 수 없는 색상: '{color}'가 color_map에 없습니다.")
            converted.append(color_map[color])
        face_sides[face] = converted
    return face_sides
