import pulp

# Data from the problem
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Create a Linear Programming problem
problem = pulp.LpProblem("Line_Fitting", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
M = pulp.LpVariable('M', lowBound=0, upBound=None, cat='Continuous')

# Objective Function
problem += M, "Minimize_Maximum_Deviation"

# Constraints
for k in range(data['NumObs']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    # y_k - (b * x_k + a) <= M
    problem += y_k - (b * x_k + a) <= M, f"Upper_Deviation_Constraint_{k}"
    # -(y_k - (b * x_k + a)) <= M
    problem += -(y_k - (b * x_k + a)) <= M, f"Lower_Deviation_Constraint_{k}"

# Solve the problem
problem.solve()

# Results
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')