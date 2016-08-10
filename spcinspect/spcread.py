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
            self.endian = t.endian
            pl = self.get_payload(fd,t)
            print(t.code, t.size, pl)

    def get_payload(self,fd,tag):
        cnt = 1

        if self.endian == 0:
            ste = '<' # little endian
        else:
            ste = '>' # big endian
            
        if tag.code == 1:
            sdtype = ste + 'a' + str(tag.size)            
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.filetype = payload
            return payload
        
        if tag.code == 2:
            sdtype = ste + 'a' + str(tag.size)            
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.fileversion = payload
            return payload
            
        if tag.code == 3:
            sdtype = ste + 'a' + str(tag.size)            
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.filedate = payload
            return payload
            
        if tag.code == 4:
            sdtype = ste + 'a' + str(tag.size)            
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.targname = payload
            return payload

        if tag.code == 5:
            sdtype = ste + 'a' + str(tag.size)            
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.projname = payload
            return payload                  
            
        if tag.code == 6:
            sdtype = ste + 'f' + str(tag.size)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.energy = payload
            return payload

        if tag.code == 7: 
            sdtype = ste + 'f' + str(tag.size)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.peakpos = payload
            return payload

        if tag.code == 8: 
            sdtype = ste + 'f' + str(tag.size)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.norm = payload
            return payload                          
            
        if tag.code == 9: # number of depth steps
            sdtype = ste + 'u' + str(tag.size)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.ndsteps = payload
            return payload                          

        if tag.code == 10: # depth [g/cm**2]
            sdtype = ste + 'f' + str(tag.size)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.depth = payload
            return payload

        if tag.code == 11: # normalization of this depth step
            sdtype = ste + 'f' + str(tag.size)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.dsnorm = payload
            return payload                          

        if tag.code == 12: # number of particle species
            sdtype = ste + 'u' + str(tag.size)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.nparts = payload
            return payload                          

        if tag.code == 13: # data block, Z and A
            payload = np.zeros(4)
            
            sdtype = ste + 'f8'
            payload[0] = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))
            payload[1] = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))

            sdtype = ste + 'u4'
            payload[2] = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))
            payload[3] = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))

            self.z = payload[0]
            self.a = payload[1]
            self.lz = payload[2]
            self.la = payload[3]
            
            return payload
            
        if tag.code == 14: # CUM: cumulated number (running sum) of fragments
            sdtype = ste +'f'+str(tag.size)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.dsnorm = payload
            return payload
        
        if tag.code == 15: # nC: reserved for later use
            sdtype = ste + 'u' + str(tag.size)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.nc = payload
            return payload
        
        if tag.code == 16: # nE: number of energy bins
            sdtype = ste + 'u' + str(tag.size)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.ne = payload
            return payload
        
        if tag.code == 17: # E: energy bin values
            sdtype = ste + 'f8'
            cnt = int(tag.size/8)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))
            self.ebinvals = payload
            return payload
        
        if tag.code == 18: # EREF: if tag is set, then use copy of ebin from tag #17.
            sdtype = ste + 'u8'
            cnt = int(tag.size/8)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))[0]
            self.eref = payload
            return payload
        
        if tag.code == 19: # H[nE]: spectrum contens divided by the bin width
            sdtype = ste + 'f8' 
            cnt = int(tag.size/8)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))
            self.histvals = payload
            return payload
        
        if tag.code == 20: # running cumulated spectrum bin values
            sdtype = ste + 'f8'
            cnt = int(tag.size/8)
            payload = np.fromfile(fd,count=cnt,dtype=np.dtype(sdtype))
            self.cum = payload
            return payload
        
    
class tag(object):
    def __init__(self,fd):
        self.fd = fd
        self.code = 0
        self.size = 0
        self.endian = -1 # 0 little endian, 1 big endian, -1 unknown
        self._ste = ''
        pass


    def get_tag(self):
        if self.endian == -1:
            #try Intel first, little endian
            self.endian = 0
            self._ste = '<' # little endian read
            code = np.fromfile(self.fd,count=1,dtype=np.dtype(self._ste + 'u4'))[0]
            self.fd.seek(-4,1) # rewind 4 bytes
            print("NB1:",code)
            
            if code < 1 or code > 20: # if fail Intel, then:
                self.endian = 1 # big endian
                self._ste = '>' # big endian read
                code = np.fromfile(self.fd,count=1,dtype=np.dtype(self._ste + 'u4'))[0]
                print("NB2:",code)
                self.fd.seek(-4,1) # rewind 4 bytes, retry
                if code < 1 or code > 20:
                    print("Error: bad format in SPC file.")
                    exit()
                else:
                    print("Found big-endian format.")
                    
        self.code = np.fromfile(self.fd,count=1,dtype=np.dtype(self._ste + 'u4'))[0]
        self.size = np.fromfile(self.fd,count=1,dtype=np.dtype(self._ste + 'u4'))[0]
