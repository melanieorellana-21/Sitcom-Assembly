memoryAddress = 5000
tRegister = 0
vars = {}


def getRegisterName(index):
    sitcom_registers = ["$phil", "$claire", "$haley", "$alex", "$luke", "$mitchel", "$cam", "$manny", "$jay", "$gloria"]
    return sitcom_registers[index % len(sitcom_registers)]


def allocate_variable(varName):
    global memoryAddress, tRegister
    reg = getRegisterName(tRegister)
    vars[varName] = (reg, memoryAddress)
    instr = f"hudoin {reg}, {memoryAddress}  # int {varName};"
    memoryAddress += 4
    tRegister += 1
    return instr


def assign_immediate(varName, value):
    reg, addr = vars[varName]
    result = f"hudoin {reg}, {value}  # {varName} = {value};"
    return result


def assign_variable(dest, src):
    reg_dest, addr_dest = vars[dest]
    reg_src, addr_src = vars[src]
    return f"nnine {reg_dest}, {reg_src}  # {dest} = {src};"


def generate_condition(var1, var2, label):
    reg1, _ = vars[var1]
    reg2, _ = vars[var2]
    return f"noc {reg1}, {reg2}, {label}  # if ({var1} == {var2})"


def compile_c_to_sitcom(input_path, output_path):
    with open(input_path, "r") as f:
        lines = f.readlines()


    output = []
    label_counter = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith("//"):
            continue


        if line.startswith("int "):
            _, var = line.split()
            var = var.strip(";")
            output.append(allocate_variable(var))


        elif "=" in line:
            var, value = map(str.strip, line.strip(";").split("="))
            if value.isdigit():
                output.append(assign_immediate(var, value))
            else:
                output.append(assign_variable(var, value))


        elif line.startswith("if"):
            condition = line[line.find("(")+1:line.find(")")]
            var1, var2 = map(str.strip, condition.split("=="))
            label = f"LABEL_{label_counter}"
            label_counter += 1
            output.append(generate_condition(var1, var2, label))
            output.append(f"# -- start if body --")
        elif line.startswith("}"):
            output.append(f"# -- end if body --")
        else:
            output.append(f"# Unrecognized line: {line}")


    with open(output_path, "w") as out:
        out.write("\n".join(output))


# Example usage:
compile_c_to_sitcom("program7.c", "sitcom_output.asm")
