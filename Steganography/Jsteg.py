
class Jsteg():
    def __init__(self):
        pass

    def get_scale(self, carrier):
        count = 0
        for i in carrier:
            if i!=0 and abs(i) != 1:
                count+=1
        return count

    def uninject(self, carrier):
        info = ""
        byte = header = 0
        index = ch_count = bit_count = 0
        res = []
        i = 0
        while i < 16 and index < len(carrier):
            if carrier[index] != 0 and abs(carrier[index]) != 1:
                header = (header<<1) | (carrier[index]&1)
                i+=1
            index += 1

        while ch_count < header:
            while index < len(carrier):
                if carrier[index] != 0 and abs(carrier[index]) != 1:
                    byte = (byte<<1) | (carrier[index]&1)
                    bit_count = (bit_count+1)%8
                    if bit_count == 0:
                        ch_count+=1
                        res.append(chr(byte))
                        index += 1
                        byte = 0
                        break
                index += 1
        return "".join(res)

    def inject(self, carrier, info):
        header = divmod(len(info),256)
        info = "".join([chr(header[0]),chr(header[1]),info])
        index = 0
        bit = 0
        for ch in info:
            while index < len(carrier):
                if carrier[index] != 0 and abs(carrier[index]) != 1:
                    to_write = (ord(ch)>>(7-bit))&1
                    carrier[index] = (carrier[index]>>1)<<1 | to_write
                    bit = (bit+1)%8
                    index += 1
                    if bit == 0:
                        break
                else:
                    index += 1
        return carrier

if __name__ == '__main__':
    from encoder.Decoder import *
    from encoder.Encoder import *
    jsteg = Jsteg()
    # _d = Decoder()
    # _e = Encoder()
    #
    # _file_str="F:/test.jpg"
    # _file=open(_file_str,'wb')
    #
    import random

    lst=[random.randint(-128,127) for i in range(10000)]
    random.shuffle(lst)
    str = "hello world!"
    in_lst = jsteg.inject(lst,str)
    print(jsteg.uninject(in_lst))

    # _e.encode(in_lst,_file)
    #
    # _file=open(_file_str,'rb')
    # lst=_d.decode(_file)
    #
    # str = jsteg.uninject(lst)
    # print(str)
    # # print(in_lst)
    #





