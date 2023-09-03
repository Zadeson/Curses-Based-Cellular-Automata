import curses
import time
import os
import random
from curses import *
import matplotlib.pyplot as plt
import questionary
from collections import deque
from datetime import datetime
import textwrap


# Resize the Windows console #
os.system("mode con cols=200 lines=50")

# User input at startup #
families_prompt = questionary.text("Please enter every character you would like in the gene pool.").ask()
while len(families_prompt) == 1:
    print("! Please enter more than one character.")
    families_prompt = questionary.text("Please enter every character you would like in the gene pool.").ask()

# chars for families: █ ░
# choice = input('would you like to separate each family? y/n \n')
choice = questionary.select(
    "Would you like to separate each family?",
    choices=["yes", "no"],
).ask()

families_form = "".join(set(families_prompt))
families_form = families_form.replace(" ", "")

# Creates the base Curses window and assign its attributes #
stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curs_set(0)
stdscr.clear()
rows, cols = stdscr.getmaxyx()
stdscr.nodelay(True)
sy, sx = stdscr.getmaxyx()
curses.mousemask(1)


width = sx // 2
height = sy // 4
begin_y = (sy // 2) - height // 2
begin_x = (sx // 2) - width // 2

stdscr.clear()

# Creates the families list which stores every gene in the pool #
families = []

for i in range(len(families_form)):
    families.append(families_form[i])

# Creates the info screen and cell screen windows
begin_x = 0
begin_y = 0
height_info = len(families) + 6
width = (sx - 1)//2
info_screen = curses.newwin(height_info, width, begin_y, begin_x)
info_screen.border()

begin_x = 0
begin_y = len(families) + 6
height_cell = sy - (len(families) + 6)
cell_screen = curses.newwin(height_cell, width, begin_y, begin_x)
cell_screen.border()

# Create the new right screens (top and bottom)
begin_x_new = width
begin_y_new = 0
height_new_top = height_info  # height for the top screen
height_new_bottom = height_cell  # height for the bottom screen

new_bottom_right_width = int(0.6 * width)
# Calculate equal height for top and bottom right screens
equal_height = sy // 2

# Create the new right screens (top and bottom)
begin_x_new = width
begin_y_new = 0
height_new_top = equal_height  # height for the top screen
height_new_bottom = equal_height  # height for the bottom screen

new_bottom_right_width = int(0.6 * width)

top_right_screen = curses.newwin(height_new_top, new_bottom_right_width, begin_y_new, begin_x_new)
top_right_screen.border()

begin_y_new_bottom = height_new_top
bottom_right_screen = curses.newwin(height_new_bottom, new_bottom_right_width, begin_y_new_bottom, begin_x_new)
bottom_right_screen.border()
# This equation is necessary to evenly distribute cells across the screen,
# if the user decides to split each family.
separation = ([width // (len(families) + 1) + (1 if x < width % len(families) else 0) for x in range(len(families))])

# Distributes cells based on user input.
if choice.lower().strip() == 'yes':
    for i in range(len(families)):
        for x in range((separation[i] * (i + 1)) - 10, (separation[i] * (i + 1))):
            for y in range((((sy + len(families)) // 2) - 5), ((sy // 2) + 5)):
                chance = random.randint(0, 10)
                if chance >= 5:
                    cell_screen.addstr(y, x, families[i])
                else:
                    pass

else:
    for x in range((sx // 2) - 5, (sx // 2) + 5):
        for y in range((((sy + len(families)) // 2) - 5), ((sy // 2) + 5)):
            chance = random.randint(0, 10)
            if chance >= 5:
                cell_screen.addstr(y, x, random.choice(families))
            else:
                pass

stdscr.refresh()


# Function used to determine the most frequent item in a list, necessary
# for new cells being created to know which family it belongs to.
def most_frequent(c_list):
    counter = 0
    num = c_list[0]

    for k in c_list:
        curr_frequency = c_list.count(k)
        if curr_frequency > counter:
            counter = curr_frequency
            num = k

    return num

def safe_addstr(window, y, x, message):
    max_y, max_x = window.getmaxyx()
    lines = textwrap.wrap(message, width=max_x-2)  # -2 to account for borders
    lines_added = 0
    for i, line in enumerate(lines):
        if y + i < max_y - 1:  # -1 to account for the bottom border
            window.addstr(y + i, x, line)
            lines_added += 1  # Keep track of lines added
    return lines_added


# Function used to check the eight tiles in each cell's neighborhood.
def check(yc, x):
    global neighbors
    direction = chr(cell_screen.inch(yc, x))
    if direction in families:
        neighbors = neighbors + 1
        surrounding.append(direction)
        for p in range(len(families)):
            if direction == families[p]:
                family_dict["{}".format(families[p])] += 1


# Variables and lists needed to create the graph at the end of the program.
generation = 0
Gen = [0]
family_dict = {}
percentdict = {}
axis_dict = {}

for i in range(len(families)):
    axis_dict["{0}axis".format(families[i])] = [0]

paused = False
current_drawing_index = 0
special_char = '█'
erase_char = ' '
drawing_chars = families + [special_char, erase_char]
current_drawing_char = drawing_chars[current_drawing_index]
# This loop contains the main cellular automata section of the code, and
# quits when the user presses the 'q' key.

commentary_feed = deque(maxlen=10)  # deque to hold the last 10 commentary messages
domination_counter = {}  # Counter for each family's domination over 600 generations
boring_counter = 0  # Counter for boring events
extinct_families = set()  # Families that have gone extinct

def get_timestamped_message(message):
    current_time = datetime.now().strftime('%H:%M:%S')
    return f" <AI> [{current_time}] {message}"

extinction_risk_counter = {family: 0 for family in families}

endangered_flag = {family: False for family in families}

def announce_comeback(faction):
    global commentary_feed
    comeback_messages = [
        "The faction {faction} has risen from the ashes!",
        "{faction} is back in the game! They've turned the tide!",
        "Just when we thought they were down, {faction} bounces back!",
        "Against all odds, {faction} has rekindled their flame!",
        "{faction} defies extinction! The tables have turned!",
        "A phoenix rises! {faction} claws their way back from the brink!",
        "From zero to hero! {faction} has reclaimed their glory!",
        "Never count {faction} out! They're back and stronger than ever!",
        "Out of nowhere, {faction} surges back into contention!"
    ]
    comeback_paragraph = get_timestamped_message(random.choice(comeback_messages).format(faction=faction))

    # Add the comeback announcement to the feed.
    commentary_feed.append(comeback_paragraph)

def announce_extinction_risk(faction):
    global commentary_feed
    extinction_risk_phrases = [
        f"The faction {faction} is on the brink of extinction! A dire situation.",
        f"{faction} is teetering on the edge! Can they recover?",
        f"With numbers dwindling, {faction} faces impending doom!",
        f"{faction} is critically endangered! Time is running out."
    ]
    extinction_risk_paragraph = get_timestamped_message(random.choice(extinction_risk_phrases))

    # Add the extinction risk announcement to the feed.
    commentary_feed.append(extinction_risk_paragraph)

domination_counter = {family: 0 for family in families}

def announce_domination(faction):
    global commentary_feed
    domination_phrases = [
        f"The faction {faction} has been dominating for 1000 generations! A true powerhouse.",
        f"{faction} has maintained control for a millennium! A historic feat!",
        f"For 1000 generations, {faction} has reigned supreme!",
        f"In an unprecedented display, {faction} has dominated for 1000 cycles!"
    ]
    domination_paragraph = get_timestamped_message(random.choice(domination_phrases))

    # Add the domination announcement to the feed.
    commentary_feed.append(domination_paragraph)

def announce_spike():
    global commentary_feed
    spike_phrases = [
        "A sudden spike in mortality rates! The arena is a slaughterhouse!",
        "Death rates are through the roof! It's a massacre out there!",
        "The death toll skyrockets! A dark cloud looms over the arena.",
        "High casualties reported! It's a grim day for many factions."
    ]
    spike_paragraph = get_timestamped_message(random.choice(spike_phrases))

    # Add the spike announcement to the feed.
    commentary_feed.append(spike_paragraph)

def announce_drop():
    global commentary_feed
    drop_phrases = [
        "A surprising turn! Death rates plummet, offering a momentary respite.",
        "Fewer casualties this round! A glimmer of hope in a cruel world.",
        "The tide of death ebbs! Is this the calm before the storm?",
        "Death rates fall dramatically! A small victory in a larger war."
    ]
    drop_paragraph = get_timestamped_message(random.choice(drop_phrases))

    # Add the drop announcement to the feed.
    commentary_feed.append(drop_paragraph)

def announce_extinct(faction):
    global commentary_feed, leaderboard
    leaderboard[faction]["losses"] += 1
    extinction_phrases = [
        f"The faction {faction} has been wiped out! A dark day indeed.",
        f"{faction} is no more! Their legacy ends here.",
        f"All is lost for {faction}. They've been eradicated.",
        f"{faction} has fallen. There will be no songs sung in their memory.",
        f"The sun has set on the empire of {faction}. Their flame has been extinguished.",
        f"It's a harsh world, and {faction} couldn't survive it. They are now a tale of caution",
        f"The whispers of {faction} fade into the wind. They are no more.",
        f"It's the end of the line for {faction}. Their colors will no longer grace this battlefield.",
        f"{faction} has crumbled to dust, a chapter closed in the annals of history.",
        f"Silence reigns as {faction} takes their final bow. A tragic conclusion to their tale."
    ]
    # Create a narrative-style extinction announcement.
    extinction_paragraph = get_timestamped_message(random.choice(extinction_phrases))

    # Add the extinction announcement to the feed.
    commentary_feed.append(extinction_paragraph)

def announce_winner(faction):
    global commentary_feed, leaderboard
    leaderboard[faction]["wins"] += 1
    victory_phrases = [
        f"The faction {faction} has achieved total domination! All hail the victorious!",
        f"{faction} stands unopposed! Victory is theirs!",
        f"The battle is over. {faction} reigns supreme!",
        f"Against all odds, {faction} has conquered all!",
        f"The arena falls silent as {faction} claims their hard-won throne. A new era begins!",
        f"It's official: {faction} has seized the day! They are the undisputed champions.",
        f"All resistance has crumbled. {faction} now rules unchallenged!",
        f"Victory belongs to {faction}! Their flag flies high over a conquered world.",
        f"The last foe has fallen. {faction} stands alone at the summit of glory!",
        f"In a stunning display of might, {faction} has captured the throne. Long may they reign!"
    ]

    # Randomly select an announcement
    win_paragraph = get_timestamped_message(random.choice(victory_phrases))


    # Add the win announcement to the feed.
    commentary_feed.append(win_paragraph)

def update_commentary():
    global commentary_feed, bottom_right_screen

    bottom_right_screen.clear()
    bottom_right_screen.border()
    current_line = 1  # Initialize to the first line inside the border

    for message in commentary_feed:
        lines_added = safe_addstr(bottom_right_screen, current_line, 1, message)
        current_line += lines_added  # Update the line number for the next message

def update_leaderboard():
    top_right_screen.clear()
    top_right_screen.border()
    top_right_screen.addstr(1, 1, " === Leaderboard ===")

    sorted_families = sorted(leaderboard.items(), key=lambda x: x[1]["wins"], reverse=True)

    top_right_screen.addstr(3, 1, " Rank | Family  | Wins | Losses")
    top_right_screen.addstr(4, 1, " -----|---------|------|-------")
    
    for i, (family, stats) in enumerate(sorted_families):
        rank = i + 1
        wins = stats['wins']
        losses = stats['losses']
        top_right_screen.addstr(i + 5, 2, f"{rank:4} | {family:7} | {wins:4} | {losses:5}")

    top_right_screen.addstr(i + 6, 1, " ==============================")




def introduce_factions():
    global commentary_feed

    # Create a narrative-style introductory paragraph.
    faction_names = ', '.join(families[:-1]) + " versus " + families[-1]
    intro_paragraph = get_timestamped_message(f"{faction_names}!")

    # Add the introductory paragraph to the feed.
    commentary_feed.append(intro_paragraph)

winner = False
introduce_factions()

low_performance_counter = {family: 0 for family in families}
previous_death_rate = None  # Initialize to None to indicate there's no previous data yet

def initialize_grid():
    if choice.lower().strip() == 'yes':
        for i in range(len(families)):
            for x in range((separation[i] * (i + 1)) - 10, (separation[i] * (i + 1))):
                for y in range((((sy + len(families)) // 2) - 5), ((sy // 2) + 5)):
                    chance = random.randint(0, 10)
                    if chance >= 5:
                        cell_screen.addstr(y, x, families[i])
                    else:
                        pass
    else:
        for x in range((sx // 2) - 5, (sx // 2) + 5):
            for y in range((((sy + len(families)) // 2) - 5), ((sy // 2) + 5)):
                chance = random.randint(0, 10)
                if chance >= 5:
                    cell_screen.addstr(y, x, random.choice(families))
                else:
                    pass

def reset_variables():
    global generation, family_dict, percentdict, domination_counter
    global extinction_risk_counter, endangered_flag, extinct_families
    global commentary_feed, previous_death_rate, axis_dict

    generation = 0
    family_dict = {family: 0 for family in families}
    percentdict = {f"{i}_percent": 0 for i in range(len(families))}
    domination_counter = {family: 0 for family in families}
    extinction_risk_counter = {family: 0 for family in families}
    endangered_flag = {family: False for family in families}
    extinct_families.clear()
    previous_death_rate = None
    axis_dict = {f"{family}axis": [0] for family in families}

leaderboard = {family: {"wins": 0, "losses": 0} for family in families}
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

while True:  # Outer loop
    winner = False  # Reset winner flag
    generation = 0  # Reset generation count
    extinct_families.clear()  # Clear extinct families set

    # Initialize the grid
    cell_screen.clear()
    cell_screen.border()
    reset_variables()
    initialize_grid()
    while True and winner == False:
        # stdscr.addstr(0, 0, str(total_left))
        c = stdscr.getch()
        if c == ord('q'):  # Check if 'q' is pressed to quit
            break
        if c == ord(' '):
            paused = not paused
        if c == ord('\t'):
            current_drawing_index = (current_drawing_index + 1) % len(drawing_chars)
            current_drawing_char = drawing_chars[current_drawing_index]
            
            if current_drawing_char == special_char:
                info_screen.addstr(3, 1, f" Current drawing character: {current_drawing_char} (Obstacle)      ")
            elif current_drawing_char == erase_char:
                info_screen.addstr(3, 1, f" Current drawing character: (Erase)         ")
            else:
                info_screen.addstr(3, 1, f" Current drawing character: {current_drawing_char}                 ")
        if not paused:
            sy, sx = cell_screen.getmaxyx()
            cell_screen.border()
            info_screen.border()
            for i in range(len(families)):  # assigns each family a value of 0 at the end of a generation
                family_dict["{0}".format(families[i])] = 0
            death_rate = 0
            total = 1
            for x in range(2, (sx - 2)):  # iterates over the maximum x,y
                for y in range(2, (sy - 2)):  # values minus four for each axis.
                    current_character = chr(cell_screen.inch(y, x))
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
                                family_dict["{0}".format(families[i])] += 1  # Assign that family's dict value +1
                        if neighbors < 2:
                            cell_screen.addstr(y, x, ' ')  # The cell dies :(
                            death_rate = death_rate + 1
                        if neighbors > 3:
                            cell_screen.addstr(y, x, ' ')  # RIP
                            death_rate = death_rate + 1
                    elif current_character == ' ':  # If the current cell is dead:
                        if neighbors == 3:  # AND it has three neighbors:
                            cell_screen.addstr(y, x, most_frequent(surrounding))  # IT'S ALIVE!
                            current_char = cell_screen.inch(y, x)
                            for i in range(len(families)):
                                if current_char == families[i]:
                                    family_dict["{0}".format(families[i])] += 1  # Add new cell to family's dict
            generation = generation + 1
            if generation % 50 == 0:  # Adds all information to the graph if current generation is a multiple of 50
                Gen.append(generation)
                for i in range(len(families)):
                    axis_dict["{0}axis".format(families[i])].append(family_dict["{0}".format(families[i])])
            info_screen.addstr(1, 1, (" Generation: %s     " % generation))  # 'Generation: #' text
            info_screen.addstr(2, 1, (' Death rate: %s     ' % death_rate))  # 'Death rate: #' text
            for i in range(len(families)):
                total += family_dict["{0}".format(families[i])]  # Total is population of all families added together
            for i in range(len(families)):
                # Calculates every family's percentage of domination of the board
                percentdict["{0}_percent".format(i)] = (round((family_dict["{0}".format(families[i])] / total) * 100, 2))
                percent = round(percentdict["{0}_percent".format(i)], 0)
                # Family character followed by sliding bar
                info_screen.addstr(i + 4, 1, ' {} |'.format(families[i]) + '█' * (int(percent) // 2) +
                                ('-' * (50 - (int(percent) // 2)) + '|') + ' {}%'.format(
                    percentdict["{0}_percent".format(i)]))
            for i in range(len(families)):
                if percentdict["{0}_percent".format(i)] < 10 and percentdict["{0}_percent".format(i)] > 0:  # 5% is the threshold for "risk of extinction"
                    extinction_risk_counter[families[i]] += 1  # Increment the counter for this faction
                    
                    if extinction_risk_counter[families[i]] == 350:  # 100 generations as a threshold for the announcement
                        announce_extinction_risk(families[i])
                        extinction_risk_counter[families[i]] = 0  # You could reset the counter or keep it at 100 to prevent spamming
                else:
                    extinction_risk_counter[families[i]] = 0
            for i in range(len(families)):
                if percentdict["{0}_percent".format(i)] > 50:  # Change 50 to the percentage you consider as "domination"
                    domination_counter[families[i]] += 1  # Increment the domination counter for this faction
                    
                    if domination_counter[families[i]] == 1000:  # If dominated for 1000 generations
                        announce_domination(families[i])
                        domination_counter[families[i]] = 0  # Reset the counter
                else:
                    domination_counter[families[i]] = 0
            for i in range(len(families)):
                if percentdict["{0}_percent".format(i)] < 5:  # 5% is the threshold for "risk of extinction"
                    endangered_flag[families[i]] = True  # Set the endangered flag
                    
                elif percentdict["{0}_percent".format(i)] > 20:  # 20% is the threshold for recovery
                    if endangered_flag[families[i]]:  # Check if this family was endangered
                        announce_comeback(families[i])
                        endangered_flag[families[i]] = False  # Reset the flag
            for i in range(len(families)):
                if percentdict["{0}_percent".format(i)] == 0:
                    if families[i] not in extinct_families:
                        announce_extinct(families[i])
                        #play_sound('extinction0')
                        extinct_families.add(families[i])
                else:
                    # If a previously extinct faction reappears, remove it from the extinct list
                    if families[i] in extinct_families:
                        extinct_families.remove(families[i])
            if previous_death_rate is not None:  # Skip this for the first generation
                percent_change = ((death_rate - previous_death_rate) / previous_death_rate) * 100

                if percent_change >= 2:  # You can adjust this threshold as needed
                    announce_spike()
                elif percent_change <= -2:  # Negative indicates a drop; adjust this threshold as needed
                    announce_drop()
            for i in range(len(families)):
                if percentdict["{0}_percent".format(i)] >= 99.98 and generation > 10:
                    announce_winner(families[i])
                    winner = True
                    break
            update_commentary()
        # Refresh all screens and windows
        else:
            # Drawing or erasing cells during pause
            if c == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                # Calculate the adjusted mouse coordinates
                adjusted_my = my - (len(families) + 6)
                adjusted_mx = mx
                cell_screen_height, cell_screen_width = cell_screen.getmaxyx()
                
                # Check if the adjusted coordinates are within the window boundaries
                if 0 <= adjusted_my < cell_screen_height and 0 <= adjusted_mx < cell_screen_width:
                    cell_screen.addstr(adjusted_my, adjusted_mx, current_drawing_char)

            elif c in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                # Move the cursor using arrow keys and erase or draw
                # Logic for updating the cell based on arrow key goes here
                pass


        stdscr.refresh()
        cell_screen.refresh()
        info_screen.refresh()
        top_right_screen.refresh()
        bottom_right_screen.refresh()
        update_leaderboard()
    time.sleep(10)
    if c == ord('q'):
        break
    commentary_feed.clear()
    stdscr.clear()
    cell_screen.clear()
    info_screen.clear()
    bottom_right_screen.erase()
    update_leaderboard()



# Finish creating and show the graph and program termination
for i in range(len(families)):
    plt.plot(Gen, axis_dict["{0}axis".format(families[i])], label=families[i])
plt.style.use('dark_background')
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

