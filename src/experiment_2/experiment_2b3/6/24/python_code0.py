import pulp

# Parse input data
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
n_years = len(requiredquality)

# Create the problem
problem = pulp.LpProblem("Mining_Optimization_Problem", pulp.LpMaximize)

# Decision variables
is_operated = pulp.LpVariable.dicts("is_operated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0, cat='Continuous')

# Objective function
discount_factors = [(1 / ((1 + discount) ** i)) for i in range(n_years)]
revenue_terms = [
    pulp.lpSum(amount[k, i] * price for k in range(n_mines)) * discount_factors[i]
    for i in range(n_years)
]
royalty_terms = [
    pulp.lpSum(royalty[k] * is_operated[k, i] for k in range(n_mines)) * discount_factors[i]
    for i in range(n_years)
]
profit = pulp.lpSum(revenue_terms) - pulp.lpSum(royalty_terms)
problem += profit

# Constraints
for i in range(n_years):
    # Quality constraint
    problem += pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines))

    # Maximum number of mines constraint
    problem += pulp.lpSum(is_operated[k, i] for k in range(n_mines)) <= n_maxwork

    for k in range(n_mines):
        # Maximum limit constraint for each mine
        problem += amount[k, i] <= is_operated[k, i] * limit[k]

        # A mine cannot produce if it is not operated
        problem += amount[k, i] >= 0

# Solve the problem
problem.solve()

# Prepare output
output = {
    "isoperated": [[pulp.value(is_operated[k, i]) for i in range(n_years)] for k in range(n_mines)],
    "amount": [[pulp.value(amount[k, i]) for i in range(n_years)] for k in range(n_mines)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')