from board import Direction, Rotation, Action
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError


from board import Direction, Rotation, Action
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError

class HumanPlayV1(Player):

    def __init__(self, seed=None):
        self.random = Random(seed)

    weights = [-10.3, 0.402, -7, 1, -20.94, -2.760, -292.4]

    weightBumpiness = weights[0]
    weightWells = weights[1]
    weightHoles = weights[2]
    weightComplete = weights[3]
    weightHeightPast = weights[4]
    weightHeightAggregate = weights[5]
    weightSmoothness = weights[6]

    def block_type(self, colour):

        type = ""

        if colour == "cyan":
            type = "I"

        elif colour == "blue":
            type = "J"

        elif colour == "orange":
            type = "L"

        elif colour == "yellow":
            type = "O"
    
        elif colour == "green":
            type = "S"
        
        elif colour == "magenta":
            type = "T"
        
        elif colour == "red":
            type = "Z"

        return type
    
    def rotationCalc(self, type):

        rotations = 0

        if type == "I":
            rotations = 1

        elif type == "J":
            rotations = 3

        elif type == "L":
            rotations = 3

        elif type == "O":
            rotations = 0
    
        elif type == "S":
            rotations = 1
        
        elif type == "T":
            rotations = 3
        
        elif type == "Z":
            rotations = 1



        return rotations

    def num_possible_left(self, type, direction):

        num = 0

        if direction == 0:
            if type == "I" or "J" or "L" or "O" or "T":
                num = 5
            elif type == "Z" or "S":
                num = 4
        
        if direction == 1:
            if type == "J" or "Z" or "S":
                num = 5
            elif type == "L" or "I" or "J":
                num = 4
            
        if direction == 2:
            if type == "J":
                num = 6
            elif type == "L" or "T":
                num = 4
            

        if direction == 3:
            #turn clockwise
            if type == "L":
                num = 4

            if type == "J" or "T":
                num = 5

        return num

    def num_possible_right(self, type, direction):

        num = 0

        if direction == 0:
            if type == "I":
                num = 4
            elif type == "L" or "J" or "Z" or "S" or "T":
                num = 3
            # I 4 L 3 T 3 Z 3 J 3 O 3
            
        
        if direction == 1:
            if type == "T":
                num = 4
            elif type == "I" or "J":
                num = 2
            elif type == "L" or "S" or "Z":
                num = 3

            # I 2 L 3 T 4 Z 3 S 3 J 2
            
            
        if direction == 2:
            if type == "L":
                num = 4
            if type == "T":
                num = 3
            if type == "J":
                num = 2
            # L 4 T 3 J 2

        if direction == 3:
            #turn clockwise

            if type == "L" or "T":
                num = 3
            if type == "J":
                num = 2
            # L 3 T 3 J 2

        return num

    def calculate_blocks(self, board):
        blocks = 0
        for x in range(10):
            for y in range(24):
                if (x,y) in board.cells:
                    blocks += 1
        return blocks

    def calculate_bumpiness(self, board, x):
        if x < 9:
            return abs(self.calculate_height(board, x) - self.calculate_height(board, x + 1)) * abs(self.calculate_height(board, x) - self.calculate_height(board, x + 1))
        return 0

    def calculate_holes(self, board, x, y):
        if y < 23:
            if 0 < x < 9:
                if ((x, y) not in board) and (((x, y + 1) in board) and ((x, y - 1) in board) and ((x-1, y) in board) and ((x+1, y) in board)):
                    return True
            elif x == 9:
                if ((x, y) not in board) and (((x, y + 1) in board) and (((x, y - 1) in board) and ((x-1, y) in board))):
                    return True
            elif x == 0:
                if ((x, y) not in board) and (((x, y + 1) in board) and (((x, y - 1) in board) and ((x+1, y) in board))):
                    return True
        elif y == 23:
            if 0 < x < 9:
                if ((x, y) not in board) and (((x, y - 1) in board) and ((x-1, y) in board) and ((x+1, y) in board)):
                    return True
            elif x == 9:
                if ((x, y) not in board) and (((x, y - 1) in board) and ((x-1, y) in board)):
                    return True
            elif x == 0:
                if ((x, y) not in board) and (((x, y - 1) in board) and ((x+1, y) in board)):
                    return True
        return False
    
    def calculate_wells(self, board, x):
        wellScore = 0
        c = 1
        
        for y in range(24):    
            if ((x,y) in board) or y == 23:
                if 0 < x < 9:
                    while (((x,y-c) not in board) and ((x+1, y-c) in board) and ((x-1, y-c) in board)):
                        if c <= 4:
                            if c <= 2:
                                wellScore += c * c * c
                        else:
                            wellScore -= c
                        c += 1
                    return wellScore
                elif x == 0:
                    while (((x,y-c) not in board) and ((x+1, y-c) in board)):
                        if c <= 4:
                            wellScore += c * c * c * c
                        else:
                            wellScore -= c
                        c += 1
                    return wellScore
                elif x == 9:
                    while (((x,y-c) not in board) and ((x+1, y-c) in board)):
                        if c <= 4:
                            wellScore += c * c * c * c
                        else:
                            wellScore -= c
                        c += 1
                    return wellScore
        return wellScore

    def calculate_height(self, board, x):
        for y in range(24):
            if (x,y) in board:
                return (23-y)
        return 0

    def calculate_column_height(self, board, x):
        score = 0
        height = self.calculate_height(board, x)
        if height > 12:
            score += ((height-12) * (height-12))
        return score
            
    def calculate_complete_under12(self, board, old_blocks):
        new_blocks = self.calculate_blocks(board)
        remain = old_blocks - new_blocks
        if remain == 6:
            return -150
        elif remain == 16:
            return -75
        elif remain == 26:
            return -25
        elif remain == 36:
            return 100
        else:
            return 0

    def calculate_complete_over12(self, board, old_blocks):
            new_blocks = self.calculate_blocks(board)
            remain = old_blocks - new_blocks
            if remain == 6:
                return -10
            elif remain == 16:
                return -10
            elif remain == 26:
                return -10
            elif remain == 36:
                return 100
            else:
                return 0

    def calculate_smoothness(self, board, x):
        smoothness = 0
        for y in range(24):
            if (x,y) in board.cells:
                for i in range(y, 24):
                    if (x,i) not in board.cells:
                        smoothness += 1
                break
        return smoothness
        
    def calculate_score(self, board, old_blocks, old_holes):
        holes = 0
        bumpiness = 0
        wells = 0
        height = 0
        aggregate_height = 0
        complete_lines = 0
        score = 0
        smoothness = 0

        for x in range(10):
            bumpiness += self.calculate_bumpiness(board, x)
            wells += self.calculate_wells(board, x)
            height += self.calculate_column_height(board, x)
            aggregate_height += self.calculate_height(board, x)
            smoothness += self.calculate_smoothness(board, x)
            for y in range(24):
                if self.calculate_holes(board, x,y) == True:
                    holes += 1

        # holes -= old_holes

        # if holes > 1:
        #     holes *= holes

        if (height * self.weightHeightPast) < -10:
            complete_lines = self.calculate_complete_over12(board, old_blocks)
        else:
            complete_lines = self.calculate_complete_under12(board, old_blocks)

        # print(bumpiness * self.weightBumpiness , wells * self.weightWells  , holes * self.weightHoles , complete_lines * self.weightComplete , height * self.weightHeightPast , aggregate_height * self.weightHeightAggregate , smoothness * self.weightSmoothness)

        score = bumpiness * self.weightBumpiness + wells * self.weightWells  + holes * self.weightHoles + complete_lines * self.weightComplete + height * self.weightHeightPast + aggregate_height * self.weightHeightAggregate + smoothness * self.weightSmoothness

        #holes height matter, bumpiness not as important medium, wells is positive, complete_lines positive

        return score

    def copy_board(self, board, rotations, direction, num_times):

        old_holes = 0

        old_blocks = self.calculate_blocks(board)

        for x in range(10):
            for y in range(24):
                if self.calculate_holes(board, x, y) == True:
                    old_holes += 1

        score = 0

        sandbox = board.clone()
        moves = []

        if old_holes > 4:
            if board.bombs_remaining > 0 :
                if sandbox.bomb() != True:
                    moves.append(Action.Bomb)

        if rotations == 3:
            if sandbox.rotate(Rotation.Clockwise) != True:
                moves.append(Rotation.Clockwise)
            else:
                return moves, score

        if rotations == 1:
            if sandbox.rotate(Rotation.Anticlockwise) != True:
                moves.append(Rotation.Anticlockwise)
            else:
                return moves, score

        if rotations == 2:
            if sandbox.rotate(Rotation.Anticlockwise) != True:
                moves.append(Rotation.Anticlockwise)
                if sandbox.rotate(Rotation.Anticlockwise) != True:
                    moves.append(Rotation.Anticlockwise)
                else:
                    return moves, score
            else:
                return moves, score

        for i in range(num_times):
            if direction == "L":
                if sandbox.move(Direction.Left) != True:
                    moves.append(Direction.Left)
                else:
                    return moves, score

            if direction == "R":
                if sandbox.move(Direction.Right) != True:
                    moves.append(Direction.Right)
                else:
                    return moves, score

        if sandbox.falling is not None:
            sandbox.move(Direction.Drop)
            moves.append(Direction.Drop)
        else:
            return score, moves
        
        score = self.calculate_score(sandbox, old_blocks, old_holes)
        
        return moves, score

    def copy_board_discard(self, board, rotations, direction, num_times):

        old_holes = 0

        old_blocks = self.calculate_blocks(board)

        for x in range(10):
            for y in range(24):
                if self.calculate_holes(board, x, y) == True:
                    old_holes += 1

        score = 0

        sandbox = board.clone()
        moves = []

        sandbox.discard()
        moves.append(Action.Discard)

        if rotations == 3:
            if sandbox.rotate(Rotation.Clockwise) != True:
                moves.append(Rotation.Clockwise)
            else:
                return moves, score

        if rotations == 1:
            if sandbox.rotate(Rotation.Anticlockwise) != True:
                moves.append(Rotation.Anticlockwise)
            else:
                return moves, score

        if rotations == 2:
            if sandbox.rotate(Rotation.Anticlockwise) != True:
                moves.append(Rotation.Anticlockwise)
                if sandbox.rotate(Rotation.Anticlockwise) != True:
                    moves.append(Rotation.Anticlockwise)
                else:
                    return moves, score
            else:
                return moves, score

        for i in range(num_times):
            if direction == "L":
                if sandbox.move(Direction.Left) != True:
                    moves.append(Direction.Left)
                else:
                    return moves, score

            if direction == "R":
                if sandbox.move(Direction.Right) != True:
                    moves.append(Direction.Right)
                else:
                    return moves, score

        if sandbox.falling is not None:
            sandbox.move(Direction.Drop)
            moves.append(Direction.Drop)
        else:
            return score, moves
        
        score = self.calculate_score(sandbox, old_blocks, old_holes)
        
        return moves, score

    def brute_force(self, board):
        type = self.block_type(board.falling.color)
        rotation = self.rotationCalc(type)

        tempmoves = []
        finalmoves =[]

        tempscore = 0
        highscore = -100000

        for i in range(rotation + 1):
            for j in range(self.num_possible_left(type, i) + 1):
                tempmoves, tempscore = self.copy_board(board, i, "L", j)
                if tempscore > highscore and tempscore != 0:
                    highscore = tempscore
                    finalmoves = tempmoves

        for i in range(rotation + 1):
            for j in range(self.num_possible_right(type, i) + 1):
                tempmoves, tempscore = self.copy_board(board, i, "R", j)
                if tempscore > highscore and tempscore != 0:
                    highscore = tempscore
                    finalmoves = tempmoves

        type = self.block_type(board.next.color)
        rotation = self.rotationCalc(type)

        for i in range(rotation + 1):
            for j in range(self.num_possible_left(type, i) + 1):
                tempmoves, tempscore = self.copy_board_discard(board, i, "L", j)
                if tempscore > highscore + 270 and tempscore != 0:
                    highscore = tempscore
                    finalmoves = tempmoves

        for i in range(rotation + 1):
            for j in range(self.num_possible_right(type, i) + 1):
                tempmoves, tempscore = self.copy_board_discard(board, i, "R", j)
                if tempscore > highscore + 270 and tempscore != 0:
                    highscore = tempscore
                    finalmoves = tempmoves

        return finalmoves

    def choose_action(self, board):
        

        choice_moves = []
        choice_moves = self.brute_force(board)
        
        return choice_moves


