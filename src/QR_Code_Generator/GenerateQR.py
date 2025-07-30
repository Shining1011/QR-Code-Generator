from Data import constants as const
from Data import generator_polynomials
import numpy as np
import yaml
from sys import exit as exit_program

try:
    with open('./src/Data/VersionCapacity.yaml', 'r') as file:
        version_capacity_file = yaml.safe_load(file)
        # print(version_capacity_file)
except FileNotFoundError:
    print("ERROR: VersionCapacity.yaml file not found in " + str(__file__))
    exit_program()
except yaml.YAMLError as e:
    print(f"Error parsing YAML: {e} in " + str(__file__))
    exit_program()

class QR_Code:
    def __init__(self, ecc: const.ecc_level, data_mode: const.data_mode, data):
        self.ecc = ecc
        self.data_mode = data_mode
        self.data = data
        self.ver = self.find_version()
        self.size = const.QR_VERSION_SIZES[self.ver]
        self.encoder = Encoder(ecc=self.ecc, ver=self.ver, data_mode=self.data_mode, data=self.data)
        self.alignment_module_locations = version_capacity_file[self.ver]["template_information"]
        self.data_str = self.encoder.get_data_str()
        self.data_placed = 0
        # print(self.data_str)
        # print(len(self.data_str))

        # index 0 = y
        # index 1 = x
        self.qr_code = np.full((self.size,self.size), None)

        # index 0 = top left corner, 
        # index 1 = top right corner, 
        # index 2 = bottom left corner
        # index 3 = bottom right corner
        self.corners = np.array([np.array([0,0]),np.array([0,self.size-1]),np.array([self.size-1,0]),np.array([self.size-1,self.size-1])])
    
    def place_data(self):
        temp_corner = self.corners.copy()[3]
        is_upward = True
        # Before timing patterns
        for column in range(0, self.size-8, 2):
            for row in range(0, self.size, 4):
                if is_upward:
                    self.insert_data_upward(temp_corner-np.array([row, column]))
                else:
                    self.insert_data_downward(temp_corner-np.array([row, column]))
            is_upward = not is_upward
        # After timing pattern
        is_upward = not is_upward
        for column in range(self.size-8, self.size, 2):
            for row in range(0, self.size, 4):
                if is_upward:
                    self.insert_data_upward(temp_corner-np.array([row, column]))
                else:
                    self.insert_data_downward(temp_corner-np.array([row, column]))
            is_upward = not is_upward
                
    def insert_data_upward(self, start: np.array):
        for y in range(4):
            if self.qr_code[start[0]-y][start[1]] == None:
                self.qr_code[start[0]-y][start[1]] = self.data_str[self.data_placed]
                self.data_placed += 1
            if self.qr_code[start[0]-y][start[1]-1] == None:
                self.qr_code[start[0]-y][start[1]-1] = self.data_str[self.data_placed]
                self.data_placed += 1
    
    def insert_data_downward(self, start: np.array):
        for y in range(4, 0, -1):
            if self.qr_code[start[0]-y][start[1]] == None:
                self.qr_code[start[0]-y][start[1]] = self.data_str[self.data_placed]
                self.data_placed += 1
            if self.qr_code[start[0]-y][start[1]-1] == None:
                self.qr_code[start[0]-y][start[1]-1] = self.data_str[self.data_placed]
                self.data_placed += 1

    def print_qr(self):
        for i in range(len(self.qr_code)):
            for k in range(len(self.qr_code[i])):
                match self.qr_code[i][k]:
                    case True:
                        print("1", end=" ")
                    case False:
                        print("0", end=" ")
                    case None:
                        print("*", end=" ")
                    case _:
                        print(str(self.qr_code[i][k]), end=" ")
            print("")
        
    def find_version(self):
        if self.data_mode == const.data_mode.NUMERIC:
            byte_len = len(str(self.data))
        else:
            byte_len = len(self.data)

        for v in version_capacity_file:
            if byte_len < version_capacity_file[v][self.ecc.value["name"]]["data_mode"][self.data_mode.value["name"]]:
                return v
        print("Error value inputted is too large")
        exit_program()

    #region Create QR Code Template

    def create_finder_pattern(self):
        temp_corners = self.corners.copy()
        temp_corners[1] += np.array([0,-len(const.QR_FINDER_PATTERN)+1])
        temp_corners[2] += np.array([-len(const.QR_FINDER_PATTERN)+1,0])
        for c in range(len(temp_corners)):
            if c==3:
                return
            for y in range(len(const.QR_FINDER_PATTERN)):
                for x in range(len(const.QR_FINDER_PATTERN[y])):
                    self.qr_code[temp_corners[c][0]+y][temp_corners[c][1]+x] = const.QR_FINDER_PATTERN[y][x]
 
    def create_seperator(self):
        temp_corners = self.corners.copy()
        temp_corners[0] += np.array([len(const.QR_SEPERATOR)-1,len(const.QR_SEPERATOR)-1])
        temp_corners[1] += np.array([len(const.QR_SEPERATOR)-1,-len(const.QR_SEPERATOR)+1])
        temp_corners[2] += np.array([-len(const.QR_SEPERATOR)+1,len(const.QR_SEPERATOR)-1])
        for c in range(len(temp_corners)):
            for s in range(len(const.QR_SEPERATOR)):
                match c:
                    case 0:
                        self.qr_code[temp_corners[c][0]-s][temp_corners[c][1]] = const.QR_SEPERATOR[s]
                        self.qr_code[temp_corners[c][0]][temp_corners[c][1]-s] = const.QR_SEPERATOR[s]
                    case 1:
                        self.qr_code[temp_corners[c][0]-s][temp_corners[c][1]] = const.QR_SEPERATOR[s]
                        self.qr_code[temp_corners[c][0]][temp_corners[c][1]+s] = const.QR_SEPERATOR[s]
                    case 2:
                        self.qr_code[temp_corners[c][0]+s][temp_corners[c][1]] = const.QR_SEPERATOR[s]
                        self.qr_code[temp_corners[c][0]][temp_corners[c][1]-s] = const.QR_SEPERATOR[s]

    def create_timing_pattern(self):
        temp_corner = self.corners.copy()[0]
        temp_corner += np.array([len(const.QR_SEPERATOR)-2,len(const.QR_SEPERATOR)-2])
        for i in range(self.size-16):
            self.qr_code[temp_corner[0]+(i+2)][temp_corner[1]] = bool((i+1)%2)
            self.qr_code[temp_corner[0]][temp_corner[1]+(i+2)] = bool((i+1)%2)

    def create_alignment_pattern(self):
        offset = np.array([-2,-2])
        for ly in self.alignment_module_locations:
            for lx in self.alignment_module_locations:
                if self.qr_code[ly][lx] == None:
                    aln_pat_corner = [ly+offset[0], lx+offset[1]]
                    for ay in range(len(const.QR_ALIGNMENT_PATTERN)):
                        for ax in range(len(const.QR_ALIGNMENT_PATTERN[ay])):
                            self.qr_code[aln_pat_corner[0]+ay][aln_pat_corner[1]+ax] = const.QR_ALIGNMENT_PATTERN[ay][ax]

    def create_dark_module(self):
        offset = np.array([len(const.QR_FINDER_PATTERN)+1,-len(const.QR_FINDER_PATTERN)])
        self.qr_code[self.corners[1][1]+offset[1]][self.corners[1][0]+offset[0]] = True

    def reserve_formatting_location(self):
        temp_corners = self.corners.copy()
        temp_corners[0] += np.array([8,8])
        temp_corners[1] += np.array([8,-7])
        temp_corners[2] += np.array([-6,8])
        for c in range(len(temp_corners)):
            if self.ver < 7:
                match c:
                    case 0:
                        for i in range(9):
                            if self.qr_code[temp_corners[c][0]-i][temp_corners[c][1]] == None:
                                self.qr_code[temp_corners[c][0]-i][temp_corners[c][1]] = "f"
                        for k in range(9):
                            if self.qr_code[temp_corners[c][0]][temp_corners[c][1]-k] == None:
                                self.qr_code[temp_corners[c][0]][temp_corners[c][1]-k] = "f"
                    case 1:
                        for i in range(8):
                            if self.qr_code[temp_corners[c][0]][temp_corners[c][1]+i] == None:
                                self.qr_code[temp_corners[c][0]][temp_corners[c][1]+i] = "f"
                    case 2:
                        for i in range(7):
                            if self.qr_code[temp_corners[c][0]+i][temp_corners[c][1]] == None:
                                self.qr_code[temp_corners[c][0]+i][temp_corners[c][1]] = "f"
            else:
                print("need to create function for format reservation ver 7 and higher")

    #endregion

