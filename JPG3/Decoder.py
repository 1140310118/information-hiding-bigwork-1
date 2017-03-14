import struct
from JPG3.Huffman import *
from JPG3.CONSTANT import *
from Steganography.Jsteg import *

class Decoder:
    def __init__(self):
        self.leaf_dict = {None:Leaf(None,0)}
        self.huff_tree = None
    def decode(self, file_in):
        self.__init__()
        self._read_header(file_in)
        self.huff_tree = Huffman(self.leaf_dict)
        _root = self.huff_tree.root
        n=_root

        all_bytes = file_in.read()

        bytes = struct.unpack(str(len(all_bytes))+'B', all_bytes)

        res = []
        count = 0
        for b in bytes:
            while count < LEN:
                if n.lchild is None and n.rchild is None and n.weight != 0:
                    res.append(n.value)
                    n = _root
                elif n.lchild is not None or n.rchild is not None:
                    n = n.lchild if (b>>(LEN-1)&1)==0 else n.rchild
                    b <<= 1
                    count += 1
                else:
                    return res
            count = 0
        return res
    def _read_header(self, file_in):
        # header size: 1k
        header = file_in.read(1024)
        unpacked_header = struct.unpack('256I',header)
        for i in range(len(unpacked_header)):
            if unpacked_header[i] != 0:
                self.leaf_dict[i-128] = Leaf(i-128,unpacked_header[i])

if __name__ == '__main__':
    decoder = Decoder()
    jsteg = Jsteg()
    file_in = open("F:\\hello.jpg",'rb')
    print(jsteg.uninject(decoder.decode(file_in)))