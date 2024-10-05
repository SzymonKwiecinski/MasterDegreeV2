import pulp

# Load the data
data = {
    'NumObs': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Number of observations
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

# Create the problem
problem = pulp.LpProblem("Minimize_Maximum_Deviation", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
D = pulp.LpVariable('D', lowBound=0, cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(num_obs)]

# Objective function
problem += D, "Minimize_Max_Deviation"

# Constraints
for k in range(num_obs):
    # d_k >= y_k - (b*x_k + a)
    problem += d[k] >= Y[k] - (b * X[k] + a), f"Constraint_Upper_{k}"
    # d_k >= -(y_k - (b*x_k + a))
    problem += d[k] >= -(Y[k] - (b * X[k] + a)), f"Constraint_Lower_{k}"
    # D >= d_k
    problem += D >= d[k], f"Max_Deviation_Constraint_{k}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')