import numpy as np
import cv2
from matplotlib import pyplot as plt


def CatmullRomSpline(P0, P1, P2, P3, nPoints=100):
  """
  P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
  nPoints is the number of points to include in this curve segment.
  """
  # Convert the points to np so that we can do array multiplication
  P0, P1, P2, P3 = map(np.array, [P0, P1, P2, P3])

  # Calculate t0 to t4
  alpha = 0.5
  def tj(ti, Pi, Pj):
    xi, yi = Pi
    xj, yj = Pj
    return ( ( (xj-xi)**2 + (yj-yi)**2 )**0.5 )**alpha + ti

  t0 = 0
  t1 = tj(t0, P0, P1)
  t2 = tj(t1, P1, P2)
  t3 = tj(t2, P2, P3)

  # Only calculate points between P1 and P2
  t = np.linspace(t1,t2,nPoints)

  # Reshape so that we can multiply by the points P0 to P3
  # and get a point for each value of t.
  t = t.reshape(len(t),1)

  A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
  A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
  A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

  B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
  B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

  C  = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
  return C

def CatmullRomChain(P):
  """
  Calculate Catmull Rom for a chain of points and return the combined curve.
  """
  sz = len(P)

  # The curve C will contain an array of (x,y) points.
  C = []
  for i in range(sz-3):
    c = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3])
    C.extend(c)

  return C

# Define a set of points for curve to go through
# The first and the last points are neighbors of the end points of the set.
# The order in which points appear in the sequence matters.
Points = [[24,24],[25,25],[125,125],[250,25],[251,25]]

# Calculate the Catmull-Rom splines through the points
c = CatmullRomChain(Points)
image = np.zeros((400,400,3),np.uint8)
cv2.imshow('',image)
cv2.waitKey(0)
# Convert the Catmull-Rom curve points into x and y arrays and plot
x,y = zip(*c)
x_ = np.asarray(x,np.int32)
y_ = np.asarray(y,np.int32)
# print(x)
for i,j in zip(range(0,len(x)),range(0,len(y))):
    cv2.circle(image,(x_[i],y_[j]),2,(220,220,220),-1)
    print('ha!')

# cv2.circle(image,(px[0],py[0]),2,(220,220,220),-1)

cv2.imshow('',image)
cv2.waitKey(0)
plt.plot(x,y)

# Plot the control points
px, py = zip(*Points)
plt.plot(px,py,'or')

plt.show()