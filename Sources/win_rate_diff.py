import math

winrate = [0.7596, 0.5051, 0.5122, 0.5104, 0.5021, 0.5311, 0.4947, 0.5283, 0.4861, 0.5448, 0.5676, 0.5159, 0.5306, 0.5481, 0.5106] 
res = []
for i in range(len(winrate)):
    res.append(abs(winrate[i] - 0.5348))
print(res)