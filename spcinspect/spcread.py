"""
    This file is part of SPCinspect.
"""
import numpy as np

class SPC(object):
    def __init__(self,filename):
        self.filename = filename

    def read_spc(self):
        print(self.filename)
        self.read_header()
        
        
    def read_header(self):
        fd = open(self.filename, "rb")
        t  =  tag(fd)

        for i in range(42):
            t.get_tag()
            print(t.code, t.size, t.payload)

    def read_data(self,fname):
        pass


class tag(object):
    def __init__(self,fp):
        self.fp = fp
        self.code = 0
        self.size = 0
        self.payload = []
        pass

    def get_tag(self):
        # todo: check endianess
        endian = '>' # Motorola
        #endian = '<' # Intel

        cnt = 1
        
        self.code = np.fromfile(self.fp,count=1,dtype=np.dtype(endian+'u4'))[0]
        self.size = np.fromfile(self.fp,count=1,dtype=np.dtype(endian+'u4'))[0]

        if self.code >= 1 and self.code <= 5:
            sdtype = endian+'a'+str(self.size)
        if self.code >= 6 and self.code <= 8: # get a double
            sdtype = endian+'f'+str(self.size)
        if self.code == 9: # usigned 8 byte integer
            sdtype = endian+'u'+str(self.size)
        if self.code == 10: #
            sdtype = endian+'f'+str(self.size)
        if self.code == 11: #
            sdtype = endian+'f'+str(self.size)
        if self.code == 12: #
            sdtype = endian+'u'+str(self.size)
        if self.code == 13:#special
            za = np.zeros(4)
            sdtype = endian+'f8'
            za[0] = np.fromfile(self.fp,count=cnt,dtype=np.dtype(sdtype))
            za[1] = np.fromfile(self.fp,count=cnt,dtype=np.dtype(sdtype))
            sdtype = endian+'u4'
            za[2] = np.fromfile(self.fp,count=cnt,dtype=np.dtype(sdtype))
            za[3] = np.fromfile(self.fp,count=cnt,dtype=np.dtype(sdtype))
            self.payload = za
            return
        if self.code == 14: #
            sdtype = endian+'f'+str(self.size)
        if self.code == 15: #
            sdtype = endian+'u'+str(self.size)
        if self.code == 16: #
            sdtype = endian+'u'+str(self.size)
        if self.code == 17: #
            sdtype = endian+'f8'
            cnt = int(self.size/8)
        if self.code == 18: #
            sdtype = endian+'u8'
            cnt = int(self.size/8)
        if self.code == 19: #
            sdtype = endian+'f8'
            cnt = int(self.size/8)
        if self.code == 20: #
            sdtype = endian+'f8'
            cnt = int(self.size/8)
        
        self.payload = np.fromfile(self.fp,count=cnt,dtype=np.dtype(sdtype))