class Encoder:
    def __init__(self, ecc: const.ecc_level, ver: int, data_mode: const.data_mode, data):
        self.ecc = ecc
        self.ver = ver
        self.data_mode = data_mode
        self.data = data
        self.required_remainder_bits = version_capacity_file[self.ver]["required_reminder_bits"]
        self.ecc_per_block = version_capacity_file[self.ver][self.ecc.value["name"]]["error_correction_block_information"]["ec_codeword_per_block"]
        self.bits_total = version_capacity_file[self.ver][self.ecc.value["name"]]["error_correction_block_information"]["data_codewords_total"] * 8
        self.block_num_g1 = version_capacity_file[self.ver][self.ecc.value["name"]]["error_correction_block_information"]["group_1"]["block_num"]
        self.block_num_g2 = version_capacity_file[self.ver][self.ecc.value["name"]]["error_correction_block_information"]["group_2"]["block_num"]
        self.data_codeword_num_g1 = version_capacity_file[self.ver][self.ecc.value["name"]]["error_correction_block_information"]["group_1"]["data_codeword_num"]
        self.data_codeword_num_g2 = version_capacity_file[self.ver][self.ecc.value["name"]]["error_correction_block_information"]["group_2"]["data_codeword_num"]
        self.group_1 = np.empty((self.block_num_g1, self.data_codeword_num_g1), dtype="S8")
        self.group_2 = np.empty((self.block_num_g2, self.data_codeword_num_g2), dtype="S8")

        match self.data_mode:
            case const.data_mode.NUMERIC:
                pass
            case const.data_mode.ALPHANUMERIC:
                self.data = self.get_alphanumeric()
            case const.data_mode.BYTE:
                pass
            case const.data_mode.KANJI:
                pass

        self.character_count_indicator = self.get_char_count_ind(data_original=data)
        self.terminator = self.get_terminator()
        self.padding = self.get_padding()
        self.gen_poly = Polynomial(generator_polynomials.GENERATOR_POLYNOMIALS[self.ecc_per_block-1])
        self.error_correction_codewords = []
        self.fill_groups()
        self.create_ecc(group=self.group_1)
        self.create_ecc(group=self.group_2)

    def get_alphanumeric(self):
        self.data = self.data.upper()
        binary_str = []
        for i in range(0, len(self.data), 2):
            if i+1 < len(self.data):
                result = 45 * const.ALPHANUMERIC_TO_INT[self.data[i]] + const.ALPHANUMERIC_TO_INT[self.data[i+1]]
                binary_str.append(format(result, '011b'))
            else:
                result = const.ALPHANUMERIC_TO_INT[self.data[i]]
                binary_str.append(format(result, '06b'))
        return binary_str
    
    def get_char_count_ind(self, data_original):
        match self.data_mode:
            case const.data_mode.NUMERIC:
                cci = len(str(data_original))
            case const.data_mode.ALPHANUMERIC:
                cci = len(data_original)
            case const.data_mode.BYTE:
                cci = len(data_original)
            case const.data_mode.KANJI:
                cci = len(data_original)
        return format(cci, '09b')

    def get_terminator(self):
        bits_used = len(self.data_mode.value["indicator"]) + len(self.character_count_indicator)
        for b in self.data:
            bits_used += len(b)
        if self.bits_total - bits_used < 4:
            return format(0, '0' + (self.bits_total - bits_used) + 'b')
        else:
            return format(0, '04b')

    def get_padding(self):
        padding = ""
        bits_used = len(self.data_mode.value["indicator"]) + len(self.character_count_indicator)
        for b in self.data:
            bits_used += len(b)
        bits_used += len(self.terminator)
        if bits_used % 8 != 0:
            padding = format(0, '0' + str(8 - bits_used % 8) + 'b')
        count = 0
        
        while bits_used + len(padding) < self.bits_total:
            count %= 2
            padding += const.PADDING_BYTES[count]
            count += 1
        return padding

    def fill_groups(self):
        data_str = self.data_mode.value["indicator"] + self.character_count_indicator
        for str in self.data:
            data_str += str
        data_str += self.terminator + self.padding
        count = 0
        for block in range(len(self.group_1)):
            for codeword in range(len(self.group_1[block])):
                self.group_1[block][codeword] = data_str[count*8:(count+1)*8]
                count += 1
        count = 0
        for block in range(len(self.group_2)):
            for codeword in range(len(self.group_2[block])):
                self.group_2[block][codeword] = data_str[count*8:(count+1)*8]
                count += 1

    def create_ecc(self, group: np.array):
        for block in range(len(group)):
            ecc = []
            message_poly = []
            for codeword in group[block]:
                message_poly.append(const.coef_to_alpha(int(codeword,2)))
            for i in range(self.ecc_per_block):
                message_poly.append(np.nan)
            message_poly.reverse()
            message_poly = Polynomial(np.array(message_poly))
            for i in range(self.ecc_per_block):
                lead_term = np.nan
                lead_term_index = np.nan
                for k in range(len(message_poly.polynomial)):
                    if not np.isnan(message_poly.polynomial[-k]):
                        lead_term = int(message_poly.polynomial[-k])
                        lead_term_index = k
                        break
                temp_lead_poly = np.full(len(message_poly.polynomial) - len(self.gen_poly.polynomial) - lead_term_index +2, np.nan)
                for k in range(lead_term_index):
                    np.append(temp_lead_poly, [np.nan])
                temp_lead_poly[-1] = lead_term
                temp_gen_poly = Polynomial(self.gen_poly.polynomial)
                temp_gen_poly.poly_multiply(temp_lead_poly)
                message_poly.poly_xor(temp_gen_poly.polynomial)
            for p in message_poly.polynomial:
                if np.isnan(p):
                    ecc.append(format(0, "08b"))
                else:
                    p = format(int(const.alpha_to_coef(p)), "08b")
                    ecc.append(p)
            self.error_correction_codewords.append(ecc)

    def get_data_str(self):
        data_str_bin = ""
        block_total = self.block_num_g1 + self.block_num_g2
        group_3 = [self.group_1, self.group_2]
        if  self.data_codeword_num_g1 > self.data_codeword_num_g2:
            max_data_per_block = self.data_codeword_num_g1
        else:
            max_data_per_block = self.data_codeword_num_g2
        for d in range(max_data_per_block):
            for b in range(block_total):
                for g in range(len(group_3)):
                    try:
                        # Fix in future
                        data_str_bin += str(group_3[g][b][d]).replace("b","").replace("'", "")
                    except IndexError:
                        pass
        for ecc in range(self.ecc_per_block):
            for b in range(block_total):
                data_str_bin += self.error_correction_codewords[b][ecc]
        if self.required_remainder_bits > 0:
            data_str_bin += format(0, "0" + str(self.required_remainder_bits) + "b")
        return data_str_bin

