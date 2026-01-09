import time

import musicalbeeps

scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
volumes = [0.02 + 0.2 * x / 11 for x in range(12)]
players = [musicalbeeps.Player() for _ in range(4)]


counter = 0
while True:
    for i, p in enumerate(players):
        p.volume = volumes[counter if i & 1 == 0 else -counter]
        base = scale[counter]
        note = base[:1] + str(i + 1) + base[1:]
        p.play_note(note, 0.35)

    time.sleep(0.2)
    counter = (counter + 1) % len(scale)
