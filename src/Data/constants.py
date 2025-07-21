from enum import Enum

class data_mode(Enum):
    NUMERIC = "numeric"
    ALPHANUMERIC = "alphanumeric"
    BYTE = "byte"
    KANJI = "kanji"

class ecc_level(Enum):
    L = ["L", 0.07]
    M = ["M", 0.15]
    Q = ["Q", 0.25]
    H = ["H", 0.3]

QR_CORNER = [
    [True,True,True,True,True,True,True],
    [True,False,False,False,False,False,True],
    [True,False,True,True,True,False,True],
    [True,False,True,True,True,False,True],
    [True,False,True,True,True,False,True],
    [True,False,False,False,False,False,True],
    [True,True,True,True,True,True,True]
    ]  

QR_VERSION_SIZES = {
    1:21,
    2:25,
    3:29,
    4:33,
    5:37,
    6:41,
    7:45,
    8:49,
    9:53
    }

MODE_INDICATOR = {
    data_mode.NUMERIC:"0001",
    data_mode.ALPHANUMERIC:"0010",
    data_mode.BYTE:"0100",
    data_mode.KANJI:"1000",
    data_mode.ECI:"0111"
    }

ALPHANUMERIC_TO_INT = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
    "G": 16,
    "H": 17,
    "I": 18,
    "J": 19,
    "K": 20,
    "L": 21,
    "M": 22,
    "N": 23,
    "O": 24,
    "P": 25,
    "Q": 26,
    "R": 27,
    "S": 28,
    "T": 29,
    "U": 30,
    "V": 31,
    "W": 32,
    "X": 33,
    "Y": 34,
    "Z": 35,
    " ": 36,
    "$": 37,
    "%": 38,
    "*": 39,
    "+": 40,
    "-": 41,
    ".": 42,
    "/": 43,
    ":": 44
}

