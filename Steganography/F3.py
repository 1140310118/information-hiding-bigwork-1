# written by 0oSpacebaro0 2017.03.13
# Not yet tested
from logger import logger

class Stega:
    def __init__(self, source_inf=None, secret_inf=None):
        self.source_inf = source_inf
        self.__secret_inf = secret_inf
        self.char_index = 0
        self.bit_index = 0
        infmsg = "get secret_inf : %s " % secret_inf
        infmsg = "get secret_inf : %s " % secret_inf
        logger.info(infmsg)

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

    def getIndex(self):
        # aim char
        c = self.__secret_inf[self.char_index]
        # to ascii
        asc = ord(c)
        # aim bit
        bit = asc >> self.bit_index & 1
        infmsg = "getchar inf[%d] :%s the site:%d is %d" % (self.char_index, c, self.bit_index, bit)
        logger.info(infmsg)
        return bit

    def inject(self):
        # F3
        # return isSuccess, isEmpty, newInf
        if not self.__haveInf():
            return False, False, None
        for i in range(len(self.source_inf)):
            ele = self.source_inf[i]
            bit = self.getIndex()
            # get injected element
            tmp = ele >> 1 << 1 | bit
            # 三种情况，注入与原始相同且不为 0
            #
            #if ele == tmp and not tmp == 0:
            if (not tmp == 0) and (not ele == 0):
                self.source_inf[i] = tmp
                tmp = (self.bit_index + 1) // 8
                self.char_index += tmp
                self.bit_index = (self.bit_index + 1) % 8
                if self.char_index == len(self.__secret_inf):
                    self.__secret_inf = None
                    return True, True, self.source_inf
            elif tmp == 0 and (bit == 1 or bit == -1):
                self.source_inf[i] = 0
        return True, False, self.source_inf

if __name__ == '__main__':
    list = []
    for i in range(100):
        list.append(i)
    a = Stega(list, "hello word");
    isSuccess, isEmpty, newInf = a.inject()
    if isSuccess:
        print(newInf)
    else:
        print('error')