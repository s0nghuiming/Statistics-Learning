import numpy as np
import matplotlib.pyplot as plt

global gw
global gb
global depth
global x
global y
# xt is the transposition of x. only used by pylib.
x = [ [3,3], [4,3], [1,1] ]
y = [ +1,    +1,    -1 ]
xt = list(zip(*x))
gw = None
gb = None
depth = 0
if len(x[0]):
    depth = len(x[0])

def initwb(w=[], b=0):
    # if len(w) < depth: fill 0
    # if len(w) = depth: ok
    # if len(w) > depth: cut w.
    global gw, gb, depth
    lenw = len(w)
    if lenw == 0:
        gw = [0] * depth
    else:
        if lenw < depth:
            gw = w[:]
            gw.extend([0]*(depth-lenw))
        elif lenw >= depth:
            gw = w[:depth]
    gb = b

'''
loss <= 0, wrongly classified
loss >0  , successfully classfied.
'''
def loss(i, w, b):
    global depth,x,y
    res = 0;
    assert len(x[i]) == depth, "Length of testdatum isn't equal to "+str(depth)
    res = np.multiply( y[i], np.dot(x[i],w)+b )
    return res

'''
update w,b using i-th data.
para1: i, index of data.
para2: w, matrix w with deep $depth$
para3: b, value of b
para4: eta, eta
'''
def updatewb(i, w, b, eta):
    global x, y, gw, gb
    res = None
    eta = 1
    gw = list(np.add( w, np.multiply(y[i], x[i]) ))
    gb = b + y[i]
    return (gw, gb)

'''
looking through all test data for a misclassified one. If found return the index;
if not return -1.
'''
def misclassified(w, b):
    res = -1
    for i in range(len(x)):
        if loss(i, w, b) <= 0:
            res = i
            break
    return res

def prtmodel():
    print("w is", gw, "; b is", gb, ".")


if __name__ == "__main__":
    initwb()
    loop = 100
    while loop >= 0:
        loop = loop - 1
        prtmodel()
        indx = misclassified(gw, gb)
        if indx != -1:
            #print("Index", indx, "is found.")
            updatewb(indx, gw, gb, 1)
        else:
            print("no misclassified data found!")
            break

'''
# pylot draws graph.
plt.figure(figsize=(6,6))
plt.plot( xt[0], xt[1], 'go', label='Test Data' )
plt.xlabel("$x^{(1)}$")
plt.ylabel("$x^{(2)}$")
plt.title("Machine Learning: Perceptron 1")
plt.xlim(0,5)
plt.ylim(-1,4)
ax = plt.gca()
ax.set_aspect(1)
plt.legend()
plt.show()
'''
