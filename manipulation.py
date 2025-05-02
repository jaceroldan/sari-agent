from ClientSide import (
    _XTNFWD_LEFT_,
    _XTNFWD_RIGHT_,
    _GRIP_LEFT_,
    _GRIP_RIGHT_,
    _PLLBCK_LEFT_,
    _PLLBCK_RIGHT_,
    _RSE_LEFT_,
    _RSE_RIGHT_,
    _REQUEST_SCREENSHOT_,
    _ROT_LEFT_CLOCK_,
    _ROT_RIGHT_CLOCK_
)

def reach_and_grasp(hand='left', max_attempts=20):
    grasped = False
    attempts = 0

    while not grasped and attempts < max_attempts:
        if hand == 'left':
            _XTNFWD_LEFT_()  # e.g., moves hand slightly forward
            grasped = _GRIP_LEFT_()
        elif hand == 'right':
            _XTNFWD_RIGHT_()
            grasped = _GRIP_RIGHT_()
        attempts += 1

    return grasped, attempts



def pull_back(hand='left', max_frames=10):
    texts_detected = []
    frames_captured = 0

    while frames_captured < max_frames:
        if hand == 'left':
            _PLLBCK_LEFT_()
        elif hand == 'right':
            _PLLBCK_RIGHT_()
        
        frames_captured += 1


def rotate_and_read(hand="left", max_frames=10, retract_steps=5, text_read_fn=None):
    # Step 2: Rotate and OCR
    texts = []
    rotate_fn = _ROT_LEFT_CLOCK_ if hand == 'left' else _ROT_RIGHT_CLOCK_

    for i in range(24):  # Full 360° sweep
        _REQUEST_SCREENSHOT_()
        if text_read_fn:
            texts.append(text_read_fn())
        rotate_fn()
    return texts


def raise_hand_to_eye_level(hand="left", raise_steps=5):
    if hand == "left":
        for i in range(raise_steps):
            _RSE_LEFT_()
    elif hand == "right":
        for i in range(raise_steps):
            _RSE_RIGHT_()


def grab_and_read_item(hand="left", max_attempts=30):
    accessed, attempts = reach_and_grasp(hand=hand, max_attempts=max_attempts)
    if accessed:
        pull_back(hand=hand, max_frames=attempts//2)
        raise_hand_to_eye_level(hand=hand)
        return rotate_and_read(hand="left")
    return ["No object grabbed"]
