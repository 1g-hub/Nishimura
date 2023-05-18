import matplotlib.pyplot as plt
import math
'''
func = [[0.48065, 0.93551],[0.58931, 0.87517], [0.61306, 0.81873],[0.63388,0.76593],[0.63948, 0.71653], [0.67287,0.67032],[0.70441,0.62709],[0.68373,0.58665],[0.76859,0.54881],[0.77283, 0.51342], [0.76269, 0.48031], [0.80783, 0.44933],[0.81026, 0.42035],[0.8261,0.3932]]
function1 = [i[0] for i in func]
function2 = [i[1] for i in func]
print(function1)
print(function2)
plt.xlabel('Fitness (Number of Changed Card)', fontsize=15)
plt.ylabel('Fitness (Win Rate)', fontsize=15)
plt.scatter(function2, function1, c = "blue")
'''
'''
func = [[1.2333, 0], [1.1233, 1], [0.9512, 2], [0.8042999999999999, 3], [0.7386999999999999, 4], [0.6859999999999999, 5], [0.6407999999999999, 6], [0.6028, 7], [0.5503, 8], [0.4812999999999999, 9], [0.4701, 10], [0.4261000000000001, 11], [0.33369999999999994, 12], [0.29309999999999997, 13], [0.28429999999999994, 14], [0.2819, 17], [0.2757, 18], [0.25199999999999995, 21], [0.24420000000000003, 31], [0.2358999999999999, 33], [0.23449999999999988, 41]]
function1 = [math.exp(-i[0]) for i in func]
function2 = [math.exp(-i[1]/100) for i in func]
#print(function1)
#print(function2)
plt.xlabel('Fitness (Magnitude of Changes)', fontsize=15)
plt.ylabel('Fitness (Win Rate)', fontsize=15)
plt.scatter(function2, function1, c = "red")

function1 = 0.85146
function2 = 0.44933
plt.scatter(function2, function1, c = "green")

#func = [[0.7330, 10], [0.5288, 15],[0.4893, 15], [0.4559, 23], [0.4471, 31], [0.3962, 36], [0.3504, 41], [0.3802, 35], [0.2632, 43], [0.2577, 47], [0.2709, 66], [0.2134, 63], [0.2104, 51], [0.1910,65]]
func = [[0.2134, 63],[0.2104, 51], [0.1910,65]]
function1 = [math.exp(-i[0]) for i in func]
function2 = [math.exp(-i[1]/100) for i in func]
print(function1)
print(function2)
plt.scatter(function2, function1, c = "blue")
'''
'''
func = [[0.23449999999999988, 41]]
function1 = [math.exp(-i[0]) for i in func]
function2 = [math.exp(-i[1]/100) for i in func]
print(function1)
print(function2)
plt.xlabel('Fitness (Number of change)', fontsize=15)
plt.ylabel('Fitness (Win Rate)', fontsize=15)
plt.scatter(function2, function1, c = "red")

function1 = 0.85146
function2 = 0.44933
plt.scatter(function2, function1, c = "green")

func = [[0.2134, 63]]
function1 = [math.exp(-i[0]) for i in func]
function2 = [math.exp(-i[1]/100) for i in func]
plt.scatter(function2, function1, c = "blue")
'''
'''
func = [[0.23449999999999988, 0.4204]]
function1 = [math.exp(-i[0]) for i in func]
function2 = [i[1] for i in func]
#print(function1)
#print(function2)
plt.xlabel('Fitness (Number of Changed Card)', fontsize=15)
plt.ylabel('Fitness (Win Rate)', fontsize=15)
plt.scatter(function2, function1, c = "red")

function1 = 0.85146
function2 = 0.36788
plt.scatter(function2, function1, c = "green")

#func = [[0.7330, 10], [0.5288, 15],[0.4893, 15], [0.4559, 23], [0.4471, 31], [0.3962, 36], [0.3504, 41], [0.3802, 35], [0.2632, 43], [0.2577, 47], [0.2709, 66], [0.2134, 63], [0.2104, 51], [0.1910,65]]
func = [[0.2134, 0.4493],[0.2104, 0.4204], [0.1910,0.3932]]
function1 = [math.exp(-i[0]) for i in func]
function2 = [i[1]for i in func]
print(function1)
print(function2)
plt.scatter(function2, function1, c = "blue")
'''

