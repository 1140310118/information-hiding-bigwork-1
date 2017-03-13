from JPG3.Huffman import *
import struct
from JPG3.CONSTANT import *

class Encoder:

    def __init__(self):
        # 终止节点
        self.leaf_dict = {None:Leaf(None,0)}
        self.huff_tree = None
        self._freq_table = [0 for i in range(CHAR_SIZE)]

    def _scan(self,lst):
        for key in lst:
            self._freq_table[key+128] += 1
            if key not in self.leaf_dict:
                self.leaf_dict[key] = Leaf(key,1)
            else:
                self.leaf_dict[key].weight += 1

    def _get_code(self,n):
        stack = []
        while n.parent is not None:
            if n is n.parent.lchild:
                stack.append(0)
            elif n is n.parent.rchild:
                stack.append(1)
            else:
                assert "Logistic error!"
            n = n.parent
        return stack

    def _write_header(self, f_out):
        header = (struct.pack('I',self._freq_table[i]) for i in range(CHAR_SIZE))
        f_out.write(b"".join(header))

    def encode(self, lst, file_in):
        self._scan(lst)
        self.huff_tree = Huffman(self.leaf_dict)
        self._write_header(file_in)

        res = []
        reg = 0
        bit_count = 0
        for ch in lst:
            n = self.leaf_dict[ch]
            stack = self._get_code(n)
            while len(stack) > 0:
                reg = (reg << 1) | stack.pop()
                bit_count += 1
                if bit_count % LEN == 0:
                    bit_count = 0
                    res.append(reg)
                    reg = 0
        if bit_count != 0:
            stack = self._get_code(self.leaf_dict[None])
            while bit_count < LEN and len(stack) > 0:
                reg = (reg << 1) | stack.pop()
                bit_count += 1
            if bit_count < LEN:
                reg << (LEN - bit_count)
            res.append(reg)
            byte_str = (struct.pack('B',res[i]) for i in range(len(res)))
            file_in.write(b"".join(byte_str))

if __name__ == "__main__":
    encoder = Encoder()
    file = "F:\\hello.jpg"
    encoder.encode([-128,-127,0,1,0,1,1]+[0]*100,open(file,'wb'))