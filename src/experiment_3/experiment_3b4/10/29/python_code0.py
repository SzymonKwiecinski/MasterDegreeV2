import pulp

# Data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=-1e3, upBound=1e3)
b = pulp.LpVariable('b', lowBound=-1e3, upBound=1e3)
d = pulp.LpVariable('d', lowBound=0)

# Objective
problem += d, "Objective"

# Constraints
for k in range(data['NumObs']):
    x_k = data['X'][k]
    y_k = data['Y'][k]
    problem += (y_k - (b * x_k + a)) <= d, f"Constraint_Upper_{k}"
    problem += ((b * x_k + a) - y_k) <= d, f"Constraint_Lower_{k}"

# Solve
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')