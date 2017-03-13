
class Jsteg():
    def __init__(self):
        pass

    def uninject(self, carrier):
        info = ""
        byte = header = 0
        index = ch_count = bit_count = 0
        res = []
        i = 0
        while i < 16 and index < len(carrier):
            if carrier[index] != 0 and abs(carrier[index]) != 1:
                header = (header<<1) | (carrier[index]%2)
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
    jsteg = Jsteg()
    lst = [1,23,43,2,1,4]+[9]*99
    str = "to"
    in_lst = jsteg.inject(lst,str)
    out_lst = jsteg.uninject(lst)
    print(out_lst)
    # print(in_lst)






