import visualpygame
import player

for i in range(100):
    visualpygame.random.seed()
    visualpygame.seed = visualpygame.random.randint(0,100000)
    score = visualpygame.run()
    f = open("multiple.txt", "a")
    f.write("Seed: " + str(visualpygame.seed) + "\nScore: " + str(score) + "\n\n")
    f.close()

