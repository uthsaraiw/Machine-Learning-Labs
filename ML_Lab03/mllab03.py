# -*- coding: utf-8 -*-
"""MLlab03.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f0mZgF0CdsMrd-pnehL_VVhx3PM0mrTe
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

def gauss2D(x,m,C):
 Ci=np.linalg.inv(C)
 dC=np.linalg.det(C)
 num=np.exp(-0.5 *np.dot((x-m).T,np.dot(Ci,(x-m))))
 den=2*np.pi * dC
 return num/den

def twoDGaussianPlot(m,C):
  nx=50
  ny=40
  x=np.linspace(-5,5,nx)
  y=np.linspace(-5,5,ny)
  X,Y=np.meshgrid(x,y,indexing='ij')
  Z=np.zeros([nx, ny])
  for i in range(nx):
    for j in range(ny):
      xvec=np.array([X[i,j],Y[i,j]])
      Z[i,j]=gauss2D(xvec,m,C)
  return X,Y,Z

def DrawScatterWithContours(num, m10, m11, m20, m21, c10, c11, c20, c21, c30, c31, c40, c41):
    NumDataPerClass = num
    m1 = [m10, m11]
    m2 = [m20, m21]
    C1 = [[c10, c11], [c20, c21]]
    C2 = [[c30, c31], [c40, c41]]
    A = np.linalg.cholesky(C1)
    U1 = np.random.randn(NumDataPerClass, 2)
    X1 = U1 @ A.T + m1
    U2 = np.random.randn(NumDataPerClass, 2)
    X2 = U2 @ A.T + m2

    # Create grid and multivariate normal
    x = np.linspace(-6, 10, 500)
    y = np.linspace(-6, 10, 500)
    X, Y = np.meshgrid(x, y)
    pos = np.dstack((X, Y))
    rv1 = multivariate_normal(m1, C1)
    rv2 = multivariate_normal(m2, C2)

    # Make the plot
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(X1[:, 0], X1[:, 1], c="c", s=8)
    ax.scatter(X2[:, 0], X2[:, 1], c="m", s=8)
    ax.contour(X, Y, rv1.pdf(pos), colors='blue', linewidths=1)
    ax.contour(X, Y, rv2.pdf(pos), colors='red', linewidths=1)
    ax.set_xlim(-6, 10)
    ax.set_ylim(-6, 10)
    plt.show()

def posteriorPlot(nx, ny, m1, C1, m2, C2, P1, P2):
  x = np.linspace(-5, 5, nx)
  y = np.linspace(-5, 5, ny)
  X, Y = np.meshgrid(x, y, indexing='ij')
  Z = np.zeros([nx, ny])
  for i in range(nx):
    for j in range(ny):
      xvec = np.array([X[i,j], Y[i,j]])
      num = P1*gauss2D(xvec, m1, C1)
      den = P1*gauss2D(xvec, m1, C1) + P2*gauss2D(xvec, m2, C2)
      Z[i,j] = num / den
  return X, Y, Z

def proscounter (m10,m11,m20,m21,c10,c11,c20,c21,P1,P2, c30, c31, c40, c41):
  m1=np.array([m10,m11])
  C1=np.array([[c10,c11], [c20,c21]],np.float32)
  m2=np.array([m20,m21])
  C2=np.array([[c30,c31], [c40,c41]],np.float32)

  Xp,Yp, Zp = posteriorPlot(50, 40, m1, C1, m2, C2, P1, P2)
  plt.contour(Xp,Yp, Zp,5)

DrawScatterWithContours(200,0,3,3,2.5,2,1,1,2,2,1,1,2)
proscounter (0,3,3,2.5,2,1,1,2,0.5,0.5,2,1,1,2)

DrawScatterWithContours(200,0,3,3,2.5,2,1,1,2,2,1,1,2)
proscounter (0,3,3,2.5,2,1,1,2,0.3,0.3,2,1,1,2)

DrawScatterWithContours(200,0,3,3,2.5,2,0,0,2,1.5,0,0,1.5)
proscounter (0,3,3,2.5,2,0,0,2,0.5,0.5,1.5,0,0,1.5)

#Q2, 1,2

NumDataPerClass = 200
m1 = [0,3]
m2 = [3,2.5]
C1 = C2 = [[2,1], [1,2]]
A = np.linalg.cholesky(C1)
U1 = np.random.randn(NumDataPerClass, 2)
X1 = U1 @ A.T + m1
U2 = np.random.randn(NumDataPerClass, 2)
X2 = U2 @ A.T + m2

# Create grid and multivariate normal
x = np.linspace(-6, 10, 500)
y = np.linspace(-6, 10, 500)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))
rv1 = multivariate_normal(m1, C1)
rv2 = multivariate_normal(m2, C2)

# Make the plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(X1[:, 0], X1[:, 1], c="c", s=8)
ax.scatter(X2[:, 0], X2[:, 1], c="m", s=8)
ax.contour(X, Y, rv1.pdf(pos), colors='blue', linewidths=1)
ax.contour(X, Y, rv2.pdf(pos), colors='red', linewidths=1)
ax.set_xlim(-6, 10)
ax.set_ylim(-6, 10)
plt.show()

#Q2, 3

def fisher_linear_discriminant(m1, m2, C1, C2):
    Sw = np.array(C1) + np.array(C2)
    mean_diff = np.array(m1) - np.array(m2)
    Sb = np.outer(mean_diff, mean_diff)
    eigvals, eigvecs = np.linalg.eig(np.linalg.inv(Sw).dot(Sb))
    idx = eigvals.argsort()[::-1]
    w = eigvecs[:, idx[0]]
    return w

# Given data
NumDataPerClass = 200
m1 = [0, 3]
m2 = [3, 2.5]
C1 = C2 = [[2, 1], [1, 2]]
# Compute Fisher Linear Discriminant direction
w = fisher_linear_discriminant(m1, m2, C1, C2)

# Generate data
A = np.linalg.cholesky(C1)
U1 = np.random.randn(NumDataPerClass, 2)
X1 = U1 @ A.T + m1
U2 = np.random.randn(NumDataPerClass, 2)
X2 = U2 @ A.T + m2

# Create grid and multivariate normal
x = np.linspace(-6, 10, 500)
y = np.linspace(-6, 10, 500)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))
rv1 = multivariate_normal(m1, C1)
rv2 = multivariate_normal(m2, C2)

# Make the plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(X1[:, 0], X1[:, 1], c="c", s=8)
ax.scatter(X2[:, 0], X2[:, 1], c="m", s=8)
ax.contour(X, Y, rv1.pdf(pos), colors='blue', linewidths=1)
ax.contour(X, Y, rv2.pdf(pos), colors='red', linewidths=1)

# Plot the Fisher Linear Discriminant direction
mid_point = (np.array(m1) + np.array(m2)) / 2
discriminant_line = mid_point + np.outer(x, w)
ax.plot(discriminant_line[:, 0], discriminant_line[:, 1], 'k--', label='Discriminant Direction')

ax.set_xlim(-6, 10)
ax.set_ylim(-6, 10)
ax.legend()
plt.show()

#Q2, 4

import matplotlib

Ci = np.linalg.inv(2*np.array(C1))
uF = Ci @ (np.array(m2)-np.array(m1))
yp1 = X1 @ uF
yp2 = X2 @ uF
matplotlib.rcParams.update({'font.size': 16})
plt.hist(yp1, bins=40)
plt.hist(yp2, bins=40)
plt.savefig('histogramprojections.png')

#Q2, 5

# Define a range over which to slide a threshold
#
pmin = np.min( np.array( (np.min(yp1), np.min(yp2) )))
pmax = np.max( np.array( (np.max(yp1), np.max(yp2) )))
print(pmin, pmax)
# Set up an array of thresholds
#
nRocPoints = 50;
thRange = np.linspace(pmin, pmax, nRocPoints)
ROC = np.zeros( (nRocPoints, 2) )
# Compute True Positives and False positives at each threshold
#
for i in range(len(thRange)):
  thresh = thRange[i]
  TP = len(yp2[yp2 > thresh]) * 100 / len(yp2)
  FP = len(yp1[yp1 > thresh]) * 100 / len(yp1)
  ROC[i,:] = [TP, FP]
# Plot ROC curve
#
fig, ax = plt.subplots(figsize=(6,6))
ax.plot(ROC[:,1], ROC[:,0], c='m')
ax.set_xlabel('False Positive')
ax.set_ylabel('True Positive')
ax.set_title('Receiver Operating Characteristics')
ax.grid(True)
plt.savefig('rocCurve.png')

#Q2, 6
# Sort the ROC array by FPR
ROC = ROC[ROC[:,1].argsort()]

# Compute the area under the ROC curve using numpy.trapz
roc_auc = np.trapz(ROC[:,0], ROC[:,1])

print("Area under the ROC curve: ", roc_auc)

#Q2, 7
# Define a range over which to slide a threshold
pmin = np.min(np.array((np.min(yp1), np.min(yp2))))
pmax = np.max(np.array((np.max(yp1), np.max(yp2))))
print(pmin, pmax)

# Set up an array of thresholds
nRocPoints = 50
thRange = np.linspace(pmin, pmax, nRocPoints)

# Initialize arrays to store ROC and accuracy values
ROC = np.zeros((nRocPoints, 2))
ACC = np.zeros(nRocPoints)

# Compute True Positives, False Positives, and Accuracy at each threshold
for i in range(len(thRange)):
    thresh = thRange[i]
    TP = len(yp2[yp2 > thresh]) / len(yp2)
    FP = len(yp1[yp1 > thresh]) / len(yp1)
    TN = len(yp1[yp1 <= thresh]) / len(yp1)
    FN = len(yp2[yp2 <= thresh]) / len(yp2)
    ROC[i,:] = [TP, FP]
    ACC[i] = (TP + TN) / (TP + TN + FP + FN)

# Find the threshold with the highest accuracy
max_acc_index = np.argmax(ACC)
max_acc_thresh = thRange[max_acc_index]
max_acc = ACC[max_acc_index]

print(f"Maximum accuracy of {max_acc:.2f} achieved at threshold {max_acc_thresh:.2f}")

# Plot ROC curve
fig, ax = plt.subplots(figsize=(6,6))
ax.plot(ROC[:,1], ROC[:,0], c='m')
ax.set_xlabel('False Positive')
ax.set_ylabel('True Positive')
ax.set_title('Receiver Operating Characteristics')
ax.grid(True)
plt.savefig('rocCurve.png')

# Commented out IPython magic to ensure Python compatibility.
#Q2, 8

import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
import matplotlib

def random_direction(m1, m2, C1, C2):
    # Get the dimension of the data
    dim = len(m1)

    # Generate a random vector of the same dimension
    w = np.random.rand(dim)

    return w


# Given data
NumDataPerClass = 200
m1 = [0, 3]
m2 = [3, 2.5]
C1 = C2 = [[2, 1], [1, 2]]

# Generate data
A = np.linalg.cholesky(C1)
U1 = np.random.randn(NumDataPerClass, 2)
X1 = U1 @ A.T + m1
U2 = np.random.randn(NumDataPerClass, 2)
X2 = U2 @ A.T + m2

Ci = np.linalg.inv(2*np.array(C1))
uF = Ci @ (np.array(m2)-np.array(m1))
yp1 = X1 @ uF
yp2 = X2 @ uF
# Define a range over which to slide a threshold
#
pmin1 = np.min( np.array( (np.min(X1), np.min(X2) )))
pmax1 = np.max( np.array( (np.max(X1), np.max(X2) )))
# Set up an array of thresholds
#
nRocPoints1 = 50;
thRange1 = np.linspace(pmin1, pmax1, nRocPoints1)
ROC1 = np.zeros( (nRocPoints1, 2) )
# Compute True Positives and False positives at each threshold
#
for i in range(len(thRange1)):
  thresh1 = thRange1[i]
  TP1 = len(X2[X2 > thresh1]) * 100 / len(X2)
  FP1 = len(X1[X1 > thresh1]) * 100 / len(X1)
  ROC1[i,:] = [TP1, FP1]


# Define a range over which to slide a threshold
#
pmin = np.min( np.array( (np.min(yp1), np.min(yp2) )))
pmax = np.max( np.array( (np.max(yp1), np.max(yp2) )))
# Set up an array of thresholds
#
nRocPoints = 50;
thRange = np.linspace(pmin, pmax, nRocPoints)
ROC = np.zeros( (nRocPoints, 2) )


for i in range(len(thRange)):
  thresh = thRange[i]
  TP = len(yp2[yp2 > thresh]) * 100 / len(yp2)
  FP = len(yp1[yp1 > thresh]) * 100 / len(yp1)
  ROC[i,:] = [TP, FP]

# Plot ROC curve
#
fig, ax = plt.subplots(figsize=(6,6))
ax.plot(ROC1[:,1], ROC1[:,0], c='m')
ax.plot(ROC[:,1], ROC[:,0], c='m')
ax.set_xlabel('False Positive')
ax.set_ylabel('True Positive')
ax.set_title('Receiver Operating Characteristics')
ax.grid(True)
plt.savefig('rocCurve.png')

#Q3

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

# Generate some example data
np.random.seed(0)
class1 = np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]], 100)
class2 = np.random.multivariate_normal([1, 2], [[2, 0], [0, 2]], 100)

# Compute the means of the two classes
mean1 = np.mean(class1, axis=0)
mean2 = np.mean(class2, axis=0)

# Compute the covariance matrices of the two classes
cov1 = np.cov(class1.T)
cov2 = np.cov(class2.T)

# Define a new data point
x = np.array([0.5, 1])

# Compute the Euclidean distances to the means
dist1_euclidean = distance.euclidean(x, mean1)
dist2_euclidean = distance.euclidean(x, mean2)

# Compute the Mahalanobis distances to the means
dist1_mahalanobis = distance.mahalanobis(x, mean1, np.linalg.inv(cov1))
dist2_mahalanobis = distance.mahalanobis(x, mean2, np.linalg.inv(cov2))

print(f"Euclidean distances: {dist1_euclidean}, {dist2_euclidean}")
print(f"Mahalanobis distances: {dist1_mahalanobis}, {dist2_mahalanobis}")