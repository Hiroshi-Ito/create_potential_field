from matplotlib import pyplot as plt
from matplotlib import gridspec as gs
import numpy as np
import clicker
import arm

plt.figure(num=None, figsize=(8, 6), dpi=100, facecolor='w', edgecolor='k')
gs = gs.GridSpec(2, 4)
gs.update(left=0.05, right=0.98, hspace=0.3)


houseMap = plt.subplot(gs[:, :-1])
houseMap.set_title('BMI house layout at experiment room')
im = plt.imread("map.png");
xmax, ymax = im.shape[:2]
plt.imshow(im, extent=[0, ymax, 0, xmax])
plt.grid(True)
houseMap.autoscale(False)

# plot potential field
#plt.imshow(heatmap, extent=[0, ymax, 0, xmax], alpha=1)
#plt.axvspan(300, 400, facecolor='r', alpha=0.5)



leftArm = plt.subplot(gs[:-1, -1])
plt.axis('scaled')
plt.xticks(np.arange(0,80,20))
plt.xlim(0,80)
plt.ylim(-80,80)
leftArm.set_title('leftArm')

rightArm = plt.subplot(gs[-1, -1])
plt.axis('scaled')
plt.xticks(np.arange(0,80,20))
plt.xlim(0,80)
plt.ylim(-80,80)
rightArm.set_title('rightArm')

#fig = houseMap.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')


cc = clicker.clicker_class(houseMap)
larm = arm.arm_class(leftArm)
rarm = arm.arm_class(rightArm)

#larm.calc_invkinematicks(x=0, y=72)
#rarm.calc_invkinematicks(x=72, y=0)


plt.show()
