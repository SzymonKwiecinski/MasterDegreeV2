import pulp

# Data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y = data['y']
x = data['x']
K = len(y)

# Problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Decision Variables
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')

z_plus = pulp.LpVariable.dicts('z_plus', range(K), lowBound=0, cat='Continuous')
z_minus = pulp.LpVariable.dicts('z_minus', range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(z_plus[k] + z_minus[k] for k in range(K))

# Constraints
for k in range(K):
    problem += y[k] - (c * (x[k] ** 2) + b * x[k] + a) == z_plus[k] - z_minus[k]

# Solve
problem.solve()

# Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')