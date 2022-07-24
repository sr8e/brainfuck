import re
import sys
import time


# Define Interpreter Error
class BFError(Exception):
    def __init__(self, code, pos):
        self.code = code
        self.pos = pos

    def print_position(self):
        code = self.code[max(self.pos - 5, 0) : self.pos + 6]
        return (
            f"  At code position {self.pos}\n"
            f"    {code}\n"
            f"    {' ' * (5 if self.pos > 5 else self.pos)}^"
        )

    def __str__(self):
        return (
            f"{self.print_position()}\n"
            f"{self.__class__.__name__}: {self.class_message}"
        )


class PointerUnderFlowError(BFError):
    class_message = "Data pointer underflow"


class PointerOverFlowError(BFError):
    class_message = "Data pointer overflow"


class InvalidTokenError(BFError):
    def __init__(self, code, pos, message):
        super().__init__(code, pos)
        self.class_message = f"Invalid Token ({message}) found"


# Remove unused characters
# if debugging is enabled, "!" will remain
def purify(code, debug):
    pat = r"[^][><,.!+-]" if debug else r"[^][><,.+-]"
    return re.sub(pat, "", code)


def debug_info(code_ptr, mem_ptr, mem_val):
    return f"Debug: code pointer at {code_ptr}, memory address {mem_ptr}, memory value 0x{mem_val:02x} ({mem_val})"


# Execute code
def exec_bf(code, memsize, stdin):
    code_length = len(code)
    mem_ptr = 0
    code_ptr = 0
    memory = [0 for i in range(memsize)]
    in_stream = list(stdin.encode())
    input_left = len(in_stream)
    out_stream = []

    stime = time.perf_counter()
    steps = 0

    try:
        while code_ptr < code_length:
            token = code[code_ptr]

            if token == ">":
                mem_ptr += 1
                if mem_ptr >= memsize:
                    raise PointerOverFlowError(code, code_ptr)

            elif token == "<":
                mem_ptr -= 1
                if mem_ptr < 0:
                    raise PointerUnderFlowError(code, code_ptr)

            elif token == "+":
                memory[mem_ptr] += 1
                memory[mem_ptr] %= 0x100

            elif token == "-":
                memory[mem_ptr] -= 1
                memory[mem_ptr] %= 0x100

            elif token == ".":
                out_stream.append(memory[mem_ptr])

            elif token == ",":
                if input_left > 0:
                    memory[mem_ptr] = in_stream.pop(0)
                    input_left -= 1

            elif token == "[":
                if memory[mem_ptr] == 0:  # skip
                    ptr_open = code_ptr
                    depth = 0
                    # find corresponding close bracket
                    while True:
                        code_ptr += 1
                        if code_ptr >= code_length:
                            raise InvalidTokenError(
                                code, ptr_open, "missing closing bracket"
                            )

                        if (new_token := code[code_ptr]) == "[":
                            depth += 1
                        elif new_token == "]":
                            if depth == 0:
                                break
                            depth -= 1

            elif token == "]":
                if memory[mem_ptr] != 0:  # return to open bracket
                    ptr_close = code_ptr
                    depth = 0
                    # find corresponding open bracket
                    while True:
                        code_ptr -= 1
                        if code_ptr < 0:
                            raise InvalidTokenError(
                                code, ptr_close, "missing opening bracket"
                            )

                        if (new_token := code[code_ptr]) == "[":
                            if depth == 0:
                                break
                            depth -= 1
                        elif new_token == "]":
                            depth += 1

            elif token == "!":
                print(debug_info(code_ptr, mem_ptr, memory[mem_ptr]))

            code_ptr += 1
            steps += 1

        etime = time.perf_counter()
        elapsed = etime - stime
        stdout = bytes(out_stream).decode()

        print(stdout)
        print(
            f"Steps: {steps}, Elasped Time: {elapsed:.6f}s, {steps/elapsed:.2f} steps/sec"
        )

    except BFError as e:
        print(e)
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e.reason} '0x{e.object[e.start]:02x}'")
    except:
        print("Unknown Interpreter Error!")


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print("Usage: <filename> [options...]")
        exit()
    try:
        with open(sys.argv[1], "r") as f:
            src = f.read()
    except Exception as e:
        print(e)
        exit()

    debug = False
    memsize = 100
    stdin = ""

    for opt in sys.argv[2:]:
        if opt.startswith("-"):
            if (s := opt[1]) == "d":
                debug = True
            elif s == "m":
                try:
                    memsize = int(opt.split("=")[1])
                except ValueError:
                    print("-m: Invalid Value")
                    exit()
                except IndexError:
                    print("Usage: -m=<memory size>")
                    exit()
                if memsize < 1:
                    print("-m: Memory size must be positive")
                    exit()
            elif s == "i":
                try:
                    stdin = opt.split("=")[1]
                except IndexError:
                    print("Usage: -i=<input string>")
                    exit()
            else:
                print("Unknown Option. Available options are: -d, -i, -m")
                exit()
        else:
            print("Usage: <filename> [options...]")
            exit()

    code = purify(src, debug)
    exec_bf(code, memsize, stdin)
