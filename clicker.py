from matplotlib import pyplot as plt
from matplotlib import gridspec as gs
import numpy as np
import scipy.ndimage as ndi

arm_trj = [[ 0 , -72 ],[ 6 , -71 ],[ 13 , -70 ],[ 19 , -69 ],[ 25 , -67 ],[ 30 , -65 ],
            [ 36 , -62 ],[ 41 , -59 ],[ 46 , -55 ],[ 51 , -50 ],[ 55 , -46 ],[ 59 , -41 ],
            [ 62 , -36 ],[ 65 , -30 ],[ 68 , -23 ],[ 70 , -16 ],[ 71 , -11 ],[ 72 , 0 ]
            ]



def grid_density_gaussian_filter(x_max, y_max, data):
    r = 30
    img = np.zeros((y_max, x_max))
    for x, y in data:
        x = int(x)
        y = int(y)
        if 0 < y_max and 0 < x_max:
            img[y][x] += 1
    return ndi.gaussian_filter(img, (r,r))  ## gaussian convolution



class clicker_class(object):
    def __init__(self, ax, larm, rarm ):
        self.mode = 0
        self.map = []
        print "clicker init"
        self.ax = ax

        self.larm = larm
        self.rarm = rarm
        self.larm.calc_invkinematicks(y=-72, x=0)
        self.rarm.calc_invkinematicks(x=72, y=0)

        self.ax.set_title('BMI house layout at experiment room')
        im = plt.imread("map.png");
        self.ymax, self.xmax = im.shape[:2]
        self.ax.imshow(im, extent=[0, self.xmax, 0, self.ymax])
        self.ax.grid(True)
        self.ax.autoscale(False)

        self.canvas = ax.get_figure().canvas
        self.cid = None
        self.pt_lst = []
        self.pt_plot = ax.plot([], [], marker='o',linestyle='none', zorder=5)[0]
        #self.pix_err = pix_err
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
        self.mode = 1


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

        # heatmap mode
        #zd, xe, ye = np.histogram2d(yl, xl, range=[[0, self.xmax],[0, self.ymax]], normed=True)


        # gaussian ffilter
        self.map = grid_density_gaussian_filter(self.xmax, self.ymax, self.pt_lst)

        #zd = grid_density_gaussian_filter(self.xmax, self.ymax, self.pt_lst)
        #np.savetxt("a.csv", zd, fmt="%.0f",delimiter=",")
        np.savetxt("fieldMapArray.csv", self.map*100000, fmt="%.00f", delimiter=",")

        #writecsv.writerows(zd)
        self.ax.imshow(self.map, origin='lower', extent=[0, self.xmax, 0, self.ymax], alpha=0.3)
        #np.savetxt("imshow.csv", a, fmt="%.0f",delimiter=",")
        self.canvas.draw()


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
                if self.mode == 1:
                    self.pt_lst.pop(0)
                    self.pt_lst.append((event.xdata, event.ydata))
                    self.arm_angle()

                else:
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



    def arm_angle(self):
        xl, yl = self.pt_lst[1]
        max_num = np.amax(self.map)
        raito = self.map[yl][xl] / max_num
        desired_pos = int(round(17 * raito, 0))
        #print desired_pos
        x, y = arm_trj[desired_pos]
        print "target_position : ", x, y
        self.larm.calc_invkinematicks(x, y)
        #print raito, desired_pos
