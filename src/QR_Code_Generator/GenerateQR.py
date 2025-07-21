import numpy as np
# import sys
# sys.path.append("/C:/Users/squiz/QR-Code-Generator/src/Data")
from Data import constants as const
import yaml

try:
    with open('./src/Data/VersionCapacity.yaml', 'r') as file:
        version_capacity_file = yaml.safe_load(file)
        print(version_capacity_file)
except FileNotFoundError:
    print("ERROR: VersionCapacity.yaml file not found")
except yaml.YAMLError as e:
    print(f"Error parsing YAML: {e}")

class QR_Code:
    def __init__(self, ecc: const.ecc_level, data_mode: const.data_mode, data):
        self.ecc = ecc
        self.data_mode = data_mode
        self.data = data
        self.ver = self.find_version()
        self.size = const.QR_VERSION_SIZES[self.ver]
        self.qr_code = np.full((self.size,self.size), False)

    def instantiate_template(self):
        corners = [[0,0],[0,self.size-7],[self.size-7,0]]
        for c in corners:
            for x in range(len(const.QR_CORNER)):
                for y in range(len(const.QR_CORNER[x])):
                    self.qr_code[c[0]+x][c[1]+y] = const.QR_CORNER[x][y]
        
    def print_qr(self):
        for i in self.qr_code:
            print(list(map(int, i)))

    def find_version(self):
        if self.data_mode == const.data_mode.NUMERIC:
            byte_len = len(str(self.data))
        else:
            byte_len = len(self.data)

        for v in version_capacity_file:
            if byte_len < version_capacity_file[v][self.ecc.value][self.data_mode.value]:
                return v