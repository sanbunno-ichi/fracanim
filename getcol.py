import numpy as np
import math

def get_color(alpha):
    shift = 0.0
    color = np.empty((3,), np.float32)
    color[0] = (np.cos((alpha*2.0-1.0+shift)*np.pi) + 1.0)
    color[1] = (np.cos((alpha*2.0-0.75+shift)*np.pi) + 1.0)
    color[2] = (np.cos((alpha*2.0-0.5+shift)*np.pi) + 1.0)

    return (color*(0.5*255)).astype(np.float32)


def show_color_gradient(color_func):
    import matplotlib.pyplot as plt
    from PIL import Image
    
    maxcol = 400
    colors = np.empty((maxcol,3))
    for i in range(maxcol):
        colors[i] = color_func(i/maxcol)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim([0,maxcol])
    ax.plot(colors[:,0],'r',label='R')
    ax.plot(colors[:,1],'g',label='G')
    ax.plot(colors[:,2],'b',label='B')
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    ax.imshow(np.tile(colors/255, (255,1,1)), extent=[*xlim, *ylim])
    plt.show()


density = 0.35
for y in range(1,255):
	alpha = y * 0.05 * density
	alpha = math.log(alpha+1)

	col = get_color( alpha )
	
	c0 = int(col[0])
	c1 = int(col[1])
	c2 = int(col[2])

	#print(c0,c1,c2)
	
	if(c0 > 255):
		c0 = 255
	if(c1 > 255):
		c1 = 255
	if(c2 > 255):
		c2 = 255
	
	coldata = c0*0x10000 + c1*0x100 + c2
	print(hex(coldata))

#show_color_gradient(get_color)
