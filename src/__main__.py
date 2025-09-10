from QR_Code_Generator import GenerateQR as qr
from QR_Code_Generator import GUI as gui
from Data import constants as const
from Data import generator_polynomials as gen_poly
import toml
from sys import exit as exit_program
import numpy as np
import turtle as trt

import pstats
import time
import cProfile


try:
    with open("config.toml", 'r') as file:
        config = toml.load(file)
except FileNotFoundError:
    print("ERROR: config.toml file not found in " + str(__file__))
    exit_program()
except Exception as e:
    print(f"An error occured: {e}")
    exit_program()

if __name__ == "__main__":
    if len(gen_poly.GENERATOR_POLYNOMIALS) != config['qr_code']['max_ecc_generator_poly']:
        poly_gen = qr.Generator_Polynomial(limit=config['qr_code']['max_ecc_generator_poly'])
        poly_gen.create_generator_polynomials()
        poly_gen.push_to_constants()
        del poly_gen

    # for i in range(256):
    #     print(const.alpha_to_coef(i))
    #     print(const.ALPHA_TO_COEF[i])

    app = gui.GUI(config['qr_code']['max_version_size'])

    # with cProfile.Profile() as profile:
    #     qr = qr.QR_Code(data="HELLO WORLD", ecc=const.ecc_level.H, force_mask=None, min_ver=5)
    # results = pstats.Stats(profile)
    # results.sort_stats(pstats.SortKey.TIME)
    # # results.print_stats()
    # results.dump_stats("results.prof")
