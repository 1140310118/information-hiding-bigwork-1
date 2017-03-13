# written by 0oSpacebaro0 2017.03.13
# Not yet tested
from logger import logger

class Stega:
    def __init__(self, source_inf=None, secret_inf=None):
        self.source_inf = source_inf
        self.__secret_inf = secret_inf
        self.char_index = 0
        self.bit_index = 0

    def __haveInf(self):
        if self.source_inf is None:
            errmsg = 'Lack of carrier'
            logger.error(errmsg)
            return False
        if self.__secret_inf is None:
            errmsg = 'Lack of secret Inf'
            logger.error(errmsg)
            return False
        return True

    def addSecretInf(self,secret_int=None):
        if isinstance(secret_int, str):
            self.__secret_inf += secret_int
            return True
        else:
            return False

    def inject(self):
        # F3
        # return isSuccess, isEmpty, newInf
        if not self.__haveInf():
            return False, False, None
        for i in range(len(self.source_inf)):
            ele = self.source_inf[i]
            # aim char
            c = self.__secret_inf[self.char_index]
            # aim bit
            bit = c & (1 << self.bit_index) >> self.bit_index
            bit |= 1111111 << 1
            # get injected element
            tmp = ele & bit
            #
            if ele == tmp and not tmp == 0:
                self.source_inf[i] = tmp
                tmp = (self.bit_index + 1) // 8
                self.char_index += tmp
                self.bit_index = (self.bit_index + 1) % 8
                if self.char_index == len(self.__secret_inf)+1:
                    return True, True, self.source_inf
            elif tmp == 0 and (bit == 1 or bit == -1):
                self.source_inf[i] = 0
        return True, False, self.source_inf
