import sys
import os

#R-type and J-type
op_codes = {
    "urmyRock": "000000",    #add
    "hey.HEY": "000000",    #sub
    "THAT'Sit": "000000",   #div
    "NOTajoke": "000000",    #mfhi
    "hudoin": "001000",    #li
    "noc": "000100",     #beq
    "nnine": "000000",     #move(addu)
    "smort": "000011",    #jal
    "ciBEmore": "001000",    #addi
    "pivot": "000010",    #j
    "O.M.G": "001100",    #syscall
    "clownsrppl": "000000",    #bgt
    "BBBg": "000100",    #beqz
    "CUTitOUT": "000101",    #bne
    "UgotITdude": "001101",    #la
}
#I-type
func_codes = {
    "urmyRock": "100000",   #add
    "hey.HEY": "100010",    #sub
    "THAT'Sit": "011010",   #div
    "NOTajoke": "010000",    #mfhi
    "clownsrppl": "101010", #bgt
    "nnine": "100001",  #move
}
registers = {
    "$jake": "00000",
    "$ross": "00001",
    "$michael": "00010",
    "$dwight": "00011",
    "$jess": "00100",
    "$winston": "00101",
    "$nick": "00110",
    "$schmidt": "00111",
    "$phil": "01000",
    "$claire": "01001",
    "$haley": "01010",
    "$alex": "01011",
    "$luke": "01100",
    "$mitchel": "01101",
    "$cam": "01110",
    "$manny":"01111",
    "$barney": "10000",
    "$robin" : "10001",
    "$ted": "10010",
    "$marshall" : "10011",
    "$lilyEriksen":"10100",
    "$tracy":"10101",
    "$ranjit":"10110",
    "$carl":"10111",
    "$jay": "11000",
    "$gloria":"11001",
    "$michelle": "11010",
    "$dj": "11011",
    "$stephanie": "11100",
    "$jessie": "11101",
    "$danny": "11110",
    "$joey": "11111",
}
shift_logic_amount = "00000"


def interpret_line(mips_file: str):
    with open(mips_file, "r") as input_file, open("program1.bin", "w") as output_file:
        for instruction in input_file:
            bin_line = assemble(instruction)
            if bin_line:
                output_file.write(bin_line + "\n")
                print(f"{instruction.strip()} → {bin_line}")
            else:
                print(f"skipped: {instruction.strip()}")

print("The assembling has been completed!")

def assemble(line):
    line = line.split("#")[0].strip() #removes comments

    if not line:
        return

    parts = line.split(" ")
    op_code = parts[0]

    #for R-type instructions
    if op_code in func_codes:
        rd, rs, rt = (
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
            parts[3].replace(",", ""),
        )
        return (
            op_codes[op_code]
            + registers[rs]
            + registers[rt]
            + registers[rd]
            + shift_logic_amount
            + func_codes[op_code]
        )
    #I-type instrctions
    if op_code == "ciBEmore":
        rt, rs, imm = (
            parts[1],
            parts[2],
            parts[3],
        )
        imm_bin = bin(int(imm)).replace("0b", "").zfill(16)
        return op_codes[op_code]+registers[rs] + registers[rt] + imm_bin
    #J-Type instructions
    if op_code in["pivot", "smort"]:
        address = bin(int(parts[1])).replace("0b", "").zfill(26)
        return op_codes[op_code]+ address
    #conversion for li ("hudoin")
    if op_code == "hudoin":
        rt, imm = parts[1], parts[2]
        rs = "$jake" 
        imm_bin = bin(int(imm)).replace("0b", "").zfill(16)
        return op_codes[op_code] +registers[rs] + registers[rt] + imm_bin
    #conversion for beq, bne, and beqz
    if op_code in["noc", "CUTitOUT", "BBBg"]:
        rs, rt, offset = parts[1], parts[2], parts[3]
        offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
        return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin
    #conversion for syscall
    if op_code == "O.M.G":
        return op_codes[op_code] + "00000000000000000100"
    #conversion for la 
    if op_code == "UgotITdude":
        rt, addr = parts[1], parts[2]
        imm_bin = bin(int(addr)).replace("0b", "").zfill(16)
        rs = "$jake" #$zero register
        return op_codes[op_code] + registers[rs] + registers[rt] + imm_bin
    return ""
if __name__ == "__main__":
    # mips_file = sys.argv[1]
    mips_file = "program1.mips"
    interpret_line(mips_file)
