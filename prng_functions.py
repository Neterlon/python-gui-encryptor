import textwrap
import encryption_utils

def bbs_generator(gen_parameters, iter_num, bin_output = False):
    """Blum Blum Shub Generator"""
    instructions = textwrap.dedent("""
    You need to enter the parameters required for this generator.
    Each parameter must be entered on a new line, the name of the parameter and its value must be separated by an equal sign.
    This generator accepts the following parameters: x, p, q.
    x - seed, p and q are two prime numbers forming the module m = p * q.
    The values of x and n must be coprime prime, i.e GCD(x, m) = 1.
    Example:
    x = 7
    p = 11
    q = 13
    Note: Binary output represents a sequence of parity bits of each iteration (even type of parity).
          Decimal output represents a sequence of decimal numbers generated at each iteration.
    """)
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
    if encryption_utils.gcd(m, x) != 1:
        return "Error: GCD of the x and the product of the numbers p and q must be equal to 1"
    # Checking whether the value of the specified number of iterations is an integer
    try:
        iter_num = int(iter_num)
    except:
        return "The value of the specified number of iterations must be an integer"
    # Implementation of Blum Blum Shub Generator
    bbs_gen_res = []
    bbs_gen_res.append((x**2) % m)
    for i in range(iter_num - 1):
        bbs_gen_res.append((bbs_gen_res[i] ** 2) % m)
    # Return in binary or decimal form depending on the input argument
    if bin_output == False:
        return " ".join(str(n) for n in bbs_gen_res)
    elif bin_output == True:
        return "".join(str(encryption_utils.get_even_parity_bit(n)) for n in bbs_gen_res)
