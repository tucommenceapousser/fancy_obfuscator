import os
import random
import string
import sys

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

def deobfuscate_code(obfuscated_code):
    obfuscated_code = obfuscated_code.strip().split('_')
    deobfuscated_code = ''
    for obfuscated_char in obfuscated_code:
        if obfuscated_char:
            deobfuscated_code += chr(int(romanToDigits(obfuscated_char)))
    return deobfuscated_code

def execute_deobfuscated(deobfuscated_code):
    exec(deobfuscated_code)

def main():
    obfuscated_code = 'cxii_cxiv_cv_cx_cxvi_xl_xxxix_civ_ci_cviii_cviii_cxi_xxxix_xli_x_'
    print("Obfuscated code:", obfuscated_code)
    deobfuscated_code = deobfuscate_code(obfuscated_code)
    print("Deobfuscated code:", deobfuscated_code)
    execute_deobfuscated(deobfuscated_code)

if __name__ == '__main__':
    main()
