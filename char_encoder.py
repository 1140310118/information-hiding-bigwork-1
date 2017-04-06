
def char2bin(str):
    lst = []
    for ch in str:
        lst.append(bin(ord(ch)))
    return "".join(lst)

def bin2char(str):
    lst = str.split('0b')
    res = []
    for s in lst[1:]:
        res.append(chr(eval('0b'+s)))
    return ''.join(res)

if __name__ == '__main__':
    # encode = char2bin('你好99')
    # print (type(encode),encode)
    # decode = bin2char(encode)
    # print(decode)
    