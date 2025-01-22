import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import numpy as np
from sys import argv

plot = False # make it True only for testing purpose

try:
    # l and d are in nm when provided through argv
    n, d, n_az = [int(a) for a in argv[1:]]
    # print(n, d, n_az)
except:
    n = 9 # number of VDCCs in a cluster
    d = 100 # AZ-VDCC coupling distance (in nm)
    n_az = 9 # number of active zones


# AZ distribution
x0 = 0   #nm
y0 = 0    #nm
xs = 250   #nm
az_x = 500 #nm
az_y = 400 #nm


# 35 points in hexagonal grid
shift = d/np.sqrt(2)
pos = [ [shift + x0,           shift + y0       ],
        [shift + x0-az_x,      shift + y0       ],
        [shift + x0+az_x,      shift + y0       ],
        [shift + x0-xs,        shift + y0-az_y  ],
        [shift + x0+xs,        shift + y0+az_y  ],
        [shift + x0-xs,        shift + y0+az_y  ],
        [shift + x0+xs,        shift + y0-az_y  ],
        [shift + x0-2*az_x,    shift + y0       ],
        [shift + x0+2*az_x,    shift + y0       ],
        [shift + x0-az_x-xs,   shift + y0-az_y  ],
        [shift + x0+az_x+xs,   shift + y0+az_y  ],
        [shift + x0+az_x+xs,   shift + y0-az_y  ],
        [shift + x0-az_x-xs,   shift + y0+az_y  ],
        [shift + x0,           shift + y0-2*az_y],
        [shift + x0,           shift + y0+2*az_y],
        [shift + x0-az_x,      shift + y0-2*az_y],
        [shift + x0+az_x,      shift + y0+2*az_y],
        [shift + x0-az_x,      shift + y0+2*az_y],
        [shift + x0+az_x,      shift + y0-2*az_y],
        [shift + x0-3*az_x,    shift + y0       ],
        [shift + x0+3*az_x,    shift + y0       ],
        [shift + x0-2*az_x-xs, shift + y0-az_y  ],
        [shift + x0+2*az_x+xs, shift + y0+az_y  ],
        [shift + x0-2*az_x-xs, shift + y0+az_y  ],
        [shift + x0+2*az_x+xs, shift + y0-az_y  ],
        [shift + x0-2*az_x,    shift + y0-2*az_y],
        [shift + x0+2*az_x,    shift + y0+2*az_y],
        [shift + x0-2*az_x,    shift + y0+2*az_y],
        [shift + x0+2*az_x,    shift + y0-2*az_y],
        [shift + x0-3*az_x,    shift + y0-2*az_y],
        [shift + x0+3*az_x,    shift + y0+2*az_y],
        [shift + x0-3*az_x,    shift + y0+2*az_y],
        [shift + x0+3*az_x,    shift + y0-2*az_y],
        [shift + x0-3*az_x-xs, shift + y0+az_y  ],
        [shift + x0+3*az_x+xs, shift + y0-az_y  ]
      ]

azpos = [ [x0,           y0       ],
          [x0-az_x,      y0       ],
          [x0+az_x,      y0       ],
          [x0-xs,        y0-az_y  ],
          [x0+xs,        y0+az_y  ],
          [x0-xs,        y0+az_y  ],
          [x0+xs,        y0-az_y  ],
          [x0-2*az_x,    y0       ],
          [x0+2*az_x,    y0       ],
          [x0-az_x-xs,   y0-az_y  ],
          [x0+az_x+xs,   y0+az_y  ],
          [x0+az_x+xs,   y0-az_y  ],
          [x0-az_x-xs,   y0+az_y  ],
          [x0,           y0-2*az_y],
          [x0,           y0+2*az_y],
          [x0-az_x,      y0-2*az_y],
          [x0+az_x,      y0+2*az_y],
          [x0-az_x,      y0+2*az_y],
          [x0+az_x,      y0-2*az_y],
          [x0-3*az_x,    y0       ],
          [x0+3*az_x,    y0       ],
          [x0-2*az_x-xs, y0-az_y  ],
          [x0+2*az_x+xs, y0+az_y  ],
          [x0-2*az_x-xs, y0+az_y  ],
          [x0+2*az_x+xs, y0-az_y  ],
          [x0-2*az_x,    y0-2*az_y],
          [x0+2*az_x,    y0+2*az_y],
          [x0-2*az_x,    y0+2*az_y],
          [x0+2*az_x,    y0-2*az_y],
          [x0-3*az_x,    y0-2*az_y],
          [x0+3*az_x,    y0+2*az_y],
          [x0-3*az_x,    y0+2*az_y],
          [x0+3*az_x,    y0-2*az_y],
          [x0-3*az_x-xs, y0+az_y  ],
          [x0+3*az_x+xs, y0-az_y  ]
      ]

