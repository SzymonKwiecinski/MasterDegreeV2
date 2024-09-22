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

# Set problem constants
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
required_quality = data['requiredquality']
price = data['price']
discount = data['discount']
years = len(required_quality)

# Setup the optimization problem
problem = pulp.LpProblem("Mining_Problem", pulp.LpMaximize)

# Decision variables
isoperated = [[pulp.LpVariable(f'isoperated_{k}_{i}', cat='Binary') for i in range(years)] for k in range(n_mines)]
amount = [[pulp.LpVariable(f'amount_{k}_{i}', lowBound=0, upBound=limit[k]) for i in range(years)] for k in range(n_mines)]

# Objective Function: Maximize discounted profit over all years
profit = sum([(price * pulp.lpSum(amount[k][i] for k in range(n_mines)) - pulp.lpSum(royalty[k] * isoperated[k][i] for k in range(n_mines))) / ((1 + discount) ** i) for i in range(years)])
problem += profit

# Constraints
for i in range(years):
    # Max number of mines operated constraint
    problem += pulp.lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork
    # Quality constraint
    problem += pulp.lpSum(quality[k] * amount[k][i] for k in range(n_mines)) == required_quality[i] * pulp.lpSum(amount[k][i] for k in range(n_mines))
    for k in range(n_mines):
        # Amount can only be produced if the mine is operated
        problem += amount[k][i] <= limit[k] * isoperated[k][i]

# Solve the problem
problem.solve()

# Extract results
output = {
    "isoperated": [[int(pulp.value(isoperated[k][i])) for i in range(years)] for k in range(n_mines)],
    "amount": [[pulp.value(amount[k][i]) for i in range(years)] for k in range(n_mines)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')