import pyautogui
import random
import tkinter as tk

x = 1400
cycle = 0
check = 1

idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]
special_events = [16, 17, 18]  # New events for blink, twitch, and head tilt

event_number = random.choice(idle_num + sleep_num + walk_left + walk_right + special_events)
impath = 'C:\\Users\\haile\\Documents\\GitHub\\Cat\\CatGifs\\'

# Define random events
def event(cycle, check, event_number, x):
    if event_number in idle_num:
        check = 0
        print('idle')
    elif event_number in walk_left:
        check = 4
        print('walking towards left')
    elif event_number in walk_right:
        check = 5
        print('walking towards right')
    elif event_number in sleep_num:
        check = 2
        print('sleep')
    elif event_number == 16:
        check = 6
        print('blink')
    elif event_number == 17:
        check = 7
        print('twitch')
    elif event_number == 18:
        check = 8
        print('head tilt')
    window.after(400 if check == 0 else 100, update, cycle, check, event_number, x)

# Function to loop through frames
def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.choice(idle_num + sleep_num + walk_left + walk_right + special_events)
    return cycle, event_number

# Update function
def update(cycle, check, event_number, x):
    if check == 0:  # Idle
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle, idle, event_number, 1, 9)
    elif check == 2:  # Sleep
        frame = sleep[cycle]
        cycle, event_number = gif_work(cycle, sleep, event_number, 10, 15)
    elif check == 4:  # Walk left
        frame = walk_positive[cycle]
        cycle, event_number = gif_work(cycle, walk_positive, event_number, 1, 9)
        x -= 3
    elif check == 5:  # Walk right
        frame = walk_negative[cycle]
        cycle, event_number = gif_work(cycle, walk_negative, event_number, 1, 9)
        x += 3
    elif check == 6:  # Blink
        frame = blink[cycle]
        cycle, event_number = gif_work(cycle, blink, event_number, 16, 16)
    elif check == 7:  # Twitch
        frame = twitch[cycle]
        cycle, event_number = gif_work(cycle, twitch, event_number, 17, 17)
    elif check == 8:  # Head tilt
        frame = head_tilt[cycle]
        cycle, event_number = gif_work(cycle, head_tilt, event_number, 18, 18)

    window.geometry(f'100x100+{x}+1050')
    label.configure(image=frame)
    window.after(1, event, cycle, check, event_number, x)

# Setup Tkinter window
window = tk.Tk()
idle = [tk.PhotoImage(file=impath + 'Idle.gif', format='gif -index %i' % i) for i in range(25)]
sleep = [tk.PhotoImage(file=impath + 'Snooze.gif', format='gif -index %i' % i) for i in range(27)]
walk_positive = [tk.PhotoImage(file=impath + 'WalkLeft.gif', format='gif -index %i' % i) for i in range(12)]
walk_negative = [tk.PhotoImage(file=impath + 'WalkRight.gif', format='gif -index %i' % i) for i in range(12)]
blink = [tk.PhotoImage(file=impath + 'Blink.gif', format='gif -index %i' % i) for i in range(8)]
twitch = [tk.PhotoImage(file=impath + 'EarTwitch.gif', format='gif -index %i' % i) for i in range(8)]
head_tilt = [tk.PhotoImage(file=impath + 'HeadTilt.gif', format='gif -index %i' % i) for i in range(20)]

# Window configuration
window.config(highlightbackground='black')
label = tk.Label(window, bd=0, bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor', 'black')
label.pack()

# Start the program
window.after(1, update, cycle, check, event_number, x)
window.mainloop()