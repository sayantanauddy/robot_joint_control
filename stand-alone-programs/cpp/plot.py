#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

with open("output.txt") as f:
    data = f.read()

data = data.split('\n')

print data
print type(data)
print np.shape(data)
data = data[0:499]

t = [row.split(' ')[0] for row in data]
x1 = [row.split(' ')[1] for row in data]
x2 = [row.split(' ')[2] for row in data]

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Plot title...")    
ax1.set_xlabel('your x label..')
ax1.set_ylabel('your y label...')

ax1.plot(t,x1, c='r', label='the data')
ax1.plot(t,x2, c='b', label='the data')

leg = ax1.legend()

plt.show()
