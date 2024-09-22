import pulp

# Data
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

K = data['K']
Y = data['Y']
X = data['X']

# LP Problem
problem = pulp.LpProblem("Line_Fitting", pulp.LpMinimize)

# Decision Variables
b = pulp.LpVariable('b', lowBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, cat='Continuous')
u = pulp.LpVariable.dicts('u', range(K), lowBound=0, cat='Continuous')
v = pulp.LpVariable.dicts('v', range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([u[k] + v[k] for k in range(K)]), "Total_Deviation"

# Constraints
for k in range(K):
    problem += Y[k] - b * X[k] - a <= u[k], f"Deviation_Constraint_Positive_{k}"
    problem += -b * X[k] - a + Y[k] <= v[k], f"Deviation_Constraint_Negative_{k}"

# Solve
problem.solve()

# Output Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')