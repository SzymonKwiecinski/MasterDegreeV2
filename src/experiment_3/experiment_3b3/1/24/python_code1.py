import pulp
import json

# Load data
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

# Extract data
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

# Define problem
problem = pulp.LpProblem("Mining_Operations", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat=pulp.LpBinary)
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(
    price * amount[k, i] * (1 + discount)**(-i) - royalty[k] * isoperated[k, i]
    for k in range(n_mines)
    for i in range(n_years)
)

# Constraints
# Mining Operations Limit
for i in range(n_years):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

# Quality Requirement
for i in range(n_years):
    total_amount = pulp.lpSum(amount[k, i] for k in range(n_mines))
    problem += (pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines)) >= requiredquality[i] * total_amount)
    problem += (total_amount > 0)  # Ensure we do not divide by zero

# Ore Extraction Limit
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Solve problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')