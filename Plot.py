import os
import numpy as np
import traceback
import matplotlib.pyplot as plt
import DDB
from DDB.Data import Reader
from DDB.Service import Query


def isNum(value):
    try:
        value + 1
    except TypeError:
        return False
    else:
        return True


class Ploter:
    """
    Plot 
    Input:
        Taglist    The list of tags which you want to plot.
        Shotlist   The list of Shots which you want to plot.
    Output:
    
    
    """
    def __init__(self, hdf5_path=None):
        if hdf5_path:
            self.hdf5path = hdf5_path
        else:
            config = DDB.get_config()
            self.hdf5path = config['path']['hdf5']
        if not os.path.exists(self.hdf5path):
            os.mkdir(self.hdf5path)


    def plot_one(self, Tag=None, Shot=None, Savepath=None, xline=None ,yline=None, Showplot=False):
        if Savepath:
            root_path = Savepath
            if not os.path.exists(root_path):
                raise ValueError('No such saving path, you need to create one! ')
        else:
            root_path = os.getcwd() + os.sep + "plot"
            print(root_path)
            if not os.path.exists(root_path):
                os.makedirs(root_path)

        reader = Reader(root_path=self.hdf5path)
        try:
            data = reader.read_one(int(Shot), Tag)
            tag_name = Tag[1:]
            plt.figure((str(Shot) + tag_name))
            plt.plot(data[1], data[0], 'g')
            if xline:
                if not isNum(xline):
                    raise ValueError('xline needs to be number ')
                plt.axvline(round(xline, 3))
            if yline:
                if not isNum(yline):
                    raise ValueError('yline needs to be number ')
                plt.axhline(round(yline, 3))
            name = str(Shot)+ r" " + tag_name
            path = root_path + os.sep + r"{}.png".format(name)
            plt.savefig(path)
            if Showplot:
                plt.show()
            plt.close()
        except Exception as err:
            print("Shot:{}".format(shot) + " Tag:{}  ".format(tag_name) + "No data")
            plt.close()
            pass



    def plot_much(self, Taglist=None, Shotlist=None, Savepath=None,ShowDownTime=False,ShowIpFlat=False, xline = None ,yline = None):
        if Savepath:
            root_path = Savepath
            if not os.path.exists(root_path):
                raise ValueError('No such saving path, you need to create one! ')
        else:
            root_path = os.getcwd() + os.sep + "plot"
            print(root_path)
            if not os.path.exists(root_path):
                os.makedirs(root_path)
        for tag in Taglist:
            tag_name = tag[1:]
            file_path = root_path + os.sep + tag_name
            if not os.path.exists(file_path):
                os.makedirs(file_path)

        reader = Reader(root_path = self.hdf5path)
        db = Query()
        for tag in Taglist:
            tag_name = tag[1:]
            file_path = root_path + os.sep + tag_name
            n = 1
            for shot in Shotlist:
                print("Shot:{}".format(shot) + " Tag:{}  ".format(tag_name) + "No.{}".format(n))
                n += 1
                try:
                    shot_info = db.tag(int(shot))
                    data = reader.read_one(int(shot), tag)
                    plt.figure((str(shot) + tag_name))
                    plt.plot(data[1], data[0], 'g')
                    if ShowDownTime:
                        if shot_info["IsValidShot"]:
                            if shot_info["IsDisrupt"]:
                                plt.axvline(round(shot_info["CqTime"], 3), c='r')
                            else:
                                plt.axvline(round(shot_info["RampDownTime"], 3), c='r')
                    if ShowIpFlat:
                        if tag == r"\ip":
                            if shot_info["IsValidShot"]:
                                plt.axhline(round(shot_info["IpFlat"], 3), c='k')
                    if xline:
                        if not isNum(xline):
                            raise ValueError('xline needs to be number ')
                        plt.axvline(round(xline, 3))
                    if yline:
                        if not isNum(yline):
                            raise ValueError('yline needs to be number ')
                        plt.axhline(round(yline, 3))
                    path = file_path + os.sep + r"{}.png".format(shot)
                    plt.savefig(path)
                    plt.close()
                except Exception as err:
                    print("Shot:{}".format(shot) + " Tag:{}  ".format(tag_name) + "No data")
                    plt.close()
                    pass
