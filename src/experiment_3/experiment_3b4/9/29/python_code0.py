import pulp

# Data from the JSON
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Model parameters
intercept_value = None
slope_value = None

# Unpack data
K = data['NumObs']
y = data['Y']
x = data['X']

# Create a new LP problem
problem = pulp.LpProblem("Minimize_Max_Absolute_Deviation", pulp.LpMinimize)

# Decision variables
t = pulp.LpVariable('t', lowBound=0, cat='Continuous')  # Minimize this
b = pulp.LpVariable('b', cat='Continuous')             # Slope
a = pulp.LpVariable('a', cat='Continuous')             # Intercept

# Objective function
problem += t

# Constraints
for k in range(K):
    problem += y[k] - (b * x[k] + a) <= t
    problem += -(y[k] - (b * x[k] + a)) <= t

# Solve the problem
problem.solve()

# Print the value of the objective function
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')