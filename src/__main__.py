from QR_Code_Generator import GenerateQR as qr
from QR_Code_Generator import GUI as gui
from Data import constants as const
from Data import generator_polynomials as gen_poly
import toml
from sys import exit as exit_program
import numpy as np
import turtle as trt


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

    app = gui.GUI(config['qr_code']['max_version_size'])

    # qr_code = qr.QR_Code(ecc=const.ecc_level.L, data_mode=const.data_mode.ALPHANUMERIC, data="HELLO WORLDHELLO WORLDHELLO WORLDHELLO WORLDHELLO WORLDHELLO WORLDHELLO WORLDHELLO WORLDHELLO WORLD")
    # qr_code.get_image(file_type=".png", pixel_size=2560)
    # print(qr_code.ver)
    # print(qr_code.mask.name)
    # qr_code.print_qr(qr_code.qr_code)

    # gui = gui.turtle_qr(10)
    # gui.draw_qr(qr=qr_code.qr_code)
    # while True:
    #     trt.done()
