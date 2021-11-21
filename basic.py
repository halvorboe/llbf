import sys
from typing import List
from collections import defaultdict



INSTRUCTIONS = set("<>+-.,[]")


def eval_bf(program: str, input_buffer: List[int] = list(), debug: bool = False) -> List[int]:
    program = [c for c in program if c in INSTRUCTIONS]

    registers = defaultdict(lambda: 0)
    stack = []  # stores the current call stack.
    ip = 0  # points to the current instruction.
    mp = 0  # points to the current memory location.

    # io
    ibp = 0  # points to the current position in the input buffer.
    output_buffer = []

    while ip < len(program):
        instruction = program[ip]

        # forwards
        if instruction == ">":
            mp += 1
        # backwards
        elif instruction == "<":
            mp -= 1
        # add
        elif instruction == "+":
            registers[mp] += 1
        # subtract
        elif instruction == "-":
            registers[mp] -= 1
        # output
        elif instruction == ".":
            output_buffer.append(registers[mp])
        # input
        elif instruction == ",":
            if ibp > len(input_buffer):
                raise ValueError("outside input buffer. invalid program")
            registers[mp] = input_buffer[ibp]
            ibp += 1
        # jump begin 
        elif instruction == "[":
            if registers[mp]:
                # no jump 
                stack.append(ip)
            else:
                # jump
                current_level = 1
                while current_level > 0:
                    ip += 1
                    if ip > len(program):
                        raise ValueError("no matching ] bracket. invalid program")
                    if program[ip] == "[":
                        current_level += 1
                    elif program[ip] == "]":
                        current_level -= 1
        # jump end
        elif instruction == "]":
            previous = stack.pop()
            if registers[mp]:
                ip = previous - 1
        else:
            raise ValueError(f"{instruction} is not a valid BF instruction. invalid program")

        ip += 1

        if debug:
            print(instruction, ip, mp, list(registers.values()))

    return output_buffer


if __name__ == "__main__":
    if not sys.argv or len(sys.argv) < 2:
        raise ValueError("invalid args")
    code = open(sys.argv[1]).read()
    input_buffer = [int(c) for c in sys.argv[2:]]

    print("eval: ", code)
    print("result: ", "".join(chr(r) for r in eval_bf(code, input_buffer)))
    