class Generator_Polynomial:

    def __init__(self,  limit: int):
        self.limit = limit
        self.error_correction_codewords = 1
        self.generator_polynomial = Polynomial(np.array([0,0])) 
        self.generator_list = [tuple(self.generator_polynomial.polynomial.tolist())]
        
    def create_generator_polynomials(self):
        if self.error_correction_codewords < self.limit:
            self.generator_polynomial.poly_multiply(np.array([self.error_correction_codewords,0]))
            self.generator_list.append(tuple(self.generator_polynomial.polynomial.tolist()))
            self.error_correction_codewords += 1 
            self.create_generator_polynomials()
    
    def push_to_constants(self):
        try:
            with open('./src/Data/generator_polynomials.py', 'r') as file:
                gen_poly_lines = file.readlines()
        except FileNotFoundError:
            print("ERROR: generator_polynomials.py file not found in " + str(__file__))
            exit_program()

        for i, line in enumerate(gen_poly_lines):
            if "GENERATOR_POLYNOMIALS =" in line:
                gen_poly_lines[i] = "GENERATOR_POLYNOMIALS = " + str(tuple(self.generator_list)) + "\n"

        with open('./src/Data/generator_polynomials.py', 'w') as file:
                file.writelines(gen_poly_lines)       

class Polynomial:
    def __init__(self, polynomial: np.array):
        # index rep power of x
        # value rep power of coef
        # value np.nan represents a coef of 0 
        self.polynomial = polynomial

    def poly_multiply(self, polynomial_factor: np.array):
        poly_result = np.full(len(self.polynomial)+len(polynomial_factor)-1, np.nan)
        for degree_1 in range(len(self.polynomial)):
            for degree_2 in range(len(polynomial_factor)):
                index = degree_1 + degree_2
                if not np.isnan(self.polynomial[degree_1]) and not np.isnan(polynomial_factor[degree_2]):
                    power = self.polynomial[degree_1] + polynomial_factor[degree_2]
                    if not np.isnan(poly_result[index]):
                        gf_result = const.alpha_to_coef(exp=int(poly_result[index])) ^ const.alpha_to_coef(exp=int(power))
                        if gf_result == 0:
                            poly_result[index] = np.nan
                        else:
                            gf_result = int(gf_result)
                            poly_result[index] = const.coef_to_alpha(gf_result)%const.GALOIS_FIELD_MODULO
                    else:
                        
                        poly_result[index] = power%const.GALOIS_FIELD_MODULO
        self.polynomial = poly_result

    def poly_xor(self, polynomial_factor: np.array):
        if len(self.polynomial) != len(polynomial_factor):
            print("Cannot XOR polynomials: \n" + str(self.polynomial) + "\nand\n" + str(polynomial_factor))
            exit_program()
        result_poly = np.full(len(self.polynomial),0,dtype=float)
        for degree in range(len(self.polynomial)):
            if not np.isnan(self.polynomial[degree]) and not np.isnan(polynomial_factor[degree]):
                result_coef = const.alpha_to_coef(self.polynomial[degree]) ^ const.alpha_to_coef(polynomial_factor[degree])
                if result_coef != 0:
                    result_poly[degree] = const.coef_to_alpha(result_coef)%256
                else:
                    result_poly[degree] = np.nan
            else:
                result_alpha = polynomial_factor[degree]
                if np.isnan(result_alpha):
                    result_alpha = self.polynomial[degree]
                result_poly[degree] = result_alpha
        power = 0
        for i in range(len(result_poly)):
            if not np.isnan(result_poly[-(i+1)]):
                power = i
                break
        if power != 0:
            result_poly = result_poly[:-power]
        self.polynomial = result_poly

