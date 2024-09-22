import pulp

# Provided data
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

# Extract parameters
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

# Create the LP problem
problem = pulp.LpProblem("Mining_Operation", pulp.LpMaximize)

# Decision variables
is_operated = pulp.LpVariable.dicts("IsOperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("Amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0)

# Objective: Maximize profit
objective = 0
for i in range(n_years):
    revenue = pulp.lpSum(amount[k, i] * price for k in range(n_mines)) / ((1 + discount) ** i)
    cost = pulp.lpSum(royalty[k] * is_operated[k, i] for k in range(n_mines)) / ((1 + discount) ** i)
    objective += revenue - cost

problem += objective

# Constraints

# Quality constraint
for i in range(n_years):
    problem += (
        pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) ==
        requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines))
    )

# Max mines operated constraint
for i in range(n_years):
    problem += pulp.lpSum(is_operated[k, i] for k in range(n_mines)) <= n_maxwork

# Amount limits
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * is_operated[k, i]

# Ensure binary operation for mines based on future royalties
for k in range(n_mines):
    for i in range(1, n_years):
        problem += is_operated[k, i] <= is_operated[k, i-1]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "isoperated": [[int(pulp.value(is_operated[k, i])) for i in range(n_years)] for k in range(n_mines)],
    "amount": [[pulp.value(amount[k, i]) for i in range(n_years)] for k in range(n_mines)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')