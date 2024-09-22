import pulp

# Data from JSON
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

# Create a problem instance
problem = pulp.LpProblem("Fit_Line", pulp.LpMinimize)

# Declare variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
D = pulp.LpVariable('D', lowBound=0, cat='Continuous')

# Objective function
problem += D, "Minimize maximum deviation"

# Constraints
for k in range(num_obs):
    y_k = Y[k]
    x_k = X[k]
    problem += y_k - (b * x_k + a) <= D, f"Constraint_upper_{k}"
    problem += -(y_k - (b * x_k + a)) <= D, f"Constraint_lower_{k}"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')