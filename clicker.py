from matplotlib import pyplot as plt
from matplotlib import gridspec as gs
import numpy as np
import fieldMap


def get_ax_size(ax):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height


class clicker_class(object):
    def __init__(self, ax, pix_err=1):
        print "clicker init"
        self.ax = ax
        self.ax.set_title('BMI house layout at experiment room')
        im = plt.imread("map.png");
        self.xmax, self.ymax = im.shape[:2]
        self.ax.imshow(im, extent=[0, self.ymax, 0, self.xmax])
        self.ax.grid(True)
        self.ax.autoscale(False)

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
            self.cid = self.canvas.mpl_connect('button_press_event', self.click_event)
            self.cid = self.canvas.mpl_connect('key_press_event', self.on_key)
            #self.cid = self.canvas.mpl_connect()


    def disconnect_sf(self):
        print "disconnect_sf"
        if self.cid is not None:
            self.canvas.mpl_disconnect(self.cid)
            self.cid = None


    def on_key(self, event):
        print event.key
        if event.key == 'escape':
            print 'escape, try to plot potential field'
            self.plot_field_map()
        if event.key == 'backspace':
            print "clear all dots"
            self.clear()


    def plot_field_map(self):
        print "plot_field"
        #print self.pt_lst
        xl, yl = zip(*self.pt_lst)
        #print(get_ax_size(self.ax))
        #print self.ax.im.shape
        #zd, xe, ye = np.histogram2d(yl, xl, range=[[0, 467],[0, 807]], bins=1,normed=True)
        #zd, xe, ye = np.histogram2d(yl, xl)
        zd, xe, ye = np.histogram2d(yl, xl, range=[[0, self.xmax],[0, self.ymax]], normed=True)
        self.ax.imshow(zd, origin='lower',extent=[0, self.ymax, 0, self.xmax],alpha=0.8)
        self.canvas.draw()
        #print zd
        #plot_field_map(zd)
        #field_map.canvas.draw()
        #plt.imshow(zd, origin='lower')



    def click_event(self, event):
        print "click_event", event.key, event.button
        ''' Extracts locations from the user'''
        if event.key == 'shift':
            print "Press shift"
            self.pt_lst = []
            return
        if event.xdata is None or event.ydata is None:
            return
        if event.button == 1:
            if len(self.pt_lst) < 2:
                self.pt_lst.append((event.xdata, event.ydata))
            else:
                #self.pt_lst.pop(0)
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
        #if(len(x) > 1):
            #print x,y,x[0],x[1]
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
