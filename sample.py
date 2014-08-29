from matplotlib import pyplot as plt

def on_key(event):
    print('you pressed', event.key, event.xdata, event.ydata)

fig = plt.figure()
cid = fig.canvas.mpl_connect("key_press_event", on_key)
plt.show()
