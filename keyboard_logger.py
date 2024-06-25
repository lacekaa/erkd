import keyboard
import time
import pandas as pd
import atexit

# List to store the key event data
key_events = []

# List to store time calculations
time_calculations = []


def on_key_event(event):
    key_name = event.name
    event_type = event.event_type
    event_time = time.time()

    if event_type == 'down':
        key_events.append({'key': key_name, 'press_time': event_time, 'release_time': None})
        print(f"Key {key_name} pressed at {event_time}")
    elif event_type == 'up':
        for key_event in key_events:
            if key_event['key'] == key_name and key_event['release_time'] is None:
                key_event['release_time'] = event_time
                print(f"Key {key_name} released at {event_time}")
                break

        # Calculate D1U1, D1U2, and D1U3
        D1U1 = key_event['release_time'] - key_event['press_time'] if key_event['release_time'] else None
        D1U2 = key_event['release_time'] - key_events[-2]['press_time'] if len(key_events) >= 2 and key_event[
            'release_time'] else None
        D1U3 = key_event['release_time'] - key_events[-3]['press_time'] if len(key_events) >= 3 and key_event[
            'release_time'] else None

        time_calculations.append({
            'key': key_name,
            'D1U1': D1U1,
            'D1U2': D1U2,
            'D1U3': D1U3,
        })

        print(f"D1U1 for {key_name}: {D1U1}")
        print(f"D1U2 for {key_name}: {D1U2}")
        print(f"D1U3 for {key_name}: {D1U3}")


def save_to_csv():
    df_times = pd.DataFrame(time_calculations)

    # Calculate mean values for D1U1, D1U2, D1U3
    D1U1_mean = df_times['D1U1'].mean() if 'D1U1' in df_times else None
    D1U2_mean = df_times['D1U2'].mean() if 'D1U2' in df_times else None
    D1U3_mean = df_times['D1U3'].mean() if 'D1U3' in df_times else None

    df_times['D1U1_mean'] = D1U1_mean
    df_times['D1U2_mean'] = D1U2_mean
    df_times['D1U3_mean'] = D1U3_mean

    df_times.to_csv('key_times.csv', index=False)
    print("Key events and time calculations have been saved to CSV file.")


# Hook the keyboard events
keyboard.hook(on_key_event)

# Register the save_to_csv function to be called on program exit
atexit.register(save_to_csv)

# Block the script so it keeps running and listening for events
keyboard.wait('esc')  # Change this to any key you want to stop the script
