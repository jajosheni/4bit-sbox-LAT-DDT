from sympy import *
x = symbols('x')

state = {
    'sBox': {
        '0': '', '1': '', '2': '', '3': '',
        '4': '', '5': '', '6': '', '7': '',
        '8': '', '9': '', 'A': '', 'B': '',
        'C': '', 'D': '', 'E': '', 'F': '',
    },
    'hex': {
        '0': 0x0, '1': 0x1, '2': 0x2, '3': 0x3,
        '4': 0x4, '5': 0x5, '6': 0x6, '7': 0x7,
        '8': 0x8, '9': 0x9, 'a': 0xa, 'b': 0xb,
        'c': 0xc, 'd': 0xd, 'e': 0xe, 'f': 0xf,
    },
    'symbolEquation:': x,
    'irreducibleEquation': ['0', '0', '0', '0', '0'],  # x4 + x3+x2+x1+1
    'objects': {
        '0': 0x1,   '1': x,     '2': '',    '3': '',
        '4': '',    '5': '',    '6': '',    '7': '',
        '8': '',    '9': '',    '10': '',   '11': '',
        '12': '',   '13': '',   '14': '',   '15': '',
    },
    'binaryObjects': {
        '0': 0b1,   '1': '',    '2': '',    '3': '',
        '4': '',    '5': '',    '6': '',    '7': '',
        '8': '',    '9': '',    '10': '',   '11': '',
        '12': '',   '13': '',   '14': '',   '15': '',
    },
    'mappingEquation': x,
    'mappingInteger': 1,
    'mappingBox': {                # X => X^1
        '0': 0x0,    '1': x**1,    '2': x**2,    '3': x**3,
        '4': x**4,   '5': x**5,    '6': x**6,    '7': x**7,
        '8': x**8,   '9': x**9,    '10': x**10,   '11': x**11,
        '12': x**12, '13': x**13,  '14': x**14,   '15': x**15,
    },
}


def get_irreducible_equation(state):
    print('Irreducible Equation format: x4 + x3 + x2 + x1 + 1')
    stri = input('Enter Irreducible Equation: ')
    state['irreducibleEquation'] = symbol_to_binary(stri, 1)
    state['symbolEquation'] = binary_to_symbol(state['irreducibleEquation'])


def binary_to_symbol(equation):
    return_symbol = x**4
    if equation[-1] == '1':
        return_symbol += 1

    j = 3
    for i in range(1,4):
        if equation[i] == '1':
            return_symbol += x**j
        j -= 1

    return return_symbol

# -----------------------------------------------------------------
# ---------------------------- Objects ----------------------------
# -----------------------------------------------------------------


def create_objects(state):
    for i in range(2,16):
        prev_symbol = state['objects'][str(i-1)]
        next_symbol = expand(prev_symbol * x)
        state['objects'][str(i)] = custom_mod(next_symbol)

    state['binaryObjects']['0'] = ['0', '0', '0', '1']
    for i in range(1, 16):
        state['binaryObjects'][str(i)] = symbol_to_binary(str(state['objects'][str(i)]).replace('*', ''))


def custom_mod(first_exp):
    if 'x**4' in str(first_exp):
        first_exp -= x**4
        first_exp += state['symbolEquation'] - x**4

    result = expand(first_exp)

    for i in range (1, 4):
        if '2*x**'+str(i) in str(result):
            result -= 2*x**i
    if '2*x' in str(result):
        result -= 2*x
    if str(result)[-1] == ' 2':
        result -= 2
    return result


def symbol_to_binary(equation, mode=0):
    if mode == 1:
        return_str = ['0', '0', '0', '0', '0']
        if equation[-1] == '1':
            return_str[4] = '1'

        j = 0
        for i in range(4, 0, -1):
            if ('x' + str(i)) in equation:
                return_str[j] = '1'
            j += 1
    else:
        return_str = ['0', '0', '0', '0']
        if equation[-1] == '1':
            return_str[3] = '1'

        j = 0
        for i in range(3, 0, -1):
            if ('x' + str(i)) in equation:
                return_str[j] = '1'
            j += 1

    if 'x ' in str(equation):
        return_str[2] = '1'
    if equation[-1] =='x':
        return_str[2] = '1'

    return return_str

