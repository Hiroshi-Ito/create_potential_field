from matplotlib import pyplot as plt
from matplotlib import gridspec as gs
import numpy as np
import clicker
import arm
import fieldMap

plt.figure(num=None, figsize=(8, 6), dpi=100, facecolor='w', edgecolor='k')
gs = gs.GridSpec(2, 4)
gs.update(left=0.05, right=0.98, hspace=0.3)


houseMap = plt.subplot(gs[:, :-1])

# plot potential field
#plt.imshow(heatmap, extent=[0, ymax, 0, xmax], alpha=1)
#plt.axvspan(300, 400, facecolor='r', alpha=0.5)



leftArm = plt.subplot(gs[:-1, -1])
leftArm.axis('scaled')
plt.xticks(np.arange(0,80,20))
plt.xlim(0,80)
plt.ylim(-80,80)
leftArm.set_title('leftArm')

rightArm = plt.subplot(gs[-1, -1])
rightArm.axis('scaled')
plt.xticks(np.arange(0,80,20))
plt.xlim(0,80)
plt.ylim(-80,80)
rightArm.set_title('rightArm')

#fig = houseMap.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')


cc = clicker.clicker_class(houseMap)
#fm = fieldMap.field_class(houseMap)
larm = arm.arm_class(leftArm)
rarm = arm.arm_class(rightArm)

#larm.calc_invkinematicks(x=0, y=72)
#rarm.calc_invkinematicks(x=72, y=0)


plt.show()
