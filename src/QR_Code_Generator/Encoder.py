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

class Encoder:
    def __init__(self, ecc: const.ecc_level, ver: int, data_mode: const.data_mode, data):
        self.ecc = ecc
        self.ver = ver
        self.data_mode = data_mode
        self.character_count_indicator = self.get_char_count_ind()
        self.terminator = self.get_terminator()
        self.data = data
        self.padding = self.get_padding()

        match self.data_mode:
            case const.data_mode.NUMERIC:
                pass
            case const.data_mode.ALPHANUMERIC:
                self.data = self.get_alphanumeric()
            case const.data_mode.BYTE:
                pass
            case const.data_mode.KANJI:
                pass

        

    def get_alphanumeric(self):
        self.data = self.data.upper()
        binary_str = []
        for i in range(0, len(self.data), 2):
            if i+1 < len(self.data):
                result = 45 * const.ALPHANUMERIC_TO_INT[self.data[i]] + const.ALPHANUMERIC_TO_INT[self.data[i-1]]
                binary_str.append(format(result, '011b'))
            else:
                result = const.ALPHANUMERIC_TO_INT[self.data[i]]
                binary_str.append(format(result, '06b'))
        return binary_str
    
    def get_char_count_ind(self):
        match self.data_type:
            case const.data_mode.NUMERIC:
                self.character_count_indicator = len(str(self.data))
            case const.data_mode.ALPHANUMERIC:
                self.character_count_indicator = len(self.data)
            case const.data_mode.BYTE:
                self.character_count_indicator = len(self.data)
            case const.data_mode.KANJI:
                self.character_count_indicator = len(self.data)
        return format(self.character_count_indicator, '09b')

    def get_terminator(self):
        bits_total = version_capacity_file[self.ver][self.ecc]["data_codewords_total"] * 8
        bits_used = len(const.MODE_INDICATOR[self.data_mode]) + len(self.character_count_indicator)
        for b in self.data:
            bits_used += len(b)
        if bits_total - bits_used < 4:
            return format(0, '0' + (bits_total - bits_used) + 'b')
        else:
            return format(0, '04b')

    def get_padding(self):
        bits_used = len(const.MODE_INDICATOR[self.data_mode]) + len(self.character_count_indicator)
        for b in self.data:
            bits_used += len(b)
        if bits_used % 8 != 0:
            return format(0, '0' + bits_used % 8 + 'b')
        return b''

    def encode(self):
        