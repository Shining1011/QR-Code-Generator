from enum import Enum
from QR_Code_Generator import GenerateQR as qr
import galois
import math as m
import numpy as np

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
    L = {
        "name" : "L", 
        "indicator" : "01"
        }
    M = {
        "name" : "M", 
        "indicator" : "00"
        }
    Q = {
        "name" : "Q", 
        "indicator" : "11"
        }
    H = {
        "name" : "H", 
        "indicator" : "10"
        }

class mask_level(Enum):
    VER_0 = {
        "formula" : lambda r,c: (r+c)%2==0,
        "indicator" : "000",
        }
    VER_1 = {
        "formula" : lambda r,c: r%2==0,
        "indicator" : "001",
        }
    VER_2 = {
        "formula" : lambda r,c: c%3==0,
        "indicator" : "010",
        }
    VER_3 = {
        "formula" : lambda r,c: (r+c)%3==0,
        "indicator" : "011",
        }
    VER_4 = {
        "formula" : lambda r,c: (m.floor(float(r)/2)+m.floor(float(c)/2))%2==0,
        "indicator" : "100",
        }
    VER_5 = {
        "formula" : lambda r,c: ((r*c)%2)+((r*c)%3)==0,
        "indicator" : "101",
        }
    VER_6 = {
        "formula" : lambda r,c: (((r*c)%2)+((r*c)%3))%2==0,
        "indicator" : "110",
        }
    VER_7 = {
        "formula" : lambda r,c: (((r+c)%2)+((r*c)%3))%2==0,
        "indicator" : "111",
        }
    
QR_SEPERATOR = ("0","0","0","0","0","0","0","0")

QR_ALIGNMENT_PATTERN = (
    ("1","1","1","1","1"),
    ("1","0","0","0","1"),
    ("1","0","1","0","1"),
    ("1","0","0","0","1"),
    ("1","1","1","1","1")
    )

QR_FINDER_PATTERN = (
    ("1","1","1","1","1","1","1"),
    ("1","0","0","0","0","0","1"),
    ("1","0","1","1","1","0","1"),
    ("1","0","1","1","1","0","1"),
    ("1","0","1","1","1","0","1"),
    ("1","0","0","0","0","0","1"),
    ("1","1","1","1","1","1","1")
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

MASK_TEST_3 = ("1","0","1","1","1","0","1","0","0","0")
MASK_TEST_3_REVERSED = ("0","0","0","1","0","1","1","1","0","1")

# Equals x^10 + x^8 + x^5 + x^4 + x^2 + x + 1, values represent powers of alpha coef
FORMAT_GENERATOR_POLYNOMIAL="10100110111"

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

FORMAT_INFO_STRINGS = {
    (ecc_level.L,mask_level.VER_0):'111011111000100',
    (ecc_level.L,mask_level.VER_1):'111001011110011',
    (ecc_level.L,mask_level.VER_2):'111110110101010',
    (ecc_level.L,mask_level.VER_3):'111100010011101',
    (ecc_level.L,mask_level.VER_4):'110011000101111',
    (ecc_level.L,mask_level.VER_5):'110001100011000',
    (ecc_level.L,mask_level.VER_6):'110110001000001',
    (ecc_level.L,mask_level.VER_7):'110100101110110',
    (ecc_level.M,mask_level.VER_0):'101010000010010',
    (ecc_level.M,mask_level.VER_1):'101000100100101',
    (ecc_level.M,mask_level.VER_2):'101111001111100',
    (ecc_level.M,mask_level.VER_3):'101101101001011',
    (ecc_level.M,mask_level.VER_4):'100010111111001',
    (ecc_level.M,mask_level.VER_5):'100000011001110',
    (ecc_level.M,mask_level.VER_6):'100111110010111',
    (ecc_level.M,mask_level.VER_7):'100101010100000',
    (ecc_level.Q,mask_level.VER_0):'011010101011111',
    (ecc_level.Q,mask_level.VER_1):'011000001101000',
    (ecc_level.Q,mask_level.VER_2):'011111100110001',
    (ecc_level.Q,mask_level.VER_3):'011101000000110',
    (ecc_level.Q,mask_level.VER_4):'010010010110100',
    (ecc_level.Q,mask_level.VER_5):'010000110000011',
    (ecc_level.Q,mask_level.VER_6):'010111011011010',
    (ecc_level.Q,mask_level.VER_7):'010101111101101',
    (ecc_level.H,mask_level.VER_0):'001011010001001',
    (ecc_level.H,mask_level.VER_1):'001001110111110',
    (ecc_level.H,mask_level.VER_2):'001110011100111',
    (ecc_level.H,mask_level.VER_3):'001100111010000',
    (ecc_level.H,mask_level.VER_4):'000011101100010',
    (ecc_level.H,mask_level.VER_5):'000001001010101',
    (ecc_level.H,mask_level.VER_6):'000110100001100',
    (ecc_level.H,mask_level.VER_7):'000100000111011',
}

test_5q = "0100001101010101010001101000011001010111001001100101010111000010011101110011001000000110000100100000011001100111001001101111011011110110010000100000011101110110100001101111001000000111001001100101011000010110110001101100011110010010000001101011011011100110111101110111011100110010000001110111011010000110010101110010011001010010000001101000011010010111001100100000011101000110111101110111011001010110110000100000011010010111001100101110000011101100000100011110110000010001111011000001000111101100"

# main sequence for HELLO WORLD, ver 1, ecc Q  CORRECT
# 00100000010110110000101101111000110100010111001011011100010011010100001101000000111011000001000111101100

# What ecc is supposed to be
# 10101000010010000001011001010010110110010011011010011100000000000010111000001111101101000111101000010000
# 10101000010010000001011001010010110110010011011010011100000000000010111000001111101101000111101000010000