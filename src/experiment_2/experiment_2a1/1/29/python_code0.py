import json
import pulp

data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create the problem variable
problem = pulp.LpProblem("Fit_Best_Straight_Line", pulp.LpMinimize)

# Variables for slope (b) and intercept (a)
b = pulp.LpVariable('b', lowBound=None)  # slope
a = pulp.LpVariable('a', lowBound=None)  # intercept

# Deviations variables
deviations = [pulp.LpVariable(f'dev_{i}', lowBound=0) for i in range(data['NumObs'])]

# Objective function: minimize the maximum deviation
problem += pulp.lpSum(deviations)

# Constraints for each observation
for i in range(data['NumObs']):
    problem += deviations[i] >= data['Y'][i] - (b * data['X'][i] + a)
    problem += deviations[i] >= -(data['Y'][i] - (b * data['X'][i] + a))

# Solve the problem
problem.solve()

intercept = pulp.value(a)
slope = pulp.value(b)

print(f' (Intercept): <INTERCEPT>{intercept}</INTERCEPT>')
print(f' (Slope): <SLOPE>{slope}</SLOPE>')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')