class HumanPlayV2(Player):

    def __init__(self, seed=None):
        self.random = Random(seed)

    weights = [-8.5, 0.4, -350, 5, -200, -4.75, -1200]

    weightBumpiness = weights[0]
    weightWells = weights[1]
    weightHoles = weights[2]
    weightComplete = weights[3]
    weightHeightPast = weights[4]
    weightHeightAggregate = weights[5]
    weightSmoothness = weights[6]

    def block_type(self, colour):

        type = ""

        if colour == "cyan":
            type = "I"

        elif colour == "blue":
            type = "J"

        elif colour == "orange":
            type = "L"

        elif colour == "yellow":
            type = "O"
    
        elif colour == "green":
            type = "S"
        
        elif colour == "magenta":
            type = "T"
        
        elif colour == "red":
            type = "Z"

        return type
    
    def rotationCalc(self, type):

        rotations = 0

        if type == "I":
            rotations = 1

        elif type == "J":
            rotations = 3

        elif type == "L":
            rotations = 3

        elif type == "O":
            rotations = 0
    
        elif type == "S":
            rotations = 1
        
        elif type == "T":
            rotations = 3
        
        elif type == "Z":
            rotations = 1



        return rotations

    def num_possible_left(self, type, direction):

        num = 0

        if direction == 0:
            if type == "I" or "J" or "L" or "O" or "T":
                num = 5
            elif type == "Z" or "S":
                num = 4
        
        if direction == 1:
            if type == "J" or "Z" or "S":
                num = 5
            elif type == "L" or "I" or "J":
                num = 4
            
        if direction == 2:
            if type == "J":
                num = 6
            elif type == "L" or "T":
                num = 4
            

        if direction == 3:
            #turn clockwise
            if type == "L":
                num = 4

            if type == "J" or "T":
                num = 5

        return num

    def num_possible_right(self, type, direction):

        num = 0

        if direction == 0:
            if type == "I":
                num = 4
            elif type == "L" or "J" or "Z" or "S" or "T":
                num = 3
            # I 4 L 3 T 3 Z 3 J 3 O 3
            
        
        if direction == 1:
            if type == "T":
                num = 4
            elif type == "I" or "J":
                num = 2
            elif type == "L" or "S" or "Z":
                num = 3

            # I 2 L 3 T 4 Z 3 S 3 J 2
            
            
        if direction == 2:
            if type == "L":
                num = 4
            if type == "T":
                num = 3
            if type == "J":
                num = 2
            # L 4 T 3 J 2

        if direction == 3:
            #turn clockwise

            if type == "L" or "T":
                num = 3
            if type == "J":
                num = 2
            # L 3 T 3 J 2

        return num

    def calculate_blocks(self, board):
        blocks = 0
        for x in range(10):
            for y in range(24):
                if (x,y) in board.cells:
                    blocks += 1
        return blocks

    def calculate_bumpiness(self, board, x):
        if x < 8:
            return abs(self.calculate_height(board, x) - self.calculate_height(board, x + 1)) * abs(self.calculate_height(board, x) - self.calculate_height(board, x + 1))
        return 0

    def calculate_holes(self, board, x, y):
        if y < 23:
            if 0 < x < 9:
                if ((x, y) not in board) and (((x, y + 1) in board) and ((x, y - 1) in board) and ((x-1, y) in board) and ((x+1, y) in board)):
                    return True
            elif x == 9:
                if ((x, y) not in board) and (((x, y + 1) in board) and (((x, y - 1) in board) and ((x-1, y) in board))):
                    return True
            elif x == 0:
                if ((x, y) not in board) and (((x, y + 1) in board) and (((x, y - 1) in board) and ((x+1, y) in board))):
                    return True
        elif y == 23:
            if 0 < x < 9:
                if ((x, y) not in board) and (((x, y - 1) in board) and ((x-1, y) in board) and ((x+1, y) in board)):
                    return True
            elif x == 9:
                if ((x, y) not in board) and (((x, y - 1) in board) and ((x-1, y) in board)):
                    return True
            elif x == 0:
                if ((x, y) not in board) and (((x, y - 1) in board) and ((x+1, y) in board)):
                    return True
        return False
    
    def calculate_wells(self, board, x):
        wellScore = 0
        c = 1
        
        for y in range(24):    
            if ((x,y) in board) or y == 23:
                if 0 < x < 9:
                    while (((x,y-c) not in board) and ((x+1, y-c) in board) and ((x-1, y-c) in board)):
                        if c <= 4:
                            wellScore -= c * c * 100
                        else:
                            wellScore -= c * c * c * c * c * c
                        c += 1
                    return wellScore
                elif x == 0:
                    while (((x,y-c) not in board) and ((x+1, y-c) in board)):
                        if c <= 4:
                            wellScore -= c * c * 100
                        else:
                            wellScore -= c * c * c * c * c * c
                        c += 1
                    return wellScore
                elif x == 9:
                    while (((x,y-c) not in board) and ((x-1, y-c) in board)):
                        if c <= 4:
                            wellScore += c * c * c * c * 15
                        else:
                            wellScore -= c
                        c += 1
                    return wellScore
        return wellScore

    def calculate_height(self, board, x):
        for y in range(24):
            if (x,y) in board:
                return (23-y)
        return 0

    def calculate_column_height(self, board, x):
        score = 0
        height = self.calculate_height(board, x)
        if height > 12:
            score += ((height-12) * (height-12))
        return score
            
    def calculate_complete_under12(self, board, old_blocks):
        new_blocks = self.calculate_blocks(board)
        remain = old_blocks - new_blocks
        if remain == 6:
            return -300
        elif remain == 16:
            return -200
        elif remain == 26:
            return -100
        elif remain == 36:
            return 400
        else:
            return 0

    def calculate_complete_over12(self, board, old_blocks):
            new_blocks = self.calculate_blocks(board)
            remain = old_blocks - new_blocks
            if remain == 6:
                return 10
            elif remain == 16:
                return 20
            elif remain == 26:
                return 30
            elif remain == 36:
                return 50
            else:
                return 0

    def calculate_smoothness(self, board, x):
        smoothness = 0
        for y in range(24):
            if (x,y) in board.cells:
                for i in range(y, 24):
                    if (x,i) not in board.cells:
                        smoothness += 1
                break
        return smoothness
        
    def calculate_score(self, board, old_blocks, old_holes):
        holes = 0
        bumpiness = 0
        wells = 0
        height = 0
        aggregate_height = 0
        complete_lines = 0
        score = 0
        smoothness = 0

        for x in range(10):
            bumpiness += self.calculate_bumpiness(board, x)
            wells += self.calculate_wells(board, x)
            height += self.calculate_column_height(board, x)
            aggregate_height += self.calculate_height(board, x)
            smoothness += self.calculate_smoothness(board, x)
            for y in range(24):
                if self.calculate_holes(board, x,y) == True:
                    holes += 1

        holes -= old_holes

        if holes > 1:
            holes *= holes

        if (height * self.weightHeightPast) < -10:
            complete_lines = self.calculate_complete_over12(board, old_blocks)
        else:
            complete_lines = self.calculate_complete_under12(board, old_blocks)

        # print(bumpiness * self.weightBumpiness , wells * self.weightWells  , holes * self.weightHoles , complete_lines * self.weightComplete , height * self.weightHeightPast , aggregate_height * self.weightHeightAggregate , smoothness * self.weightSmoothness)

        score = bumpiness * self.weightBumpiness + wells * self.weightWells  + holes * self.weightHoles + complete_lines * self.weightComplete + height * self.weightHeightPast + aggregate_height * self.weightHeightAggregate + smoothness * self.weightSmoothness * 20

        #holes height matter, bumpiness not as important medium, wells is positive, complete_lines positive

        return score

    def copy_board(self, board, rotations, direction, num_times):

        old_holes = 0

        old_blocks = self.calculate_blocks(board)

        for x in range(10):
            for y in range(24):
                if self.calculate_holes(board, x, y) == True:
                    old_holes += 1

        score = 0

        sandbox = board.clone()

        moves = []
        
        if rotations == 3:
            if sandbox.falling:
                if sandbox.rotate(Rotation.Clockwise) != True and sandbox.falling is not None:
                    moves.append(Rotation.Clockwise)
                else:
                    return moves, score, sandbox

        if rotations == 1:
            if sandbox.falling:
                if sandbox.rotate(Rotation.Anticlockwise) != True and sandbox.falling is not None:
                    moves.append(Rotation.Anticlockwise)
                else:
                    return moves, score, sandbox

        if rotations == 2:
            if sandbox.falling:
                if sandbox.rotate(Rotation.Anticlockwise) != True and sandbox.falling is not None:
                    moves.append(Rotation.Anticlockwise)
                    if sandbox.rotate(Rotation.Anticlockwise) != True and sandbox.falling is not None:
                        moves.append(Rotation.Anticlockwise)
                    else:
                        return moves, score, sandbox
                else:
                    return moves, score, sandbox

        for i in range(num_times):
            if sandbox.falling:
                if direction == "L":
                    if sandbox.move(Direction.Left) != True and sandbox.falling is not None:
                        moves.append(Direction.Left)
                    else:
                        return moves, score, sandbox

                if direction == "R":
                    if sandbox.move(Direction.Right) != True and sandbox.falling is not None:
                        moves.append(Direction.Right)
                    else:
                        return moves, score, sandbox

        if sandbox.falling:
            if sandbox.falling is not None:
                sandbox.move(Direction.Drop)
                moves.append(Direction.Drop)
            else:
                return moves, score, sandbox
        
        score = self.calculate_score(sandbox, old_blocks, old_holes)
        
        return moves, score, sandbox


    def brute_force(self, board):
        typeblock = self.block_type(board.falling.color)
        rotation = self.rotationCalc(typeblock)

        all_scores = []

        tempmoves = []
        finalmoves =[]

        returnmoves = []

        best = -1

        tempscore = 0
        highscore = -100000

        if board.falling:
            for i in range(rotation + 1):
                for j in range(self.num_possible_left(typeblock, i) + 1):
                    tempmoves, tempscore, tempboard = self.copy_board(board, i, "L", j)
                    if tempscore != 0:
                        all_scores.append([tempscore, tempmoves, tempboard])
            for i in range(rotation + 1):
                for j in range(self.num_possible_right(typeblock, i) + 1):
                    tempmoves, tempscore, tempboard = self.copy_board(board, i, "R", j)
                    if tempscore != 0:
                        all_scores.append([tempscore, tempmoves, tempboard])

            tempholder = []

            if len(all_scores) > 0:
                flag = False
                while flag == False:
                    flag = True
                    for i in range(len(all_scores) - 1):
                        if all_scores[i][0] < all_scores[i+1][0]:
                            tempholder = all_scores[i+1]
                            all_scores[i+1] = all_scores[i]
                            all_scores[i] = tempholder
                            flag = False

            typeblock = self.block_type(board.next.color)
            rotation = self.rotationCalc(typeblock)

            if not board.falling.supported(board) and len(all_scores) > 0:
                for k in range(min(len(all_scores), 10)):
                    for i in range(rotation + 1):
                        for j in range(self.num_possible_left(typeblock, i) + 1):
                            tempmoves, tempscore, tempboard = self.copy_board(all_scores[k][2], i, "L", j)
                            if tempscore > highscore and tempscore != 0:
                                highscore = tempscore
                                best = k
                    
                    for i in range(rotation + 1):
                        for j in range(self.num_possible_right(typeblock, i) + 1):
                            tempmoves, tempscore, tempboard = self.copy_board(all_scores[k][2], i, "R", j)
                            if tempscore > highscore and tempscore != 0:
                                highscore = tempscore
                                best = k

                returnmoves = all_scores[best][1]

                if board.discards_remaining > 0:
                    if all_scores[best][0] < -5000:
                        returnmoves = [Action.Discard]

            else:
                return all_scores[0][1]
        else:
            return returnmoves

        return returnmoves

    def choose_action(self, board):
        
        choice_moves = []
        choice_moves = self.brute_force(board)
        
        return choice_moves
    
SelectedPlayer = HumanPlayV2
