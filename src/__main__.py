from QR_Code_Generator import GenerateQR as qr
from QR_Code_Generator import Encoder as enc
from Data import constants as const

if __name__ == "__main__":
    qr_code = qr.QR_Code(const.ecc_level.H, const.data_mode.ALPHANUMERIC,"hello worlds")
    qr_code.instantiate_template()
    # qr_code.print_qr()
    # qr = enc.Encoder(const.ecc_level.H, 1, const.data_mode.ALPHANUMERIC,"hello worlds")
    # qr.alphanumeric()
    