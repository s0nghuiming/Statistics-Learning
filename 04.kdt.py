import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import copy
import math
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

"""
X,  feature vectors
Y,  class of X
D,  dimension of each of vectors.
"""

# Construct initial to be classified data
D   = 2
NUM = 50
C = [ 'g', 'r', 'b' ]
#X = np.array([ (3,5), (2,4), (1,1), (5,2), (1,5), (4,1) ])
X = np.random.rand(NUM,D)
Y = [ C[i] for i in np.random.randint(0,len(C),NUM) ]

class KD_Node:
    cur_trav = None             # cursor for traversal.
    x_min = 0
    x_max = 1
    y_min = 0
    y_max = 1

    def __init__( self,
                  point=None, split=None, color=None,
                  L=None, R=None, father=None,
                  scope={} ):
        """
        initiate a kd tree.
        point: datum of this node
        split: split plane for this node
        L:     left son
        R:     right son
        father: father of this node, if root it's None
        scope: area in hyperspace for each node.
        """
        self.point  = point
        self.split  = split
        self.color  = color
        self.left   = L
        self.right  = R
        self.father = father
        self.flag_trav = 0      # traversal flag. 
                                #   bit 0 is notation for itself
                                #   bit 1 is for its left son
                                #   bit 2 is for its right son
        self.scope = scope      # paint scope:
                                #   x0: min of x
                                #   x1: max of x
                                #   y0: min of y
                                #   y1: max of y

    def clear_trav(self):
        KD_Node.cur_trav = None
        self.flag_trav = 0
        if self.left:
            self.left.clear_trav()
        if self.right:
            self.right.clear_trav()

    def __iter__(self):
        return self

    def __next__(self):
        # with non-iteration traverse the tree
        cursor = None
        if KD_Node.cur_trav == None:        # First time to use cur_trav, initiate.
            KD_Node.cur_trav = self

        cursor = KD_Node.cur_trav
        while 1:
            if cursor.flag_trav & 0X07 == 0X7:      # any node has flag with
                                                    # value=3 
                                                    # that states a completion
                                                    # of traversal.
                if cursor.father == None:
                    raise StopIteration
                else:
                    cursor = cursor.father

            elif cursor.flag_trav & 0X01 == 0:      # if bit0 == 0,
                cursor.flag_trav |= 0X01            # set bit0 = 1
                #cursor = cursor            # not need. set cursor => self
                break                               # BREAK! return current.

            elif cursor.flag_trav & 0X02 == 0:      # if bit1==0, bit2==0
                cursor.flag_trav |= 0X02            # set bit1 of self
                if cursor.left != None:
                    cursor = cursor.left            # set cursor => left son
                else:                               # self.left is None, skip
                    continue

            elif cursor.flag_trav & 0X04 == 0:      # if bit2 == 0,
                cursor.flag_trav |= 0X04            # set bit2 = 1
                if cursor.right != None:
                    cursor = cursor.right           # set cursor => right son
                else:
                    continue
        KD_Node.cur_trav = cursor

        return KD_Node.cur_trav


def CreateKDT(node=None, data=None, color=None, father=None ):
    """
    TODO: DOC FOR CreateKDT
    INPUT: node, the node itself?
           data, [ (3,5), (2,4), (1,1) ]
           father, the father
    OUTPUT: 
    """
    global C
    if len(data) > 0:
        global D
        dim = D
        var = np.var(data, axis=0)          # variance for each dimension
        split = np.argmax(var)              # split for this node
        pos = int(len(data)/2)
        pos_list = np.argpartition(data[:,split], pos)
        point = data[pos_list[pos]]         # point for this node
        color = C[np.random.randint(0, len(C))]
        cur_scope = {}                      # scope

        if not father:
            cur_scope = { 'x0': 0, 'x1': 6, # current scope is where the node is.
                          'y0': 0, 'y1': 6 }# Or you can assign it the min and
                                            # max of the graph.
        else:                               # update cur_scope
            cur_scope = copy.deepcopy(father.scope)
            if father.split == 0:
                if point[0] < father.point[0]:
                    cur_scope['x1'] = father.point[0]
                else:
                    cur_scope['x0'] = father.point[0]
            elif father.split == 1:
                if point[1] < father.point[1]:
                    cur_scope['y1'] = father.point[1]
                else:
                    cur_scope['y0'] = father.point[1]                

        node = KD_Node( point=point, split=split, color=color, father=father,
                        scope=cur_scope )

        if len(data[pos_list[:pos]]) != 0:
            node.left  = CreateKDT( node    = node.left,
                                    data    = data[pos_list[:pos]],
                                    color   = color,
                                    father  = node )

        if len(data[pos_list[(pos+1):]]) != 0:
            node.right = CreateKDT( node    = node.right,
                                    data    = data[pos_list[(pos+1):]],
                                    color   = color,
                                    father  = node )

    return node

def get_split_pos(data, split):
    """return the position to split in data."""
    pos = len(data)/2
    return 

def preorder(node, depth=-1):
    """
    Preorder a KD node
    """
    print(node)
    if node:
        if node.left:
            preorder(node.left)
        if node.right:
            preorder(node.right)

def draw_KDT(kd):
    """
    Draw a plot in which each of data determined by a point and draw the classifying plane.
    """
    x_min = kd.x_min
    x_max = kd.x_max
    y_min = kd.y_min
    y_max = kd.y_max
    plt.figure(figsize=(6,6))
    plt.xlabel("$x^{(1)}$")
    plt.ylabel("$x^{(2)}$")
    plt.title("Machine Learning: KD Tree")
    plt.xlim(int(x_min),math.ceil(x_max))
    plt.ylim(int(y_min),math.ceil(y_max))
    ax = plt.gca()
    ax.set_aspect(1)

    plt.plot( [x_min, x_max, x_max, x_min, x_min],
              [y_min, y_min, y_max, y_max, y_min] )

    line_from = []              # split line from and to
    line_to   = []

    for node in kd:
        if node.split == 0:
            line_from = [ node.point[0], node.scope['y0'] ]
            line_to   = [ node.point[0], node.scope['y1'] ]
        if node.split == 1:
            line_from = [ node.scope['x0'], node.point[1] ]
            line_to   = [ node.scope['x1'], node.point[1] ]

        plt.plot( [ line_from[0], line_to[0] ],
                  [ line_from[1], line_to[1] ],
                  'k-', linewidth=1 )
        plt.scatter( node.point[0], node.point[1], color=node.color )

    plt.show()
    pass


def find_knn(root, x):
    pass


def main():
    kd = None
    kd = CreateKDT(kd, X)

    #kd.clear_trav()
    draw_KDT(kd)


if __name__ == "__main__":
    main()

