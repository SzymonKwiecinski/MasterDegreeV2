import pulp

# Data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Problem definition
problem = pulp.LpProblem("Line_Fitting_Problem", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, cat='Continuous')
D_plus = pulp.LpVariable('D_plus', lowBound=0, cat='Continuous')
D_minus = pulp.LpVariable('D_minus', lowBound=0, cat='Continuous')

# Objective function: Minimize D_plus + D_minus
problem += D_plus + D_minus

# Constraints
for k in range(data['NumObs']):
    x_k = data['X'][k]
    y_k = data['Y'][k]
    problem += y_k - (b * x_k + a) <= D_plus, f"Constraint_Positive_Deviation_{k}"
    problem += -(y_k - (b * x_k + a)) <= D_minus, f"Constraint_Negative_Deviation_{k}"

# Solve
problem.solve()

# Print solution
print(f'Optimal Intercept (a): {pulp.value(a)}')
print(f'Optimal Slope (b): {pulp.value(b)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')