import pulp

# Data
data = {
    'n_mines': 4,
    'n_maxwork': 3,
    'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    'quality': [1.0, 0.7, 1.5, 0.5],
    'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0],
    'price': 10,
    'discount': 0.1
}

# Sets
K = range(data['n_mines'])
I = range(len(data['requiredquality']))

# Problem
problem = pulp.LpProblem("Mine_Operation", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, i) for k in K for i in I), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, i) for k in K for i in I), cat='Binary')

# Objective Function
objective = pulp.lpSum(
    (1 / (1 + data['discount'])**(i + 1)) * (
        data['price'] * pulp.lpSum(x[k, i] for k in K) - 
        pulp.lpSum(data['royalty'][k] * y[k, i] for k in K)
    ) 
    for i in I
)
problem += objective

# Constraints

# Ore quality constraint for each year
for i in I:
    problem += pulp.lpSum(data['quality'][k] * x[k, i] for k in K) == data['requiredquality'][i] * pulp.lpSum(x[k, i] for k in K)

# Mine operation and production link
for k in K:
    for i in I:
        problem += x[k, i] <= data['limit'][k] * y[k, i]

# Maximum number of mines operated in a year
for i in I:
    problem += pulp.lpSum(y[k, i] for k in K) <= data['n_maxwork']

# Solving the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')