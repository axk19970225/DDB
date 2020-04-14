import os
import DDB
import pprint
import numpy as np
from DDB.Data import Reader
from scipy import signal as signal
import matplotlib.pyplot as plt

"""
Tag Complete Shot
"""

class eliminater:
    def __init__(self, hdf5_path=None):
        if hdf5_path:
            self.hdf5path = hdf5_path
        else:
            config = DDB.get_config()
            self.hdf5path = config['path']['hdf5']
        if not os.path.exists(self.hdf5path):
            os.mkdir(self.hdf5path)

    def TagNum(self, Taglist=None, Shotlist=None):
        Taglist  = list(Taglist)
        Shotlist = list(Shotlist)
        for i in range(len(Taglist)):
            Taglist[i] = Taglist[i][1:len(Taglist[i])]
        result = {}
        for i in Taglist:
            result.update({i: 0})
        reader = Reader(root_path=self.hdf5path)
        n = 1
        for i in Shotlist:
            print("第{}个".format(n))
            n += 1
            ShotTag = reader.tags(int(i))
            for k in range(len(ShotTag)):
                ShotTag[k] = ShotTag[k][1:len(ShotTag[k])]
            for j in Taglist:
                for tag in ShotTag:
                    if j == tag :
                        result[j] = result[j]+1
        pprint.pprint(result)

    def TCShotlist(self, Taglist=None, Shotlist=None, Detail=False):
        Shotlist = list(Shotlist)
        input = Shotlist.copy()
        reader = Reader(root_path=self.hdf5path)
        n = 1
        IncompleteNumber = []
        for i in Shotlist:
            print("第{}个".format(n))
            n += 1
            ShotTag = reader.tags(int(i))
            for j in Taglist:
                if j in ShotTag:
                    continue
                else:
                    IncompleteNumber.append(i)
                    break
        for i in IncompleteNumber:
            for j in Shotlist:
                if int(i) == int(j):
                    Shotlist.remove(j)
        outlist = Shotlist
        if Detail:
            print("Number of input shots    : {}".format(len(input)))
            print("Number of excluded shots : {}".format(len(IncompleteNumber)))
            print("Number of output shots   : {}".format(len(outlist)))
        return outlist

    def Vpfiltshot(self, Shotlist=None, Threshold=None, Detail=False):
        Shotlist = list(Shotlist)
        input = Shotlist
        if not Threshold:
            Threshold = 0.015
        reader = Reader(root_path=self.hdf5path)
        breakvp = []
        n = 1
        for shot in Shotlist:
            print("第{}个".format(n))
            n += 1
            data = reader.read_one(int(shot), r"\vp2")
            # 低通滤波
            ba = signal.butter(8, 0.01, "lowpass")
            fdata = signal.filtfilt(ba[0], ba[1], data[0])
            if max(fdata) < Threshold:
                breakvp.append(shot)
        output = breakvp
        if Detail:
            print("Number of input shots    : {}".format(len(input)))
            print("Number of output shots   : {}".format(len(output)))
        return output

    def Elimshot(self, Biglist=None, Smalllist=None):
        Biglist = list(Biglist)
        Smalllist = list(Smalllist)
        for i in Smalllist:
            for j in Biglist:
                if int(i) == int(j):
                    Biglist.remove(j)
        return Biglist


