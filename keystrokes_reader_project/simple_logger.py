import csv
from pynput import keyboard
import time

key_events = []
running = True  # Flag to control the running of the listener

def on_press(key):
    try:
        key_events.append({'key': key.char, 'down': time.time(), 'up': None})
    except AttributeError:
        key_events.append({'key': str(key), 'down': time.time(), 'up': None})

def on_release(key):
    for event in reversed(key_events):
        if event['key'] == (getattr(key, 'char', str(key))) and event['up'] is None:
            event['up'] = time.time()
            break
    if key == keyboard.Key.esc:
        global running
        running = False  # Set the flag to False to stop the loop
        return False  # Stop listener

def write_to_csv(events, filename='key_times.csv'):
    with open(filename, 'w', newline='') as file:
        fieldnames = ['key', 'down', 'up']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for event in events:
            writer.writerow(event)

def main():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()  # Start the listener in a separate thread
    try:
        while running:  # Keep the main thread alive until ESC is pressed
            time.sleep(0.1)
    finally:
        listener.stop()  # Ensure the listener is stopped
        write_to_csv(key_events)  # Write events to CSV

if __name__ == "__main__":
    main()