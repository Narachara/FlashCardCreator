import numpy as np


def closest(lst, K):
     # find the item in lst which is closest to K
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
     return lst[idx]

threshold = 5
spaces = [3, 7, 11, 18, 24, 29, 34, 45, 50, 55, 59, 67, 70, 75, 80, 84, 90, 93, 97, 108]
out = []

for i in range(37,444,37):
  ret = closest(spaces, i)
  if abs(ret-i) <= threshold:
    out.append(ret)


print(out)