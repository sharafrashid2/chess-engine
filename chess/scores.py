from copy import deepcopy

"""
In this file, all the scores for pieces at each position of the board are stored.
"""

def reverse_array(array):
    result = deepcopy(array)
    result.reverse()
    return result

white_pawn_scores = [
                    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                    [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
                    [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
                    [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
                    [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
                    [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
                    [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
                    [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
                ]

black_pawn_scores = reverse_array(white_pawn_scores)

knight_scores = [
                    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                    [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
                    [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
                    [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
                    [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
                    [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
                    [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
                    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
                ]

white_bishop_scores =   [
                            [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                            [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                            [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
                            [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
                            [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
                            [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
                            [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
                            [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
                        ]

black_bishop_scores = reverse_array(white_bishop_scores)

white_rook_scores = [
                        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                        [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
                        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
                        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
                        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
                        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
                        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
                        [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
                    ]

black_rook_scores = reverse_array(white_rook_scores)

queen_scores =  [
                    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
                    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
                ]

white_king_scores = [
                        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                        [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                        [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                        [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
                        [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
                    ]

black_king_scores = reverse_array(white_king_scores)