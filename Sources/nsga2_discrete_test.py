from nsga2_problem import Problem
from nsga2_evolution import Evolution
import matplotlib.pyplot as plt

#配列の和
def f1(x):
    sum = 0
    for i in x:
        sum += i
    return sum

#配列の同じ要素数
def f2(x):
    same_sum = len(x) - len(set(x))
    return same_sum


problem = Problem(num_of_variables=5, objectives=[f1, f2], variables_range=[(1, 5)], expand= False)
evo = Evolution(problem)
evol = evo.evolve()
func = [i.objectives for i in evol]
ans_list = [i.features for i in evol]
print("func")
print(func)
print("ans_list")
print(ans_list)
function1 = [i[0] for i in func]
function2 = [i[1] for i in func]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.savefig("nsga2.png", format="png", dpi=300)