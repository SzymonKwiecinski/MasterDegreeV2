import pulp

# Data from the provided JSON
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

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Create the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), lowBound=0)
y = pulp.LpVariable.dicts("y", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), cat='Binary')

# Objective function
profit = pulp.lpSum((price * pulp.lpSum(x[k, i] for k in range(n_mines)) - pulp.lpSum(royalty[k] * y[k, i] for k in range(n_mines))) / ((1 + discount) ** (i + 1)) for i in range(len(requiredquality)))
problem += profit

# Constraints
# Maximum number of mines operated in any one year
for i in range(len(requiredquality)):
    problem += pulp.lpSum(y[k, i] for k in range(n_mines)) <= n_maxwork

# Extraction limit from each mine
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += x[k, i] <= limit[k] * y[k, i]

# Quality constraint
for i in range(len(requiredquality)):
    problem += pulp.lpSum(x[k, i] * quality[k] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(x[k, i] for k in range(n_mines))

# Operation order constraint
for k in range(n_mines):
    for i in range(1, len(requiredquality)):
        problem += y[k, i] <= y[k, i - 1]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')