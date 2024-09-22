import pulp

# Define the problem
problem = pulp.LpProblem("Line_Fitting_Min_Max_Deviation", pulp.LpMinimize)

# Define the variables
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
t = pulp.LpVariable('t', lowBound=0)

# Data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Extract data values
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

# Define the objective function
problem += t, "Minimize_Max_Deviation"

# Add constraints
for k in range(num_obs):
    y_k = Y[k]
    x_k = X[k]
    
    # y_k - (b * x_k + a) <= t
    problem += y_k - (b * x_k + a) <= t, f"Constraint_Pos_{k}"
    
    # -(y_k - (b * x_k + a)) <= t --> -y_k + (b * x_k + a) <= t
    problem += -y_k + (b * x_k + a) <= t, f"Constraint_Neg_{k}"

# Solve the problem
problem.solve()

# Print the results
print(f"Optimal Intercept (a): {pulp.value(a)}")
print(f"Optimal Slope (b): {pulp.value(b)} (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")