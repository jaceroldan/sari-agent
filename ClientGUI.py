import tkinter as tk
from tkinter import font
from ClientSide import (
    _MOVE_FWD_,
    _MOVE_BCK_,
    _MOVE_LEFT_,
    _MOVE_RIGHT_,
    _PAN_LEFT_,
    _PAN_RIGHT_,
    _GRIP_LEFT_,
    _GRIP_RIGHT_,
    _XTNFWD_LEFT_,
    _XTNFWD_RIGHT_,
    _PLLBCK_LEFT_,
    _PLLBCK_RIGHT_,
    _PAN_UP_,
    _PAN_DOWN_,
    _RSE_LEFT_,
    _LWR_LEFT_,
    _RSE_RIGHT_,
    _LWR_RIGHT_
)

def on_key(event):
    controls = {
        'w': _MOVE_FWD_,
        's': _MOVE_BCK_,
        'a': _MOVE_LEFT_,
        'd': _MOVE_RIGHT_,
        'q': _PAN_LEFT_,
        'e': _PAN_RIGHT_,
        'u': _XTNFWD_LEFT_,
        'o': _XTNFWD_RIGHT_,
        'h': _PLLBCK_LEFT_,
        'k': _PLLBCK_RIGHT_,
        'b': _GRIP_LEFT_,
        'm': _GRIP_RIGHT_,
        'i': _PAN_UP_,
        'j': _PAN_DOWN_,
        'y': _RSE_LEFT_,
        'g': _LWR_LEFT_,
        'p': _RSE_RIGHT_,
        'l': _LWR_RIGHT_
    }
    action = controls.get(event.keysym)
    if action:
        action()


for _ in range(16):
    _RSE_LEFT_()
    _RSE_RIGHT_()


root = tk.Tk()
root.title('Sari-Sari Environment V1 Agent Controls')
root.bind("<KeyPress>", on_key)

heading_font = font.Font(size=20, family='Courier', underline=True)
buttons_font = font.Font(size=9, family='Courier')

heading_frame = tk.Frame(root)
tk.Label(heading_frame, text='Agent Controls', bg='black', fg='white', font=heading_font).pack(side=tk.TOP)
heading_frame.pack()

controls_frame = tk.Frame(root)
tk.Button(controls_frame, text='Move Forward\n(W)', bg='black', fg='white',
          font=buttons_font, command=_MOVE_FWD_).grid(row=0, column=1)

tk.Button(controls_frame, text='Move Backward\n(S)', bg='black', fg='white',
          font=buttons_font, command=_MOVE_BCK_).grid(row=2, column=1)

tk.Button(controls_frame, text='Move Left\n(A)', bg='black', fg='white',
          font=buttons_font, command=_MOVE_LEFT_).grid(row=1, column=0, pady=10)

tk.Button(controls_frame, text='Move Right\n(D)', bg='black', fg='white',
          font=buttons_font, command=_MOVE_RIGHT_).grid(row=1, column=2, pady=10)

tk.Button(controls_frame, text='Pan Left\n(Q)', bg='black', fg='white',
          font=buttons_font, command=_PAN_LEFT_).grid(row=0, column=0)

tk.Button(controls_frame, text='Pan Right\n(E)', bg='black', fg='white',
          font=buttons_font, command=_PAN_RIGHT_).grid(row=0, column=2)

tk.Button(controls_frame, text='Pan Up\n(I)', bg='black', fg='white',
          font=buttons_font, command=_PAN_UP_).grid(row=2, column=0)

tk.Button(controls_frame, text='Pan Down\n(J)', bg='black', fg='white',
          font=buttons_font, command=_PAN_DOWN_).grid(row=2, column=2)

controls_frame.pack(side=tk.LEFT, pady=10)


hands_frame = tk.Frame(root)
tk.Button(hands_frame, text='Raise Left Hand\n(Y)', bg='black', fg='white',
          font=buttons_font, command=_RSE_LEFT_).grid(row=0, column=0, pady=10)

tk.Button(hands_frame, text='Raise Right Hand\n(P)', bg='black', fg='white',
          font=buttons_font, command=_RSE_RIGHT_).grid(row=0, column=1, pady=10)

tk.Button(hands_frame, text='Extend Left Hand\n(U)', bg='black', fg='white',
          font=buttons_font, command=_XTNFWD_LEFT_).grid(row=1, column=0, pady=10)

tk.Button(hands_frame, text='Extend Right Hand\n(O)', bg='black', fg='white',
          font=buttons_font, command=_XTNFWD_RIGHT_).grid(row=1, column=1, pady=10)

tk.Button(hands_frame, text='Retract Left Hand\n(H)', bg='black', fg='white',
          font=buttons_font, command=_PLLBCK_LEFT_).grid(row=2, column=0, padx=10)

tk.Button(hands_frame, text='Retract Right Hand\n(K)', bg='black', fg='white',
          font=buttons_font, command=_PLLBCK_RIGHT_).grid(row=2, column=1, padx=10)

tk.Button(hands_frame, text='Toggle Left Grip\n(B)', bg='black', fg='white',
          font=buttons_font, command=_GRIP_LEFT_).grid(row=3, column=0, pady=10)

tk.Button(hands_frame, text='Toggle Right Grip\n(M)', bg='black', fg='white',
          font=buttons_font, command=_GRIP_RIGHT_).grid(row=3, column=1, pady=10)

tk.Button(hands_frame, text='Lower Left Hand\n(G)', bg='black', fg='white',
          font=buttons_font, command=_LWR_LEFT_).grid(row=4, column=0, pady=10)

tk.Button(hands_frame, text='Lower Right Hand\n(L)', bg='black', fg='white',
          font=buttons_font, command=_LWR_RIGHT_).grid(row=4, column=1, pady=10)

hands_frame.pack(side=tk.RIGHT, pady=10)

root.mainloop()