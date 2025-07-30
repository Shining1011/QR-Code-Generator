from QR_Code_Generator import GenerateQR as qr
from Data import constants as const
from Data import generator_polynomials as gen_poly
import toml
from sys import exit as exit_program
import numpy as np

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
    
    qr_code = qr.QR_Code(const.ecc_level.M, const.data_mode.ALPHANUMERIC,"HELLO WORLD HELLO WORLD")
    qr_code.create_finder_pattern()
    qr_code.create_seperator()
    qr_code.create_timing_pattern()
    qr_code.create_alignment_pattern()
    qr_code.create_dark_module()
    qr_code.reserve_formatting_location()
    qr_code.place_data()
    qr_code.print_qr()

    # encoder_check = qr.Encoder(ecc=const.ecc_level.M, ver=1, data_mode=const.data_mode.ALPHANUMERIC, data="HELLO WORLD")
    # encoder_check.fill_groups()
    # encoder_check.create_ecc()

    