import curses
from curses import *
import time, random, os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

os.system("mode con cols=93 lines=45")

infamilies1 = input('Please enter every character you would like in the gene pool.\n')
choice = input('would you like to seperate each family? y/n \n')
infamilies = "".join(set(infamilies1))
infamilies = infamilies.replace(" ", "")
stdscr = curses.initscr()

curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.mousemask(1)

curs_set(0)
stdscr.clear()

rows, cols = stdscr.getmaxyx()

stdscr.nodelay(1)

sy,sx = stdscr.getmaxyx()

print(sy,sx)

families = []

for i in range(len(infamilies)):
    families.append(infamilies[i])

begin_x = 0
begin_y = 0
height = len(families) + 4
width = sx

infoscreen = curses.newwin(height,width,begin_y,begin_x)

infoscreen.border()

begin_x = 0
begin_y = len(families) + 4
height = sy - (len(families) + 4)
width = sx

cellscr = curses.newwin(height, width, begin_y, begin_x)

cellscr.border()

seperation = ([sx // (len(families)+1) + (1 if x < sx % len(families) else 0)  for x in range (len(families))])

if choice.lower().strip() == 'y':
    for i in range(len(families)):
        for x in range((seperation[i]*(i+1))-10,(seperation[i]*(i+1))):
            for y in range((((sy+len(families))//2)-5),((sy//2)+5)):
                chance = random.randint(0, 10)
                if chance >= 5:
                    cellscr.addstr(y, x, families[i])
                else:
                    pass

else:
    for x in range((sx//2)-5, (sx//2)+5):
        for y in range((((sy+len(families))//2)-5),((sy//2)+5)):
            chance = random.randint(0, 10)
            if chance >= 5:
                cellscr.addstr(y, x, random.choice(families))
            else:
                pass
stdscr.refresh()

"""
stdscr.addstr(5, 15, '0')
stdscr.addstr(6, 15, '0')
stdscr.addstr(4, 15, '0')
stdscr.addstr(4, 16, '0')
stdscr.addstr(5, 14, '0')
stdscr.refresh()
"""
  
#(70, 190) - bottom right corner
def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num



generation = 0
Gen = [0]

familydict = {}

percentdict = {}

axisdict = {}

for i in range(len(families)):
    axisdict["{0}axis".format(families[i])] = [0]

while stdscr.getch() != ord('q'):
    sy,sx = cellscr.getmaxyx()
    cellscr.border()
    infoscreen.border()
    for i in range(len(families)):
        familydict["{0}".format(families[i])] = 0
    deathrate = 0
    total = 1
    for x in range(2, (sx-1)):
        for y in range(1, (sy-1)):
            current_character = chr(cellscr.inch(y, x))
            
            neighbors = 0
            surrounding = []
            
            above = chr(cellscr.inch(y + 1, x))
            if above in families:
                neighbors = neighbors + 1
                surrounding.append(above)
                for i in range(len(families)):
                    if above == families[i]:
                        familydict["{0}".format(families[i])] += 1

            below = chr(cellscr.inch(y - 1, x))
            if below in families:
                neighbors = neighbors + 1
                surrounding.append(below)
                for i in range(len(families)):
                    if below == families[i]:
                        familydict["{0}".format(families[i])] += 1

            left = chr(cellscr.inch(y, x - 1))
            if left in families:
                neighbors = neighbors + 1
                surrounding.append(left)
                for i in range(len(families)):
                    if left == families[i]:
                        familydict["{0}".format(families[i])] += 1

            right = chr(cellscr.inch(y, x + 1))
            if right in families:
                neighbors = neighbors + 1
                surrounding.append(right)
                for i in range(len(families)):
                    if right == families[i]:
                        familydict["{0}".format(families[i])] += 1

            #newstart

            topright = chr(cellscr.inch(y+1, x+1))
            if topright in families:
                neighbors = neighbors + 1
                surrounding.append(topright)
                for i in range(len(families)):
                    if topright == families[i]:
                        familydict["{0}".format(families[i])] += 1

            bottomright = chr(cellscr.inch(y-1, x+1))
            if bottomright in families:
                neighbors = neighbors + 1
                surrounding.append(bottomright)
                for i in range(len(families)):
                    if bottomright == families[i]:
                        familydict["{0}".format(families[i])] += 1

            topleft = chr(cellscr.inch(y+1, x-1))
            if topleft in families:
                neighbors = neighbors + 1
                surrounding.append(topleft)
                for i in range(len(families)):
                    if topleft == families[i]:
                        familydict["{0}".format(families[i])] += 1

            bottomleft = chr(cellscr.inch(y-1, x-1))
            if bottomleft in families:
                neighbors = neighbors + 1
                surrounding.append(bottomleft)
                for i in range(len(families)):
                    if bottomleft == families[i]:
                        familydict["{0}".format(families[i])] += 1
            
            if current_character in families:
                for i in range(len(families)):
                    if current_character == families[i]:
                        familydict["{0}".format(families[i])] += 1
                if neighbors < 2:
                    cellscr.addstr(y, x, ' ')
                    deathrate = deathrate + 1
                elif neighbors > 3:
                    cellscr.addstr(y, x, ' ')
                    deathrate = deathrate + 1
            
            elif current_character == ' ':
                if neighbors == 3:
                    cellscr.addstr(y, x, most_frequent(surrounding))
                    current_char = cellscr.inch(y, x)
                    for i in range(len(families)):
                        if current_char == families[i]:
                            familydict["{0}".format(families[i])] += 1
    #add_random()

    generation = generation + 1
    if generation%50 == 0:
        Gen.append(generation)
        for i in range(len(families)):
            axisdict["{0}axis".format(families[i])].append(familydict["{0}".format(families[i])])
    
    infoscreen.addstr(1, 1, ('Generation: ' + str(generation) + '     '))
    infoscreen.addstr(2, 1, ('Deathrate: ' + str(deathrate) + '     '))

    for i in range(len(families)):
        total += familydict["{0}".format(families[i])]
    for i in range(len(families)):
        percentdict["{0}_percent".format(i)] = (round((familydict["{0}".format(families[i])] / total)*100, 2))
        infoscreen.addstr(i + 3, 1, families[i] + ': ' + str(percentdict["{0}_percent".format(i)]) + '%   ')
        
    
    stdscr.refresh()
    cellscr.refresh()
    infoscreen.refresh()
    #time.sleep(0.1)

for i in range(len(families)):
    plt.plot(Gen, axisdict["{0}axis".format(families[i])], label = families[i])
plt.legend()
plt.xlabel('Generation')
plt.ylabel('Population')
plt.show()


curses.nocbreak()
stdscr.keypad(False)
curses.echo()

curses.endwin()

print("Generations passed: " + str(generation))






