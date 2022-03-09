import curses
import os
import random
from curses import *
import numpy
import matplotlib.pyplot as plt

# Resize the Windows console #
os.system("mode con cols=93 lines=45")

# User  input at startup #
infamilies1 = input('Please enter every character you would like in the gene pool.\n')  # Good chars for families: █ ░
choice = input('would you like to separate each family? y/n \n')
infamilies = "".join(set(infamilies1))
infamilies = infamilies.replace(" ", "")

# Creates the base Curses window and assign its attributes #
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curs_set(0)
stdscr.clear()
rows, cols = stdscr.getmaxyx()
stdscr.nodelay(True)
sy, sx = stdscr.getmaxyx()

# Creates the families list which stores every gene in the pool #
families = []

for i in range(len(infamilies)):
    families.append(infamilies[i])

# Creates the infoscreen and cell screen windows #
begin_x = 0
begin_y = 0
height = len(families) + 4
width = sx
infoscreen = curses.newwin(height, width, begin_y, begin_x)
infoscreen.border()

begin_x = 0
begin_y = len(families) + 4
height = sy - (len(families) + 4)
width = sx
cellscr = curses.newwin(height, width, begin_y, begin_x)
cellscr.border()

# This equation is necessary to evenly distribute cells across the screen,
# if the user decides to split each family.
separation = ([sx // (len(families) + 1) + (1 if x < sx % len(families) else 0) for x in range(len(families))])

# Distributes cells based on user input.
if choice.lower().strip() == 'y':
    for i in range(len(families)):
        for x in range((separation[i] * (i + 1)) - 10, (separation[i] * (i + 1))):
            for y in range((((sy + len(families)) // 2) - 5), ((sy // 2) + 5)):
                chance = random.randint(0, 10)
                if chance >= 5:
                    cellscr.addstr(y, x, families[i])
                else:
                    pass

else:
    for x in range((sx // 2) - 5, (sx // 2) + 5):
        for y in range((((sy + len(families)) // 2) - 5), ((sy // 2) + 5)):
            chance = random.randint(0, 10)
            if chance >= 5:
                cellscr.addstr(y, x, random.choice(families))
            else:
                pass

stdscr.refresh()


# Function used to determine the most frequent item in a list, necessary
# for new cells being created to know which family it belongs to.
def most_frequent(clist):
    counter = 0
    num = clist[0]

    for k in clist:
        curr_frequency = clist.count(k)
        if curr_frequency > counter:
            counter = curr_frequency
            num = k

    return num


# Function used to check the eight tiles in each cell's neighborhood.
def check(yc, x):
    global neighbors
    direction = chr(cellscr.inch(yc, x))
    if direction in families:
        neighbors = neighbors + 1
        surrounding.append(direction)
        for p in range(len(families)):
            if direction == families[p]:
                familydict["{}".format(families[p])] += 1


# Variables and lists needed to create the graph at the end of the program.
generation = 0
Gen = [0]
familydict = {}
percentdict = {}
axisdict = {}

for i in range(len(families)):
    axisdict["{0}axis".format(families[i])] = [0]

# This loop contains the main cellular automata section of the code, and
# quits when the user presses the 'q' key.
while stdscr.getch() != ord('q'):
    sy, sx = cellscr.getmaxyx()
    cellscr.border()
    infoscreen.border()
    for i in range(len(families)):  # assigns each family a value of 0 at the end of a generation
        familydict["{0}".format(families[i])] = 0
    deathrate = 0
    total = 1
    for x in range(2, (sx - 2)):  # iterates over the maximum x,y
        for y in range(2, (sy - 2)):  # values minus four for each axis.
            current_character = chr(cellscr.inch(y, x))
            neighbors = 0
            surrounding = []
            check(y - 1, x)  # above
            check(y + 1, x)  # below
            check(y, x - 1)  # left
            check(y, x + 1)  # right
            check(y - 1, x + 1)  # top right
            check(y + 1, x + 1)  # bottom right
            check(y - 1, x - 1)  # top left
            check(y + 1, x - 1)  # bottom left
            if current_character in families:  # If the cell at the current coordinate is alive:
                for i in range(len(families)):
                    if current_character == families[i]:
                        familydict["{0}".format(families[i])] += 1  # Assign that family's dict value +1
                if neighbors < 2:
                    cellscr.addstr(y, x, ' ')  # The cell dies :(
                    deathrate = deathrate + 1
                if neighbors > 3:
                    cellscr.addstr(y, x, ' ')  # RIP
                    deathrate = deathrate + 1
            elif current_character == ' ':  # If the current cell is dead:
                if neighbors == 3:  # AND it has three neighbors:
                    cellscr.addstr(y, x, most_frequent(surrounding))  # IT'S ALIVE!
                    current_char = cellscr.inch(y, x)
                    for i in range(len(families)):
                        if current_char == families[i]:
                            familydict["{0}".format(families[i])] += 1  # Add new cell to family's dict
    generation = generation + 1
    if generation % 50 == 0:  # Adds all information to the graph if current generation is a multiple of 50
        Gen.append(generation)
        for i in range(len(families)):
            axisdict["{0}axis".format(families[i])].append(familydict["{0}".format(families[i])])
    infoscreen.addstr(1, 1, ("Generation: %s     " % generation))  # 'Generation: #' text
    infoscreen.addstr(2, 1, ('Death rate: %s     ' % deathrate))  # 'Death rate: #' text
    for i in range(len(families)):
        total += familydict["{0}".format(families[i])]  # Total is population of all families added together
    for i in range(len(families)):
        # Calculates every family's percentage of domination of the board
        percentdict["{0}_percent".format(i)] = (round((familydict["{0}".format(families[i])] / total) * 100, 2))
        # Adds percentage value behind family's character
        infoscreen.addstr(i + 3, 1, '{}: {}%     '.format(families[i], percentdict["{0}_percent".format(i)]))
    # Refresh all screens and windows
    stdscr.refresh()
    cellscr.refresh()
    infoscreen.refresh()
# Finish creating and show the graph and program termination
for i in range(len(families)):
    plt.plot(Gen, axisdict["{0}axis".format(families[i])], label=families[i])
plt.legend()
plt.xlabel('Generation')
plt.ylabel('Population')
plt.show()
# Terminate the program
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
# Once the program has ended, and we're back at the console, display
# how many generations passed during runtime.
print("Generations passed: %s" % generation)
