import pulp

# Data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_values = data['Y']
x_values = data['X']
K = data['K']

# Problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Variables
intercept = pulp.LpVariable('intercept', lowBound=None, cat='Continuous')
slope = pulp.LpVariable('slope', lowBound=None, cat='Continuous')

# Deviations
deviations = [pulp.LpVariable(f'dev_{i}', lowBound=0, cat='Continuous') for i in range(K)]

# Objective
problem += pulp.lpSum(deviations)

# Constraints
for i in range(K):
    problem += y_values[i] - (slope * x_values[i] + intercept) <= deviations[i]
    problem += -(y_values[i] - (slope * x_values[i] + intercept)) <= deviations[i]

# Solve
problem.solve()

# Results
result = {
    "intercept": pulp.value(intercept),
    "slope": pulp.value(slope)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')