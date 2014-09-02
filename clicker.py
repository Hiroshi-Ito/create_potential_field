from matplotlib import pyplot as plt
from matplotlib import gridspec as gs
import numpy as np
import scipy.ndimage as ndi
import fieldMap
import csv


def grid_density_kdtree(xl, yl, xi, yi, dfactor):
    zz = np.empty([len(xi),len(yi)], dtype=np.uint8)
    zipped = zip(xl, yl)
    kdtree = KDTree(zipped)
    for xci in range(0, len(xi)):
        xc = xi[xci]
        for yci in range(0, len(yi)):
            yc = yi[yci]
            density = 0.
            retvalset = kdtree.query((xc,yc), k=5)
            for dist in retvalset[0]:
                density = density + math.exp(-dfactor * pow(dist, 2)) / 5
            zz[yci][xci] = min(density, 1.0) * 255
    return zz

def grid_density(xl, yl, xi, yi):
    ximin, ximax = min(xi), max(xi)
    yimin, yimax = min(yi), max(yi)
    xxi,yyi = np.meshgrid(xi,yi)
    #zz = np.empty_like(xxi)
    zz = np.empty([len(xi),len(yi)])
    for xci in range(0, len(xi)):
        xc = xi[xci]
        for yci in range(0, len(yi)):
            yc = yi[yci]
            density = 0.
            for i in range(0,len(xl)):
                xd = math.fabs(xl[i] - xc)
                yd = math.fabs(yl[i] - yc)
                if xd < 1 and yd < 1:
                    dist = math.sqrt(math.pow(xd, 2) + math.pow(yd, 2))
                    density = density + math.exp(-5.0 * pow(dist, 2))
            zz[yci][xci] = density
    return zz

def boxsum(img, w, h, r):
    st = [0] * (w+1) * (h+1)
    for x in xrange(w):
        st[x+1] = st[x] + img[x]
    for y in xrange(h):
        st[(y+1)*(w+1)] = st[y*(w+1)] + img[y*w]
        for x in xrange(w):
            st[(y+1)*(w+1)+(x+1)] = st[(y+1)*(w+1)+x] + st[y*(w+1)+(x+1)] - st[y*(w+1)+x] + img[y*w+x]
    for y in xrange(h):
        y0 = max(0, y - r)
        y1 = min(h, y + r + 1)
        for x in xrange(w):
            x0 = max(0, x - r)
            x1 = min(w, x + r + 1)
            img[y*w+x] = st[y0*(w+1)+x0] + st[y1*(w+1)+x1] - st[y1*(w+1)+x0] - st[y0*(w+1)+x1]

def grid_density_boxsum(x0, y0, x1, y1, w, h, data):
    kx = (w - 1) / (x1 - x0)
    ky = (h - 1) / (y1 - y0)
    r = 15
    border = r * 2
    imgw = (w + 2 * border)
    imgh = (h + 2 * border)
    img = [0] * (imgw * imgh)
    for x, y in data:
        ix = int((x - x0) * kx) + border
        iy = int((y - y0) * ky) + border
        if 0 <= ix < imgw and 0 <= iy < imgh:
            img[iy * imgw + ix] += 1
    for p in xrange(4):
        boxsum(img, imgw, imgh, r)
    a = np.array(img).reshape(imgh,imgw)
    b = a[border:(border+h),border:(border+w)]
    return b

'''''
def grid_density_gaussian_filter(x_max, y_max, data):
    kx = (x_max - 1) / (x_max)
    ky = (y_max - 1) / (y_max)
    r = 20
    border = r
    imgw = (x_max + 2 * border)
    imgh = (y_max + 2 * border)
    img = np.zeros((imgh,imgw))
    for x, y in data:
        ix = int(x * kx) + border
        iy = int(y * ky) + border
        if 0 <= ix < imgw and 0 <= iy < imgh:
            img[iy][ix] += 1
    return ndi.gaussian_filter(img, (r,r))  ## gaussian convolution


'''''
def grid_density_gaussian_filter(x_max, y_max, data):
    r = 50
    img = np.zeros((y_max, x_max))
    for x, y in data:
        x = int(x)
        y = int(y)
        if 0 < y_max and 0 < x_max:
            img[y][x] += 1
    return ndi.gaussian_filter(img, (r,r))  ## gaussian convolution



class clicker_class(object):
    def __init__(self, ax, pix_err=1):
        print "clicker init"
        self.ax = ax
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
        
        # heatmap mode
        #zd, xe, ye = np.histogram2d(yl, xl, range=[[0, self.xmax],[0, self.ymax]], normed=True)

        
        # gaussian ffilter
        zd = grid_density_gaussian_filter(self.xmax, self.ymax, self.pt_lst)

        #zd = grid_density_gaussian_filter(self.xmax, self.ymax, self.pt_lst)
        #np.savetxt("a.csv", zd, fmt="%.0f",delimiter=",")
        np.savetxt("fieldMapArray.csv", zd, delimiter=",")

        #writecsv.writerows(zd)
        self.ax.imshow(zd, origin='lower', extent=[0, self.xmax, 0, self.ymax], alpha=0.8)
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
