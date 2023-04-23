import textwrap
import encryption_utils

def bbs_generator(gen_parameters = None, iter_num = None, bin_output = False, get_instructions = False):
    """Blum Blum Shub Generator"""
    if get_instructions == True:
        instructions = textwrap.dedent("""\
        You need to enter the parameters required for this generator.
        Each parameter must be entered on a new line, the name of the parameter and its value must be separated by an equal sign.
        This generator accepts the following parameters: x, p, q.
        x - seed (start value), p and q are two prime numbers forming the module m = p * q.
        The values of x and n must be coprime prime, i.e GCD(x, m) = 1.
        Example:
        x = 7
        p = 11
        q = 13
        Note: Binary output represents a sequence of parity bits of each iteration (even type of parity).
        Decimal output represents a sequence of decimal numbers generated at each iteration.
        """)
        return instructions
    # Conversion of the input parameters of the generator into a dictionary and checking the correctness 
    try:
        gen_parameters = gen_parameters.split("\n")
        gen_parameters = [parameter.split("=") for parameter in gen_parameters]
        gen_parameters = {parameter[0]:int(parameter[1]) for parameter in gen_parameters}
    except:
        return "Error: you entered the wrong parameters"
    if ("p" not in gen_parameters) or ("q" not in gen_parameters) or ("x" not in gen_parameters):
        return "Error: the required parameters for this generator are missing"
    x = gen_parameters["x"]
    p = gen_parameters["p"]
    q = gen_parameters["q"]
    m = p * q
    del gen_parameters
    if encryption_utils.gcd(m, x) != 1:
        return "Error: GCD of the x and the product of the numbers p and q must be equal to 1"
    # Checking whether the value of the specified number of iterations is an integer
    try:
        iter_num = int(iter_num)
    except:
        return "The value of the specified number of iterations must be an integer"
    # Implementation of Blum Blum Shub Generator
    gen_res = []
    gen_res.append((x**2) % m)
    for i in range(iter_num - 1):
        gen_res.append((gen_res[i] ** 2) % m)
    # Return in binary or decimal form depending on the input argument
    if bin_output == False:
        return " ".join(str(n) for n in gen_res)
    elif bin_output == True:
        return "".join(str(encryption_utils.get_even_parity_bit(n)) for n in gen_res)

def lcg_generator(gen_parameters = None, iter_num = None, bin_output = False, get_instructions = False):
    """Linear congruential generator"""
    if get_instructions == True:
        instructions = textwrap.dedent("""\
        You need to enter the parameters required for this generator.
        Each parameter must be entered on a new line, the name of the parameter and its value must be separated by an equal sign.
        This generator accepts the following parameters: p, q, x, a, c.
        p and q are two prime numbers forming the module m = p * q.
        x - seed (start value), 0 ≤ x < m
        m - modulus, 0 < m
        a - multiplier, 0 < a < m
        c - increment, 0 ≤ c < m
        Example:
        x = 73
        p = 3
        q = 41
        a = 5
        c = 2
        Note: Binary output represents a sequence of bits generated at each iteration that are concatenated without spaces.
        Decimal output represents a sequence of decimal numbers generated at each iteration that are separated by spaces.
        """)
        return instructions
    # Conversion of the input parameters of the generator into a dictionary and checking the correctness 
    try:
        gen_parameters = gen_parameters.split("\n")
        gen_parameters = [parameter.split("=") for parameter in gen_parameters]
        gen_parameters = {parameter[0]:int(parameter[1]) for parameter in gen_parameters}
        iter_num = int(iter_num)
    except:
        return "Error: you entered the wrong parameters"
    required_parameters = ["x", "p", "q", "a", "c"]
    for i in required_parameters:
        if i not in gen_parameters:
            return "Error: the required parameters for this generator are missing"
    # Converting dictionary elements into regular variables
    x = gen_parameters["x"]
    p = gen_parameters["p"]
    q = gen_parameters["q"]
    a = gen_parameters["a"]
    c = gen_parameters["c"]
    del gen_parameters
    m = p * q
    # Implementation of Linear congruential generator
    gen_res = []
    gen_res.append((a * x + c) % m)
    for i in range(iter_num - 1):
        gen_res.append((a * gen_res[i] + c) % m)
    if bin_output == False:
        return " ".join(str(n) for n in gen_res)
    elif bin_output == True:
        return "".join(f"{n:0b}" for n in gen_res)
