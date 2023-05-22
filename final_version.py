import os
import random
import string
import sys
import uuid
import argparse

# Générer des noms de variables aléatoires
var_names = ["_"+str(uuid.uuid4().hex) for _ in range(19)]


NumberToRoman_name, RomanToNumber_name, digitsToRoman_name, romanToDigits_name, obfuscated_code_name, \
deobfuscated_code_name, roman_name, obfuscated_char_name, result_name, numeral_name, integer_name, index_name, \
chr_name, ord_name, exec_name, int_name, str_name, len_name, c    = var_names

NumberToRoman = (
    (1000, 'm'),
    ( 900, 'cm'),
    ( 500, 'd'),
    ( 400, 'cd'),
    ( 100, 'c'),
    (  90, 'xc'),
    (  50, 'l'),
    (  40, 'xl'),
    (  10, 'x'),
    (   9, 'ix'),
    (   5, 'v'),
    (   4, 'iv'),
    (   1, 'i'),
)

RomanToNumber = {v: k for k, v in NumberToRoman}

def cipher(s, shift):
    return ''.join(chr(ord(c) - shift) for c in s), -shift


def random_cipher(s):
    shift = random.randint(1, 64) 
    return cipher(s, shift)

def digitsToRoman(value):
    roman = ''
    for n, r in NumberToRoman:
        fact, value = divmod(value, n)
        roman += r * fact
        if not value:
            break
    return roman

def romanToDigits(roman):
    result = 0
    index = 0
    for numeral, integer in RomanToNumber.items():
        while roman[index:index+len(numeral)].lower() == numeral.lower():
            result += integer
            index += len(numeral)
    result = str(result)
    if index < len(roman):
        result += romanToDigits(roman[index:])
    return result

def cipher_code(code):
    return '_'.join([digitsToRoman(ord(c)) for c in code])

def obf(obfuscated_code):
     
    chr_rotated, chr_shift = random_cipher('chr')
    ord_rotated, ord_shift = random_cipher('ord')
    len_rotated, len_shift = random_cipher('len')
    int_rotated, int_shift = random_cipher('int')
    str_rotated, str_shift = random_cipher('str')
    exec_rotated, exec_shift = random_cipher('exec')
    
    template = f"""
{NumberToRoman_name} = {NumberToRoman}
{RomanToNumber_name} = {RomanToNumber}
{chr_name} = ''.join(chr(ord({c}) - {chr_shift}) for {c} in '{chr_rotated}')
{ord_name} = ''.join(__builtins__.__dict__[{chr_name}](ord({c}) - {ord_shift} ) for {c} in '{ord_rotated}')
{exec_name} = ''.join(__builtins__.__dict__[{chr_name}](__builtins__.__dict__[{ord_name}]({c}) - {exec_shift}) for {c} in '{exec_rotated}')
{int_name} = ''.join(__builtins__.__dict__[{chr_name}](__builtins__.__dict__[{ord_name}]({c}) - {int_shift}) for {c} in '{int_rotated}')
{str_name} = ''.join(__builtins__.__dict__[{chr_name}](__builtins__.__dict__[{ord_name}]({c}) - {str_shift}) for {c} in '{str_rotated}')
{len_name} = ''.join(__builtins__.__dict__[{chr_name}](__builtins__.__dict__[{ord_name}]({c}) - {len_shift}) for {c} in '{len_rotated}')

def {romanToDigits_name}({roman_name}):
    {result_name} = 0
    {index_name} = 0
    for {numeral_name}, {integer_name} in {RomanToNumber_name}.items():
        while {roman_name}[{index_name}:{index_name}+__builtins__.__dict__[{len_name}]({numeral_name})].lower() == {numeral_name}.lower():
            {result_name} += {integer_name}
            {index_name} += __builtins__.__dict__[{len_name}]({numeral_name})
    {result_name} = __builtins__.__dict__[{str_name}]({result_name})
    if {index_name} < __builtins__.__dict__[{len_name}]({roman_name}):
        {result_name} += {romanToDigits_name}({roman_name}[{index_name}:])
    return {result_name}

{obfuscated_code_name} = '{obfuscated_code}'
{obfuscated_code_name} = {obfuscated_code_name}.strip().split('_')
{deobfuscated_code_name} = ''
for {obfuscated_char_name} in {obfuscated_code_name}:
    if {obfuscated_char_name}:
        {deobfuscated_code_name} += __builtins__.__dict__[{chr_name}](__builtins__.__dict__[{int_name}]({romanToDigits_name}({obfuscated_char_name})))
__builtins__.__dict__[{exec_name}]({deobfuscated_code_name})
"""
    return template

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="input file")
    parser.add_argument("--output", "-o", help="output file")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r") as f:
            code = f.read()

        payload = cipher_code(code)
        obfuscated_code = obf(payload)
        
        if args.output:
            with open(args.output, "w") as f:
                f.write(obfuscated_code)
        else:
            print(obfuscated_code)

if __name__ == "__main__":
    main()

