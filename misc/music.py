from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from math import pow
from typing import NewType, Self


# Definitions


class Note(IntEnum):
    C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B = range(12)


class Steps(IntEnum):
    Unison, MinorSecond, MajorSecond, MinorThird, MajorThird, Fourth, Tritone, Fifth, MinorSixth, MajorSixth, MinorSeventh, MajorSeventh, Octave = range(13)  # fmt: skip # noqa: E501


Scale = NewType("Scale", list[int])
Chord = NewType("Chord", list[Steps])


@dataclass(frozen=True)
class Pitch:
    semitone: int  # absolute, C0 = 0

    @classmethod
    def new(cls, note: Note, octave: int) -> Self:
        return cls(octave * Steps.Octave + note)

    def note(self) -> Note:
        pc = self.semitone % Steps.Octave
        return Note(pc)

    def octave(self) -> int:
        return self.semitone // Steps.Octave

    def frequency(self) -> float:
        a4_semitone = Pitch.new(Note.A, 4).semitone
        a4_freq = 440.0
        return a4_freq * pow(2.0, (self.semitone - a4_semitone) / Steps.Octave)

    def scale(self, scale: Scale) -> list[Pitch]:
        notes = [Pitch(self.semitone)]
        acc = self.semitone
        for s in scale[:-1]:
            acc += s
            notes.append(Pitch(acc))
        return notes

    def chord(self, chord: Chord) -> list[Pitch]:
        return [self + i for i in chord]

    def __add__(self, steps: Steps) -> Pitch:
        return Pitch(self.semitone + steps)

    def __str__(self) -> str:
        return f"{self.note().name.replace('s', '#')}{self.octave()}"


# Common Scales & Chords

MAJOR_SCALE = Scale([2, 2, 1, 2, 2, 2, 1])
MINOR_SCALE = Scale([2, 1, 2, 2, 1, 2, 2])

MAJOR_TRIAD = Chord([Steps.Unison, Steps.MajorThird, Steps.Fifth])
MINOR_TRIAD = Chord([Steps.Unison, Steps.MinorThird, Steps.Fifth])
DOM7 = Chord(
    [
        Steps.Unison,
        Steps.MajorThird,
        Steps.Fifth,
        Steps.MinorSeventh,
    ]
)


# =========================

if __name__ == "__main__":
    e2 = Pitch.new(Note.E, 2)

    print(f"{e2}: ", round(e2.frequency(), 2), "Hz")

    print("\nE2 major scale:")
    print([str(n) for n in e2.scale(MAJOR_SCALE)])

    print("\nE2 minor chord:")
    print([str(n) for n in e2.chord(MINOR_TRIAD)])

    # Equality check
    assert e2 + Steps.Fifth == Pitch.new(Note.B, 2)
