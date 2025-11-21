from enum import IntEnum, StrEnum


class PROFICIENCY_LEVELS(StrEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class DIFFICULTY(IntEnum):
    BEGINNER = 1
    ELEMENTARY = 2
    INTERMEDIATE = 3
    UPPER_INTERMEDIATE = 4
    ADVANCED = 5


class RATE(IntEnum):
    NOVICE = 1
    BEGINNER = 2
    COMPETENT = 3
    PROFICIENT = 4
    EXPERT = 5
