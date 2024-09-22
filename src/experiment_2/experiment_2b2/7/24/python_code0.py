import pulp

# Define data
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

# Define constants
n_mines = data['n_mines']
n_years = len(data['requiredquality'])
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Create the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Define decision variables
is_operated = pulp.LpVariable.dicts("is_operated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0)

# Objective function: Total profit maximization
discount_factors = [(1 / ((1 + discount) ** i)) for i in range(n_years)]
profit = pulp.lpSum([(price * pulp.lpSum([amount[k, i] for k in range(n_mines)]) * discount_factors[i]) - 
                     pulp.lpSum([royalty[k] * is_operated[k, i] * discount_factors[i] for k in range(n_mines)])
                     for i in range(n_years)])
problem += profit

# Constraints
# Quality balance constraints
for i in range(n_years):
    problem += pulp.lpSum([(quality[k] * amount[k, i]) for k in range(n_mines)]) == requiredquality[i] * pulp.lpSum([amount[k, i] for k in range(n_mines)])

# Limit constraints
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * is_operated[k, i]

# Maximum operated mines constraint
for i in range(n_years):
    problem += pulp.lpSum([is_operated[k, i] for k in range(n_mines)]) <= n_maxwork

# Solve the problem
problem.solve()

# Extract the results
is_operated_solution = [[pulp.value(is_operated[k, i]) for i in range(n_years)] for k in range(n_mines)]
amount_solution = [[pulp.value(amount[k, i]) for i in range(n_years)] for k in range(n_mines)]

# Format the output
output = {
    "isoperated": is_operated_solution,
    "amount": amount_solution
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')