'''
#単目的 GA
fp1 = 0.44933
fw1 = 0.85146
fc1 = 0.36788
#多目的 GA
fp2 = 0.66365
fw2 = 0.79097
fc2 = 0.42035
#提案手法
fp3 = 0.53259
fw3 = 0.80783
fc3 = 0.44933

plt.xlabel('Fitness (Number of Changed Card)', fontsize=15)
plt.ylabel('Fitness (Win Rate)', fontsize=15)

plt.scatter(fc1, fw1, c="green")
plt.scatter(fc2, fw2, c="red")
plt.scatter(fc3, fw3, c="blue")
'''


func = [[1.2318, 0, 0], [1.1162, 1, 1], [0.9655, 2, 2], [0.7845, 3, 3], [0.7175, 4, 4], [0.6829000000000001, 5, 4], [0.63, 6, 5], [0.5124000000000001, 7, 6], [0.3101999999999999, 8, 6], [0.29370000000000007, 9, 7], [0.27919999999999995, 13, 8], [0.263, 15, 8], [0.25550000000000006, 20, 9], [0.2492999999999999, 21, 9], [0.24079999999999996, 23, 9], [0.2294, 30, 11], [0.20699999999999996, 31, 10], [0.2046, 32, 11], [0.19679999999999997, 33, 11], [0.181, 40, 12], [0.18020000000000003, 43, 12], [0.17230000000000006, 44, 13]]
function1 = [math.exp(-i[0]) for i in func]
function2 = [math.exp(-i[1]/100) for i in func]
#print(function1)
#print(function2)
plt.xlabel('Fitness (Magnitude of Changes)', fontsize=15)
plt.ylabel('Fitness (Win Rate)', fontsize=15)
plt.scatter(function2, function1, c = "red")

function1 = 0.85146
function2 = 0.44933
plt.scatter(function2, function1, c = "green")

func = [[0.7330, 10], [0.5288, 15],[0.4893, 15], [0.4559, 23], [0.4471, 31], [0.3962, 36], [0.3504, 41], [0.3802, 35], [0.2632, 43], [0.2577, 47], [0.2709, 66], [0.2134, 63], [0.2104, 51], [0.1910,65]]
function1 = [math.exp(-i[0]) for i in func]
function2 = [math.exp(-i[1]/100) for i in func]
plt.scatter(function2, function1, c = "blue")

func = [[1.2277, 0, 0], [1.1122, 1, 1], [1.0223, 2, 1], [0.9772000000000001, 3, 1], [0.9435, 4, 1], [0.8566, 5, 1], [0.8138, 7, 1], [0.9571000000000001, 2, 2], [0.8742, 3, 2], [0.8138, 4, 2], [0.7841, 5, 2], [0.6958000000000001, 6, 2], [0.6645, 8, 2], [0.5769, 9, 2], [0.5683999999999999, 10, 2], [0.7606999999999999, 4, 3], [0.7098, 5, 3], [0.5955, 7, 3], [0.4905, 10, 3], [0.59, 5, 4], [0.5312, 8, 4], [0.45609999999999995, 9, 4], [0.45299999999999996, 14, 4], [0.44909999999999994, 16, 4], [0.43339999999999995, 18, 4], [0.4764, 6, 5], [0.43840000000000007, 11, 5], [0.38829999999999987, 12, 5], [0.30870000000000003, 14, 5], [0.45849999999999996, 7, 6], [0.4348000000000001, 8, 6], [0.3404, 12, 6], [0.2994000000000001, 14, 6], [0.35609999999999997, 9, 7], [0.33729999999999993, 10, 7], [0.31789999999999996, 11, 7], [0.3006, 13, 7], [0.28830000000000006, 17, 7], [0.2862, 21, 7], [0.29200000000000004, 16, 8], [0.27209999999999995, 17, 8], [0.2682, 18, 8], [0.2624, 19, 9], [0.2555, 20, 9], [0.28630000000000005, 14, 10], [0.2549, 23, 10], [0.25149999999999995, 24, 10], [0.2476000000000001, 26, 10], [0.23540000000000005, 24, 11]]

function1 = [math.exp(-i[0]) for i in func]
function2 = [math.exp(-i[1]/100) for i in func]

plt.scatter(function2, function1, c = "black")


plt.savefig("fwfp_reall.png", format="png", dpi=300)