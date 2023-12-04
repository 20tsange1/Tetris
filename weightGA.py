import visualpygame
import random
import player

# https://www.youtube.com/watch?v=4XZoVQOt-0I&ab_channel=TopShelfTechnology

def fitness(bumpiness, wells, holes, complete, past, aggregate, smoothness):

    score = []

    player.weightBumpiness = bumpiness
    player.weightWells = wells
    player.weightHoles = holes
    player.weightComplete = complete
    player.weightHeightPast = past
    player.weightHeightAggregate = aggregate    
    player.weightSmoothness = smoothness

    for i in range(5):
        visualpygame.random.seed()
        visualpygame.seed = visualpygame.random.randint(0,1000)
        score.append(visualpygame.run())

    f = open("weightings.txt", "a")
    f.write("[" + str(bumpiness) + "," + str(wells) + "," + str(holes) + "," + str(complete) + "," + str(past) + "," + str(aggregate) + "," + str(smoothness) + "]" + "\n" + str(score) + "\n------\n")
    f.close()

    return score[2]

# Fitness is your score
solutions = [
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4],
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4],
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4],
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4],
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4],
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4],
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4],
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4],
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4],
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4],
    [-10.3, 0.403, -7, 1, -21, -2.76, -252.4]
]

for x in range(10-len(solutions)):
    solutions.append((-random.uniform(0.1,0.3),random.uniform(0,0.2),-random.randint(3,10),1,-random.uniform(0.2,0.8),-random.uniform(0.5,1.5),-random.uniform(0,10)))
print()

for i in range(10000):
    rankedsolutions = []
    for s in solutions:
        rankedsolutions.append( (fitness(s[0],s[1],s[2],s[3],s[4],s[5],s[6]),s) )
    rankedsolutions.sort()
    rankedsolutions.reverse()
    print("Gen", str(i), "best solutions")
    print(rankedsolutions[0])
    bestsolutions = rankedsolutions[:8]

    elements = []
    for s in bestsolutions:
        elements.append(s[1][0])
        elements.append(s[1][1])
        elements.append(s[1][2])
        elements.append(s[1][3])
        elements.append(s[1][4])
        elements.append(s[1][5])
        elements.append(s[1][6])
    
    newGen = []
    for _ in range(32):
        e1 = random.choice(elements) * random.uniform(0.99,1.01)
        e2 = random.choice(elements) * random.uniform(0.99,1.01)
        e3 = random.choice(elements) * random.uniform(0.99,1.01)
        e4 = random.choice(elements) * random.uniform(0.99,1.01)
        e5 = random.choice(elements) * random.uniform(0.99,1.01)
        e6 = random.choice(elements) * random.uniform(0.99,1.01)
        e7 = random.choice(elements) * random.uniform(0.99,1.01)
        
        newGen.append((e1,e2,e3,e4,e5,e6,e7))

    rankedsolutions = newGen
