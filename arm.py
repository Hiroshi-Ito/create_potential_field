from matplotlib import pyplot as plt
import numpy as np
import math

L1 = 26.0
L2 = 46.0

class arm_class(object):
    def __init__(self, ax, pix_err=1):
        print "arm init"
        self.canvas = ax.get_figure().canvas
        self.x = np.zeros(3)
        self.y = np.zeros(3)
        self.angle = np.zeros(2)
        self.pt_plot = ax.plot([], [], marker='o', zorder=5)[0]


    def calc_invkinematicks(self, x, y):
        print "calc_invkinematicks : ", x, y
        numer = math.sqrt( 4*L1*L1*L2*L2 - ((x*x + y*y) - (L1*L1 + L2*L2))*((x*x + y*y) - (L1*L1 + L2*L2)))
        denom = 2*L1*L1 + (x*x + y*y) - (L1*L1 + L2*L2)
        self.angle[0] = -( math.atan2(x,y) - math.atan2(numer,denom) - np.deg2rad(90) )
        self.angle[1] = -( np.arccos( ((x*x + y*y) - (L1*L1 + L2*L2)) / (2*L1*L2) ) )
        #print "calc angle = ", self.angle*180/3.14
        self.plt_trj()

    def plt_trj(self):
        print "plt trj"
        self.x[0] = 0
        self.y[0] = 0
        self.x[1] = L1*math.cos(self.angle[0]);
        self.y[1] = L1*math.sin(self.angle[0]);
        self.x[2] = self.x[1] + L2*math.cos(self.angle[0] + self.angle[1]);
        self.y[2] = self.y[1] + L2*math.sin(self.angle[0] + self.angle[1]);
        self.pt_plot.set_xdata(self.x)
        self.pt_plot.set_ydata(self.y)
