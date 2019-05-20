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
    'LAT': [],
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
        latRow=[]
        for col in state['hex']:
            latRow.append(calc_value(state, row, col))
        state['LAT'].append(latRow)


def calc_value(state, inputmask, outputmask):
    total = 0
    inputmask = state['hex'][inputmask]
    outputmask = state['hex'][outputmask]

    for eachHex in state['hex']:
        eachHex = state['hex'][eachHex]
        sboxi = eachHex #Input Bits , always from 0x0 to 0xF
        sboxo = state['sBox'][int(eachHex)] #Output Bits, from sBox table

        inputbit = []
        outputbit = []

        for i in range(4): #inputmask AND sboxInput
            x = ((0b0001 << i) & inputmask) >> i # GET DISTINCT BITS by shifting left and right
            y = ((0b0001 << i) & sboxi) >> i
            inputbit.append(x & y)

        for i in range(4): #outputmask & sboxOutput
            x = ((0b0001 << i) & outputmask) >> i # GET DISTINCT BITS by shifting left and right
            y = ((0b0001 << i) & sboxo) >> i
            outputbit.append(x & y)

        if (inputbit[0] ^ inputbit[1] ^ inputbit[2] ^ inputbit[3]) == (outputbit[0] ^ outputbit[1] ^ outputbit[2] ^ outputbit[3]):
            total += 1
    return total - 8 # 2**(n-1) - result


def print_LAT(state):
    coloumns = '0123456789ABCDEF'
    index=0

    print('    ',end = '')
    for hexno in state['hex']:
        print(' {:4} '.format(hexno[-1].upper()), end='')
    print('\n  |' + '-----|' * 16)

    for row in state['LAT']:
        print('{}'.format(coloumns[index]),end=' |')
        index +=1
        for element in row:
            print('{:3}  |'.format(element), end='')
        print('\n  |' + '-----|'*16)


def lat_max(state):
    max = -10000000
    first = 0
    for row in state['LAT']:
        if first == 0:
            first += 1
            continue
        for element in row:
            if(abs(element)>max):
                max = abs(element)
    return max


if __name__ == '__main__':
    print('\n\nLAT TABLE\n')

    s_box_list = False
    try:
        is_there_sbox = sys.argv[1]
        s_box_list = True
    except IndexError:
        print('\nUser Input s-Box')

    get_values(state, s_box_list)
    print_table(state)
    traverse(state)
    print_LAT(state)
    nlm = 2**(4-1) - lat_max(state)
    nlms = 2**(4-1) - 2**(4/2 - 1)
    percentage = nlm/nlms * 100
    print('Non Linear Measure: %{}'.format(percentage))
