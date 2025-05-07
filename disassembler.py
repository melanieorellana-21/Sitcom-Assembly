
import sys


#R-type and J-type
op_codes = {
    "000000": "urmyRock",    #add
    "000000": "hey.HEY",    # sub
    "000000": "THAT'Sit",    # div
    "000000": "NOTajoke",    # mfhi
    "001000": "hudoin",    # li
    "000100": "noc",    # beq
    "000000": "nnine",    # move(addu)
    "000011": "smort",    # jal
    "001000": "ciBEmore",    #addi
    "000010": "pivot",    # j
    "001100": "O.M.G",    #syscall
    "000000": "clownsrppl",    # bgt
    "000100": "BBBg",    #beqz
    "000101": "CUTitOUT",    # bne
    "000000": "UgotITdude",    #la
}
#I-types
func_codes = {
    "100001": "urmyRock",    # add
    "100010": "hey.HEY",    # sub
    "011010": "THAT'Sit",    # div
    "010000": "NOTajoke",    # mfhi
    "101010": "clownsrppl",    # bgt
    "100001": "nnine",    # move
}
registers = {
    "00000": "$jake",
    "00001": "$ross",
    "00010": "$michael",
    "00011": "$dwight",
    "00100": "$jess",
    "00101": "$winston",
    "00110": "$nick",
    "00111": "$schmidt",
    "01000": "$phil",
    "01001": "$claire",
    "01010": "$haley",
    "01011": "$alex",
    "01100": "$luke",
    "01101": "$mitchel",
    "01110": "$cam",
    "01111": "$manny",
    "10000": "$barney",
    "10001": "$robin",
    "10010": "$ted",
    "10011": "$marshall",
    "10100": "$lilyEriksen",
    "10101": "$tracy",
    "10110": "$ranjit",
    "10111": "$carl",
    "11000": "$jay",
    "11001": "$gloria",
    "11010": "$michelle",
    "11011": "$dj",
    "11100": "$stephanie",
    "11101": "$jessie",
    "11110": "$danny",
    "11111": "$joey"
}


def handle_lines(bin_file: str):
    with open(bin_file, "r") as input_file:
        line = input_file.readlines()[0].strip()
        sitcom_instructions = bin_to_sitcom(line)
        with open("BACK_TO_SITCOM.txt", "w") as output_file:
            for instruction in sitcom_instructions:
                output_file.write(instruction)
                output_file.write("\n")
def bin_to_sitcom(line):
    sitcom = []
    bit_string = ""
    for bit in line:
        bit_string += bit
        if len(bit_string) == 32:
            op_code = bit_string[0:6]
            if op_code == "000000": # R-type
                rs, rt, rd, shamt, func_code = (
                    bit_string[6:11],
                    bit_string[11:16],
                    bit_string[16:21],
                    bit_string[21:26],
                    bit_string[26:32]
                )
                instr = func_codes.get(func_code, "unknown")
                sitcom.append(f"{instr} {registers[rd]}, {registers[rs]}, {registers[rt]}")
            elif op_code in op_codes: # I-type or J-type
                if op_code in ["000010", "000011"]: # J-type
                    address = int(bit_string[6:32], 2)
                    instr = op_codes[op_code]
                    sitcom.append(f"{instr} LABEL_{address}")
                else: # I-type
                    rs = bit_string[6:11]
                    rt = bit_string[11:16]
                    imm = int(bit_string[16:32], 2)
                    instr = op_codes[op_code]
                    sitcom.append(f"{instr} {registers[rt]}, {registers[rs]}, {imm}")
            else:
                sitcom.append("unknown_instruction")
            bit_string = ""
    return sitcom


if __name__ == "__main__":
 handle_lines(sys.argv[1])