vdcc_loc = {
    '1': [[0,0]],
    '2': [[-3.5,3.5], [3.5,-3.5]],
    '3': [[-9,3], [3,-9], [6,6]],
    '4': [[5,0], [-5,0], [0,5], [0,-5]],
    '5': [[0,0], [7,7], [-7,-7], [-7,7], [7,-7]],
    '6': [[0,10], [0,-10], [9,5], [-9,-5], [-9,5], [9,-5]],
    '7': [[0,0], [0,10], [0,-10], [9,5], [-9,-5], [-9,5], [9,-5]],
    '8': [[5,0], [-5,0], [0,5], [0,-5], [6,6], [-6,-6], [-6,6], [6,-6]],
    '9': [[0,0], [10,0], [-10,0], [0,10], [0,-10], [10,10], [-10,-10], [-10,10], [10,-10]],
    '10': [[10,0], [-10,0], [0,10], [0,-10], [10,10], [-10,-10], [-10,10], [10,-10], [-3.3,-3.3], [3.3,3.3]],
    '11': [[10,0], [-10,0], [0,10], [0,-10], [10,10], [-10,-10], [-10,10], [10,-10], [-4,-4], [-4,4], [4,4]],
    '12': [[10,0], [-10,0], [0,10], [0,-10], [10,10], [-10,-10], [-10,10], [10,-10], [-4,-4], [-4,4], [4,-4], [4,4]],
    '13': [[0,0], [10,0], [-10,0], [0,10], [0,-10], [10,10], [-10,-10], [-10,10], [10,-10], [-5,-5], [-5,5], [5,-5], [5,5]],
    '14': [[3, 3], [3.3, 10], [-3, -3], [3.3, -10], [10, 3.3], [10, 10], [10, -3.3], [10, -10], 
           [-3.3, 10], [-3.3, -10], [-10, 3.3], [-10, 10], [-10, -3.3], [-10, -10]],
    '15': [[3.3, 3.3], [3.3, 10], [1.5, -3.3], [3.3, -10], [10, 3.3], [10, 10], [10, -3.3], [10, -10], [-3.3, 1.5], 
           [-3.3, 10], [-3.3, -10], [-10, 3.3], [-10, 10], [-10, -3.3], [-10, -10]],
    '16': [[3.3, 3.3], [3.3, 10], [3.3, -3.3], [3.3, -10], [10, 3.3], [10, 10], [10, -3.3], [10, -10], [-3.3, 3.3], 
           [-3.3, 10], [-3.3, -3.3], [-3.3, -10], [-10, 3.3], [-10, 10], [-10, -3.3], [-10, -10]],
}

start = '''vdcc_disk RELEASE_SITE {
    SHAPE = LIST
    MOLECULE_POSITIONS {'''
end = '''
    }
    SITE_RADIUS = 0.010
}
'''

mid = ''


f, ax = plt.subplots(1)
for i,p in enumerate(pos[:n_az]):
    loc = np.array(vdcc_loc[str(n)], dtype="float64").T

    #print('\n\n',p,'\n',loc)
    loc[0] += p[0]
    loc[1] += p[1]
    #print(loc)
    for xy in zip(loc[0], loc[1]):
        mid += "\n\t\tVDCC_C0' [{0:0.3f}, {1:0.3f}, 0.0]".format(xy[0]/1000, xy[1]/1000)

    if plot:
        ax.scatter(loc[0], loc[1],marker='.')
        plt.gca().add_patch(Circle((azpos[i]),100, fill=False))

if plot:
    az_size = 100 # nm
    for p in azpos[:n_az]:
        plt.gca().add_patch(Rectangle((p[0]-az_size/2, p[1]-az_size/2), az_size, az_size)) 


        #print mid
        ax.set_xticks(np.linspace(-1500,1500,31))
        ax.set_yticks(np.linspace(-1000,1000,21))
        ax.set_aspect(1.0)
        plt.grid()
        
    plt.show()

## Save VDCC disk to file
fname = f"vdcc_disk_n{n}_d{d}_nAZ{n_az}.mdl"
print(fname)
with open(fname, 'w') as f: f.write(start + mid + end)