# -----------------------------------------------------------------
# ---------------------------- Mapping ----------------------------
# -----------------------------------------------------------------


def get_mapping_equation(state):
    print('Mapping Equation Format: positive/negative integer n ==> X => X^n')
    stri = input('Enter Mapping Integer: ')
    n = int(stri)
    state['mappingEquation'] = x**n
    state['mappingInteger'] = n


def mapping_box(state):
    for i in range(1, 16):
        state['mappingBox'][str(i)] = state['mappingBox'][str(i)]**(state['mappingInteger'])
        state['mappingBox'][str(i)] = custom_mapping_mod(state['mappingBox'][str(i)])


def custom_mapping_mod(first_exp):
    mode = state['mappingInteger'] < 0
    pow_ = strip_integer(first_exp, mode)

    if mode:
        pow_ = floor(pow_ / 15)
        first_exp *= ((x**15)**pow_) * (x**15)
        if first_exp == x**15:
            first_exp = 1
    else:
        pow_ = floor(pow_ / 15)
        if pow_ == 0:
            first_exp = first_exp
        else:
            first_exp = first_exp * ((x ** -15) ** pow_)

        if first_exp == x ** 15:
            first_exp = 1

    return first_exp


def strip_integer(number, mode):
    if mode:
        number = str(number).replace('x', '')
        number = number.replace('*', '')
        number = number.replace('(', '')
        number = number.replace(')', '')
        if '1/' in number:
            number = -1
        number = int(number)
    else:
        number = str(number).replace('x', '')
        number = number.replace('*', '')
        number = int(number)

    return abs(number)

# -----------------------------------------------------------------
# ------------------------------ sBox -----------------------------
# -----------------------------------------------------------------


def create_s_box(state):
    state['sBox']['0'] = '0'

    for i in range (1, 16):
        first_char = i
        mapped_char = str(state['mappingBox'][str(i)])

        if mapped_char == 'x':
            mapped_char = 1
        elif 'x' not in mapped_char:
            mapped_char = 0
        else:
            mapped_char = mapped_char.replace('*','')
            mapped_char = mapped_char.replace('x', '')

        first_char = binary_to_hex(state['binaryObjects'][str(first_char)])
        mapped_char = binary_to_hex(state['binaryObjects'] [str(mapped_char)])

        state['sBox'][str(first_char).capitalize()[-1]] = str(mapped_char).capitalize()[-1]


def print_table(state):
    print('')
    for i in range(16):
        print(hex(i), end=' | ')
    print('')
    print('----|-'*16)
    for i in state['hex']:
        print(hex(state['hex'][state['sBox'][i]]), end=' | ')


def binary_to_hex(binary_number):
    if type(binary_number) != int:
        str1 = ''.join(binary_number)
        str1 = '0b' + str1
        binary_number = hex(int(str1, 2))
    else:
        binary_number = hex(int(binary_number))

    return binary_number

# -----------------------------------------------------------------
# ------------------------------ Main -----------------------------
# -----------------------------------------------------------------


def save_table(state):
    f = open('sBox.txt', 'w+')
    for i in state['hex']:
        f.write(str(hex(state['hex'][state['sBox'][i]])[-1]))
    f.close()


if __name__ == '__main__':
    get_irreducible_equation(state)

    create_objects(state)
    print('Objects:')
    for i in range(16):
        print(str(i) + ':\t' + str(state['binaryObjects'][str(i)]) + '\t' + str(state['objects'][str(i)]))

    get_mapping_equation(state)
    print('\nMapping Equation: x => ' + str(state['mappingEquation']))

    mapping_box(state)
    for i in range(16):
        print('x**' + str(i) + '\t=>\t' + str(state['mappingBox'][str(i)]))

    create_s_box(state)
    print_table(state)
    save_table(state)