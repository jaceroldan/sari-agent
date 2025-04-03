import tkinter as tk
import ClientSide as a  # Assuming this is your WebSocket client
import os

move_count = 0
suffix = 0
run_number = ""
folder_name = ""

def update_screenshot():
    global move_count, suffix
    move_count += 1
    if move_count % 5 == 0:
        suffix += 1
        a.RequestScreenshot(prefix=f"run_{run_number}", suffix=f"_{suffix}", folder_name=folder_name)

def set_run_number():
    global run_number, move_count, suffix
    run_number = run_entry.get()
    run_entry.delete(0, tk.END)  # Clear entry field
    run_label.config(text=f"Current Run: {run_number}")  # Update indicator
    root.focus_set()  # Remove focus from entry
    move_count = 0
    suffix = 0

def set_folder():
    global folder_name, move_count, suffix
    folder_name = folder_entry.get()
    folder_entry.delete(0, tk.END)  # Clear entry field
    folder_label.config(text=f"Current Folder: {folder_name}")  # Update label
    root.focus_set()  # Remove focus from entry
    move_count = 0
    suffix = 0

def move_forward():
    a.TransformAgent((0, 0, 0.02), (0, 0, 0))
    update_screenshot()

def move_backward():
    a.TransformAgent((0, 0, -0.02), (0, 0, 0))
    update_screenshot()

def move_left():
    a.TransformAgent((-0.02, 0, 0), (0, 0, 0))
    update_screenshot()

def move_right():
    a.TransformAgent((0.02, 0, 0), (0, 0, 0))
    update_screenshot()

def rotate_left():
    a.TransformAgent((0, 0, 0), (0, -10, 0))
    update_screenshot()

def rotate_right():
    a.TransformAgent((0, 0, 0), (0, 10, 0))
    update_screenshot()

def grip_left():
    a.ToggleLeftGrip()

def grip_right():
    a.ToggleRightGrip()

def extend_left_hand():
    a.TransformHands((0, 0, 0.02), (0, 0, 0), (0, 0, 0), (0, 0, 0))
    update_screenshot()

def retract_left_hand():
    a.TransformHands((0, 0, -0.02), (0, 0, 0), (0, 0, 0), (0, 0, 0))
    update_screenshot()

def extend_right_hand():
    a.TransformHands((0, 0, 0), (0, 0, 0), (0, 0, 0.02), (0, 0, 0))
    update_screenshot()

def retract_right_hand():
    a.TransformHands((0, 0, 0), (0, 0, 0), (0, 0, -0.02), (0, 0, 0))
    update_screenshot()

def screenshot():
    a.RequestScreenshot(prefix=f"run_{run_number}", suffix=f"_{suffix}", folder_name=folder_name)

def on_key(event):
    if root.focus_get() != run_entry and root.focus_get() != folder_entry:
        key_actions = {
            'w': move_forward,
            's': move_backward,
            'a': move_left,
            'd': move_right,
            'Left': rotate_left,
            'Right': rotate_right,
            'l': grip_left,
            'r': grip_right,
            'e': extend_right_hand,
            'q': retract_right_hand,
            'z': extend_left_hand,
            'x': retract_left_hand
        }
        action = key_actions.get(event.keysym)
        if action:
            action()

# Create UI
root = tk.Tk()
root.title("Agent Controller")
root.bind("<KeyPress>", on_key)

# Run number input
run_frame = tk.Frame(root)
tk.Label(run_frame, text="Run Number:").pack(side=tk.LEFT)
run_entry = tk.Entry(run_frame)
run_entry.pack(side=tk.LEFT)
set_run_button = tk.Button(run_frame, text="Set Run", command=set_run_number)
set_run_button.pack(side=tk.RIGHT)
run_frame.pack()

run_label = tk.Label(root, text="Current Run: None")
run_label.pack()

# Folder input
folder_frame = tk.Frame(root)
tk.Label(folder_frame, text="Folder Name:").pack(side=tk.LEFT)
folder_entry = tk.Entry(folder_frame)
folder_entry.pack(side=tk.LEFT)
set_folder_button = tk.Button(folder_frame, text="Set Folder", command=set_folder)
set_folder_button.pack(side=tk.RIGHT)
folder_frame.pack()

folder_label = tk.Label(root, text="Current Folder: None")
folder_label.pack()

# Movement buttons
movement_frame = tk.Frame(root)
tk.Button(movement_frame, text="Forward (W)", command=move_forward).grid(row=0, column=1)
tk.Button(movement_frame, text="Left (A)", command=move_left).grid(row=1, column=0)
tk.Button(movement_frame, text="Right (D)", command=move_right).grid(row=1, column=2)
tk.Button(movement_frame, text="Backward (S)", command=move_backward).grid(row=2, column=1)
tk.Button(movement_frame, text="Rotate Left (←)", command=rotate_left).grid(row=3, column=0)
tk.Button(movement_frame, text="Rotate Right (→)", command=rotate_right).grid(row=3, column=2)
movement_frame.pack()

# Hand controls
grip_frame = tk.Frame(root)
tk.Button(grip_frame, text="Toggle Left Grip (L)", command=grip_left).pack(side=tk.LEFT)
tk.Button(grip_frame, text="Toggle Right Grip (R)", command=grip_right).pack(side=tk.RIGHT)
grip_frame.pack()

# Hand extension/retraction
hand_frame = tk.Frame(root)
tk.Button(hand_frame, text="Extend Left Hand (Z)", command=extend_left_hand).pack(side=tk.LEFT)
tk.Button(hand_frame, text="Retract Left Hand (X)", command=retract_left_hand).pack(side=tk.LEFT)
tk.Button(hand_frame, text="Extend Right Hand (E)", command=extend_right_hand).pack(side=tk.RIGHT)
tk.Button(hand_frame, text="Retract Right Hand (Q)", command=retract_right_hand).pack(side=tk.RIGHT)
hand_frame.pack()

# Screenshot button
tk.Button(root, text="Take Screenshot", command=screenshot).pack()

root.mainloop()
