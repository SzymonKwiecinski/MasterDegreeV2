import pulp

# Data from JSON
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

# Constants
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
years = len(requiredquality)

# Problem
problem = pulp.LpProblem("MiningOperations", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts(
    "isoperated", 
    ((k, i) for k in range(n_mines) for i in range(years)), 
    cat=pulp.LpBinary
)
amount = pulp.LpVariable.dicts(
    "amount", 
    ((k, i) for k in range(n_mines) for i in range(years)), 
    lowBound=0
)

# Objective Function
problem += pulp.lpSum(
    (price * pulp.lpSum(amount[(k, i)] for k in range(n_mines)) / (1 + discount) ** i) -
    pulp.lpSum(royalty[k] * isoperated[(k, i)] for k in range(n_mines))
    for i in range(years)
)

# Constraints
# 1. Mine Operation Constraint
for i in range(years):
    problem += pulp.lpSum(isoperated[(k, i)] for k in range(n_mines)) <= n_maxwork

# 2. Ore Production Limits
for k in range(n_mines):
    for i in range(years):
        problem += amount[(k, i)] <= limit[k] * isoperated[(k, i)]

# 3. Quality Constraint
for i in range(years):
    total_amount = pulp.lpSum(amount[(k, i)] for k in range(n_mines))
    problem += (pulp.lpSum(quality[k] * amount[(k, i)] for k in range(n_mines)) == 
                requiredquality[i] * total_amount)

# Solve the problem
problem.solve()

# Extracting the results
output = {
    "isoperated": [[pulp.value(isoperated[(k, i)]) for i in range(years)] for k in range(n_mines)],
    "amount": [[pulp.value(amount[(k, i)]) for i in range(years)] for k in range(n_mines)]
}

# Print Output and Objective Value
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')