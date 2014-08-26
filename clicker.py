from matplotlib import pyplot as plt
import numpy as np

class clicker_class(object):
    def __init__(self, ax, pix_err=1):
        print "clicker init"
        self.canvas = ax.get_figure().canvas
        self.cid = None
        self.pt_lst = []
        self.pt_plot = ax.plot([], [], marker='o',linestyle='none', zorder=5)[0]
        self.pix_err = pix_err
        self.connect_sf()

    def set_visible(self, visible):
        print "set_visible"
        '''sets if the curves are visible '''
        self.pt_plot.set_visible(visible)

    def clear(self):
        print "clear"
        '''Clears the points'''
        self.pt_lst = []
        self.redraw()

    def connect_sf(self):
        print "connect_sf"
        if self.cid is None:
            self.cid = self.canvas.mpl_connect('button_press_event',
                                               self.click_event)

    def disconnect_sf(self):
        print "disconnect_sf"
        if self.cid is not None:
            self.canvas.mpl_disconnect(self.cid)
            self.cid = None

    def click_event(self, event):
        print "click_event"
        ''' Extracts locations from the user'''
        if event.key == 'shift':
            self.pt_lst = []
            return
        if event.xdata is None or event.ydata is None:
            return
        if event.button == 1:
            if len(self.pt_lst) < 2:
                self.pt_lst.append((event.xdata, event.ydata))
            else:
                self.pt_lst.pop(0)
                self.pt_lst.append((event.xdata, event.ydata))
        elif event.button == 3:
            self.remove_pt((event.xdata, event.ydata))

        self.redraw()


    def remove_pt(self, loc):
        print "remove_pt"
        if len(self.pt_lst) > 0:
            self.pt_lst.pop(np.argmin(map(lambda x:
                                          np.sqrt((x[0] - loc[0]) ** 2 +
                                                  (x[1] - loc[1]) ** 2),
                                                  self.pt_lst)))

    def redraw(self):
        print "redraw"
        if len(self.pt_lst) > 0:
            x, y = zip(*self.pt_lst)
        else:
            x, y = [], []
        #print x,y
        if(len(x) > 1):
            print x,y,x[0],x[1]
            #ax.arrow(x[0],y[0],x[1]-x[0],y[1]-y[0],  fc="k", ec="k", head_width=10, head_length=20)
            #ax.quiver(x[0],y[0],x[1]-x[0],y[1]-y[0] ,angles='xy',scale_units='xy',scale=1)
        self.pt_plot.set_xdata(x)
        self.pt_plot.set_ydata(y)
        self.canvas.draw()

    def return_points(self):
        print "return points"
        '''Returns the clicked points in the format the rest of the
        code expects'''
        return np.vstack(self.pt_lst).T
