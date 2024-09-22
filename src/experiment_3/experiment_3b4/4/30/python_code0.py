import pulp

# Data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

K = len(data['y'])
y = data['y']
x = data['x']

# Create a LP Minimization problem
problem = pulp.LpProblem("Minimize_Error_Sum", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('a', lowBound=None)  # a can be any real number
b = pulp.LpVariable('b', lowBound=None)  # b can be any real number
c = pulp.LpVariable('c', lowBound=None)  # c can be any real number
e_plus = pulp.LpVariable.dicts("e_plus", range(K), lowBound=0)
e_minus = pulp.LpVariable.dicts("e_minus", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum([e_plus[k] + e_minus[k] for k in range(K)])

# Constraints
for k in range(K):
    problem += y[k] == c * x[k]**2 + b * x[k] + a + e_plus[k] - e_minus[k], f"constraint_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')