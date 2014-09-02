from matplotlib import pyplot as plt
import numpy as np
import math

L1 = 26.0
L2 = 46.0

class arm_class(object):
    def __init__(self, ax, pix_err=1):
        print "arm init"
        self.canvas = ax.get_figure().canvas
        self.x = np.zeros(2)
        self.y = np.zeros(2)
        self.angle = np.zeros(2)
        self.pt_plot = ax.plot([], [], marker='o',linestyle='none', zorder=5)[0]


    def calc_invkinematicks(self, x, y):
        print "calc_invkinematicks : ", x, y
        #print x,y
        #print self.x,self.y
        numer = math.sqrt( 4*L1*L1*L2*L2 - ((x*x + y*y) - (L1*L1 + L2*L2))*((x*x + y*y) - (L1*L1 + L2*L2)))
        print numer
        denom = 2*L1*L1 + (x*x + y*y) - (L1*L1 + L2*L2)
        self.angle[0] = -( math.atan2(x,y) - math.atan2(numer,denom) - np.deg2rad(90) )
        self.angle[1] = -( np.arccos( ((x*x + y*y) - (L1*L1 + L2*L2)) / (2*L1*L2) ) )
        #numer = math.sqrt( 4*L1*L1*L2*L2 - ((self.x*self.x + self.y*self.y) - (L1*L1 + L2*L2))*((self.x*self.x + self.y*self.y) - (L1*L1 + L2*L2)))
        #denom = 2*L1*L1 + (self.x*self.x + self.y*self.y) - (L1*L1 + L2*L2)
        #self.angle[0] = math.atan2(self.x,self.y) - math.atan2(numer,denom)
        #self.angle[1] = math.acos( ((self.x*self.x + self.y*self.y) - (L1*L1 + L2*L2)) / (2*L1*L2) )
        print "calc angle = ", self.angle*180/3.14
        self.plt_trj()

    def plt_trj(self):
        print "plt trj"
        # Calce each Position using kinematicks
        self.x[0] = L1*math.cos(self.angle[0]);
        self.y[0] = L1*math.sin(self.angle[0]);
        self.x[1] = self.x[0] + L2*math.cos(self.angle[0] + self.angle[1]);
        self.y[1] = self.y[0] + L2*math.sin(self.angle[0] + self.angle[1]);
        print self.x, self.y
        self.pt_plot.set_xdata(self.x)
        self.pt_plot.set_ydata(self.y)
        #print x1,y1,x2,y2

        
