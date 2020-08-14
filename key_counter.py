from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import json
import time


keyboard_save_count = 0
mouse_save_count = 0
mouse_cooldown = 0
test_mode = True

f = open('key_counts.json')
counts = json.load(f)

##with open('key_counts.json') as f:
##    for jsonObj in f:
##        countsDict = json.loads(jsonObj)
##        counts.append(countsDict)

##def quick_save():
##    current_time = time.strftime("%H:%M:%S", time.localtime())
##    print("Quick saved at "+current_time+". Save number:",counts["save"]["total_saves"])
##    counts["save"]["total_saves"] += 1
##    counts["save"]["last_save"]=time.ctime()
##    with open('key_counts.json',"w") as f:
##        json.dump(counts,f)
##
##keyboard.add_hotkey('ctrl+shift+s', quick_save())

def save_check():
    global keyboard_save_count
    global mouse_save_count
    current_time = time.strftime("%H:%M:%S", time.localtime())
    if test_mode == True:
        print("Save function called")
    if keyboard_save_count >= 1500:
        print("Keyboard triggered save at "+current_time+". Save number:",counts["save"]["total_saves"])
        counts["save"]["total_saves"] += 1
        counts["save"]["last_save"]=time.ctime()
        with open('key_counts.json',"w") as f:
            json.dump(counts,f)
        keyboard_save_count = 0
        
    if mouse_save_count >= 2500:
        print("Mouse triggered save at "+current_time+". Save number:",counts["save"]["total_saves"])
        counts["save"]["total_saves"] += 1
        counts["save"]["last_save"] = time.ctime()
        with open('key_counts.json',"w") as f:
            json.dump(counts,f)
        mouse_save_count = 0
        
def on_release(key):
    global keyboard_save_count
    keyboard_save_count = keyboard_save_count
    try:
        try:
            k = key.char  # single-char keys
            if test_mode == True:
                print("Key pressed:",k)
                print("Keypress count: "+str(keyboard_save_count))
            try:
                k_lower = str.lower(k)
                counts["key"][k_lower] += 1
                keyboard_save_count += 1
                save_check()
            except:
                try:
                    counts["key"][k] += 1
                    keyboard_save_count += 1
                    save_check()
                except:
                    k = "Â"+k
                    counts["key"][k] += 1
                    keyboard_save_count += 1
                    save_check()
        except:
            k = key.name  # other keys
            if test_mode == True:
                print("Keypressed:",k)
                print("Keypress count: "+str(keyboard_save_count))
            keyboard_save_count += 1
            counts["key"][k] += 1
            save_check()
    except:
        counts["key"]["errors"] += 1
        print("Key press unrecognised")
        keyboard_save_count += 1
        save_check()

def on_click(x, y, button, pressed):
    global mouse_save_count
    global mouse_cooldown
    if test_mode == True:
        print("Mouse clicked with",format(button))
    if "Button.left" in str(button):
        counts["key"]["Button.left"] += int(0.5)
        mouse_save_count += 0.5
        mouse_cooldown += 0.5
        if mouse_cooldown >= 15:
            save_check()
            mouse_cooldown = 0
    elif "Button.right" in str(button):
        counts["key"]["Button.right"] += 0.5
        mouse_save_count += 0.5
        mouse_cooldown += 0.5
        if mouse_cooldown >= 15:
            save_check()
            mouse_cooldown = 0
    elif "Button.middle" in str(button):
        counts["key"]["Button.middle"] += 0.5
        mouse_save_count += 0.5
        mouse_cooldown += 0.5
        if mouse_cooldown >= 15:
            save_check()
            mouse_cooldown = 0
    else:
        counts["key"]["errors"] += 1
        print("Mouse click unrecognised")
        mouse_save_count += 1
        save_check()

print("Initialised")

with MouseListener(on_click=on_click) as listener:
    with KeyboardListener(on_release=on_release) as listener:
        listener.join()
        
