import pulp

# Data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Define the LP problem
problem = pulp.LpProblem("Linear_Regression_MinMax_Deviation", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', lowBound=None)  # Intercept
b = pulp.LpVariable('b', lowBound=None)  # Slope
D = pulp.LpVariable('D', lowBound=0)     # Maximum deviation

# Objective function
problem += D, "Minimize_Max_Deviation"

# Constraints
for k in range(data['NumObs']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    # Constraints for each observation
    problem += y_k - b * x_k - a <= D, f"Pos_Deviation_{k}"
    problem += -b * x_k - a + y_k <= D, f"Neg_Deviation_{k}"

# Solve the problem
problem.solve()

# Results
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')
print(f'Maximum Deviation (D): {pulp.value(D)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')