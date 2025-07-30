from enum import Enum
from QR_Code_Generator import GenerateQR as qr
import galois

class data_mode(Enum):
    NUMERIC = {"name" : "numeric", 
               "indicator" : "0001"}
    ALPHANUMERIC = {"name" : "alphanumeric",
                    "indicator" : "0010"}
    BYTE = {"name" : "byte", 
            "indicator" : "0100"}
    KANJI = {"name" : "kanji", 
            "indicator" : "1000"}

class ecc_level(Enum):
    L = {"name" : "L", 
               "indicator" : "01"}
    M = {"name" : "M", 
               "indicator" : "00"}
    Q = {"name" : "Q", 
               "indicator" : "11"}
    H = {"name" : "H", 
               "indicator" : "10"}

# True is black
# False is white

QR_SEPERATOR = (False,False,False,False,False,False,False,False)

QR_ALIGNMENT_PATTERN = (
    (True,True,True,True,True),
    (True,False,False,False,True),
    (True,False,True,False,True),
    (True,False,False,False,True),
    (True,True,True,True,True)
    )

QR_FINDER_PATTERN = (
    (True,True,True,True,True,True,True),
    (True,False,False,False,False,False,True),
    (True,False,True,True,True,False,True),
    (True,False,True,True,True,False,True),
    (True,False,True,True,True,False,True),
    (True,False,False,False,False,False,True),
    (True,True,True,True,True,True,True)
    )  

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

PADDING_BYTES = ('11101100', '00010001')

BYTE_WISE_MODULO = 285

GALOIS_FIELD_MODULO = 255

GALOIS_FIELD_256 = galois.GF(2**8)

def alpha_to_coef(exp: int):
        result = 1
        exp = int(exp)
        for i in range(exp):
                result *= GALOIS_FIELD_256.primitive_element
                if result >= 256:
                    result ^= BYTE_WISE_MODULO
        return result

def coef_to_alpha(coef: int):
    return GALOIS_FIELD_256(coef).log(GALOIS_FIELD_256.primitive_element)
