# MD5 实现及其验证
import math
import sys
import os

rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

# A B C D
init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
# 非线性函数
functions = 16 * [lambda b, c, d: (b & c) | (~b & d)] + \
            16 * [lambda b, c, d: (d & b) | (~d & c)] + \
            16 * [lambda b, c, d: b ^ c ^ d] + \
            16 * [lambda b, c, d: c ^ (b | ~d)]

index_functions = 16 * [lambda i: i] + \
                  16 * [lambda i: (5 * i + 1) % 16] + \
                  16 * [lambda i: (3 * i + 5) % 16] + \
                  16 * [lambda i: (7 * i) % 16]


# 对x左移amount位
def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


def md5(message):
    message = bytearray(message)  # copy our input into a mutable buffer
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder='little')

    hash_pieces = init_values[:]

    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:chunk_ofst + 64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))
def md5_to_hex(digest): #将结果以16进制字符串输出
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))
def my_md5(message): #对MD5进行最后的封装
    return md5_to_hex(md5(message))


if __name__ == '__main__':
    argv1 = sys.argv[1]  # 获取操作
    if argv1=="-h":
        print("[-h]:--help information")
        print("[-t]:[content of string]--compute MD5 of string")
        print("[-c]:[[file path of the file computed]--compute MD5 of given file")
        print("[-f]:[file path of the file validated] [file path of the .md5 file]")
        print("     --validate the integrality of a given file by read MD5 value from .md5 file")
    elif argv1=="-t":
        argv2 = sys.argv[2] # string
        message = argv2.encode("utf-8")
        print("MD5 of "+argv2+" is ",my_md5(message))
    elif argv1=="-c":
        argv2 = sys.argv[2] #filename
        with open(argv2, 'rb') as fp:
            data = fp.read()
        bmd5 = md5(data)
        md5result=argv2+".md5"
        with open(md5result, 'wb') as fs:
            fs.write(bmd5.to_bytes(16, byteorder='little'))
        print("MD5 value of file("+argv2+") is ",md5_to_hex(bmd5))
        print("MD5 value is also stored in current folder as "+argv2+".md5 .")
    elif argv1=="-f":
        argv2 = sys.argv[2] # file validated
        argv3 = sys.argv[3] # .md5 file
        with open(argv2,'rb') as f:
            data = f.read()
        with open(argv3,'rb') as f_old:
            bOldMd5=f_old.read()
        # oldMd5 = md5_to_hex(bOldMd5)
        oldMd5 = '{:032x}'.format(int.from_bytes(bOldMd5, byteorder='big'))
        print("The old MD5 value of file("+argv2+") is ",oldMd5)
        newMd5 = my_md5(data)
        print("The new MD5 value of file("+argv2+") computed is ",newMd5)
        if oldMd5==newMd5:
            print("OK! The file is integrated")
        else:
            print("Match Error! The file has been modified!")
    else:
        print("No valid option. For more information, type '-h'")




