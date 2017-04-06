# written by 0oSpacebaro0 2017.03.13
# Not yet tested
from logger import logger


class Stega:
    def __init__(self, source_inf=None, secret_inf=None, injected_inf=None):
        self.source_inf = source_inf
        self.__secret_inf = secret_inf
        self.char_index = 0
        self.bit_index = 0
        self.code_len = 0
        self.injectedInf = injected_inf

        if secret_inf is not None:
            infmsg = "get secret_inf : %s " % secret_inf
            logger.info(infmsg)

    def reset(self):
        self.char_index = 0
        self.bit_index = 0
        self.code_len = 0
        self.__secret_inf = ''

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
        bit = asc >> (7 - self.bit_index) & 1
        infmsg = "getchar inf[%d] :%s the site:%d is %d" % (self.char_index, c, (7 - self.bit_index), bit)
        logger.info(infmsg)
        return bit

    def inject(self):
        # F3
        # return isSuccess, isEmpty, newInf
        if not self.__haveInf():
            return False, 0, None
        for i in range(len(self.source_inf)):
            ele = self.source_inf[i]
            bit = self.getIndex()
            # get injected element
            tmp = ele >> 1 << 1 | bit
            if (not tmp == 0) and (not ele == 0):
                self.source_inf[i] = tmp
                tmp = (self.bit_index + 1) // 8
                self.char_index += tmp
                self.bit_index = (self.bit_index + 1) % 8
                if self.char_index == len(self.__secret_inf):
                    self.__secret_inf = None
                    self.source_inf.insert(0, self.char_index)
                    return True, self.char_index, self.source_inf
            elif tmp == 0 and (ele == 1 or ele == -1):
                self.source_inf[i] = 0
        return False, self.char_index, self.source_inf

    def decrypt(self):
        # decrypt F3
        self.reset()
        tmp = 0
        if self.injectedInf is None:
            errmsg = "Missing encrypted information"
            logger.error(errmsg)
            return False, ""

        self.code_len = self.injectedInf[0]
        inf = self.injectedInf[1:]
        # print(inf)
        for i in inf:
            if i == 0:
                continue
            bit = i & 1
            tmp = tmp << 1 | bit
            self.bit_index = (self.bit_index + 1) % 8
            if self.bit_index == 0:
                infmsg = "Get ascii : %d" % tmp
                logger.info(infmsg)
                c = chr(tmp)
                tmp = 0
                self.__secret_inf += c
                self.char_index += 1
                if self.char_index == self.code_len:
                    return True, self.__secret_inf





if __name__ == '__main__':
    list = []
    for i in range(100):
        list.append(i)
    a = Stega(list, "hello word")
    isSuccess, len, newInf = a.inject()
    if isSuccess:
        print(newInf)
    else:
        print('error')
    a = Stega(None, None, newInf)
    isSuccess, secret_inf = a.decrypt()
    if isSuccess:
        print(secret_inf)
    else:
        print('error')