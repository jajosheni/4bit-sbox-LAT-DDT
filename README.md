# 4bit-sbox-LAT-DDT

### Homework

#### 140201113

Language: `python3` on pyCharm</br>
Requirements: sympy</br>
 to install: `pip install sympy`

Code's logic: 
For both LAT & DDT there are similarities in the code:
1 big global variable holding the necessary information.
Next on get_values, check_value, print_table, traverse, print_DDT/print_LAT functions the input from the user is taken and shown in tables. The difference is on calc_value function: 

For LAT:
1. get the inputmask and outputmask from traverse function.
2. get the sboxinput and sboxoutput values
3. then take single bits from the both the inputs and outputs
4. xor and compare them
5. if the result is true increment the `total` variable
6. finally return `total - 2**(n-1) [2**(4-1) = 8]`
7. `[2**(n-1) - 2**(n/2 - 1) / 2**(n-1) - |max|]`  returns the percentage of `nlm`

For DDT:
1. get a and b from traverse function
2. then get the value for S(x ^ a) as variable x.
3. finally xOR it with S(X) which is sboxo
4. if the S(X) xOR S(X xOR a) == b returns true increment total
5. return total
