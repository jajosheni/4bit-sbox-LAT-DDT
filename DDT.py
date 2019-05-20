import sys

state = {
    'size': 16,
    'sBox': [],
    'hex': {
        '0': 0x0, '1': 0x1, '2': 0x2, '3': 0x3,
        '4': 0x4, '5': 0x5, '6': 0x6, '7': 0x7,
        '8': 0x8, '9': 0x9, 'a': 0xa, 'b': 0xb,
        'c': 0xc, 'd': 0xd, 'e': 0xe, 'f': 0xf,
    },
    'DDT': [],
}


def get_values(state, mode):
    if mode:
        f = open("sBox.txt", "r")
        contents = f.read()
        contents = list(contents)

        for i in range(state['size']):
            state['sBox'].append(state['hex'][contents[i]])
    else:
        for i in range(state['size']):
            val = check_value(state, i)
            state['sBox'].append(state['hex'][val])


def check_value(state, i):
    val = input('Enter the sBox value for ' + hex(i) + ': ')
    while True:
        if len(val) is 1 and val.isdigit() and int(val) in range(0,10):
            return val
        elif len(val) is 1 and val in 'abcdef':
            return val
        else:
            val = input('Enter the sBox value for ' + hex(i) + ': ')


def print_table(state):
    for i in range(state['size']):
        print(hex(i), end=' | ')
    print('')
    print('----|-'*state['size'])
    for i in range(state['size']):
        print(hex(state['sBox'][i]), end=' | ')
    print('\n\nCalculating ...', end='\r')


def traverse(state):
    for row in state['hex']:
        ddtRow=[]
        for col in state['hex']:
            ddtRow.append(calc_value(state, row, col))
        state['DDT'].append(ddtRow)


def calc_value(state, a, b):
    total = 0
    a = state['hex'][a]
    b = state['hex'][b]

    for eachHex in state['hex']:
        eachHex = state['hex'][eachHex]
        sboxo = state['sBox'][int(eachHex)] # Output Bits, from sBox table

        x = state['sBox'][eachHex ^ a]

        if sboxo ^ x == b:
            total += 1

    return total


def print_DDT(state):
    coloumns = '0123456789ABCDEF'
    index=0

    print('    ',end = '')
    for hexno in state['hex']:
        print(' {:4} '.format(hexno[-1].upper()), end='')
    print('\n  |' + '-----|' * 16)

    for row in state['DDT']:
        print('{}'.format(coloumns[index]),end=' |')
        index += 1
        for element in row:
            print('{:3}  |'.format(element), end='')
        print('\n  |' + '-----|'*16)


if __name__ == '__main__':
    print('\n\nDDT TABLE\n')

    s_box_list = False
    try:
        is_there_sbox = sys.argv[1]
        s_box_list = True
    except IndexError:
        print('\nUser Input s-Box')

    get_values(state, s_box_list)
    print_table(state)
    traverse(state)
    print_DDT(state)


