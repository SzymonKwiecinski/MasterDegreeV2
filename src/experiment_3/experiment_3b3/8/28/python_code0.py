import pulp

# Data
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Problem
problem = pulp.LpProblem("Linear_Regression", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')  # Intercept
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')  # Slope

u = [pulp.LpVariable(f'u_{k}', lowBound=0, cat='Continuous') for k in range(data['K'])]
v = [pulp.LpVariable(f'v_{k}', lowBound=0, cat='Continuous') for k in range(data['K'])]

# Objective Function
problem += pulp.lpSum([u[k] + v[k] for k in range(data['K'])]), "Total_Absolute_Deviation"

# Constraints
for k in range(data['K']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    
    # y_k - (b*x_k + a) <= u_k
    problem += y_k - (b*x_k + a) <= u[k], f"Upper_Bound_{k}"
    
    # -(y_k - (b*x_k + a)) <= v_k
    problem += -(y_k - (b*x_k + a)) <= v[k], f"Lower_Bound_{k}"

# Solve the problem
problem.solve()

# Output
intercept = pulp.value(a)
slope = pulp.value(b)

output = {
    "intercept": intercept,
    "slope": slope
}

# Print the output and objective value
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')