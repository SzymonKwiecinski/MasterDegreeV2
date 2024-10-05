import pulp
import json

# Data input
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

# Extract data
n_mines = data["n_mines"]
n_maxwork = data["n_maxwork"]
royalty = data["royalty"]
limit = data["limit"]
quality = data["quality"]
requiredquality = data["requiredquality"]
price = data["price"]
discount = data["discount"]

n_years = len(requiredquality)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isOperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("Amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0, cat='Continuous')

# Objective function
profit_terms = []
for i in range(n_years):
    revenue = price * sum(amount[k, i] for k in range(n_mines))
    royalties = sum(royalty[k] * isoperated[k, i] for k in range(n_mines))
    discount_factor = (1 / ((1 + discount) ** i))
    profit_terms.append((revenue - royalties) * discount_factor)

profit = sum(profit_terms)
problem += profit

# Constraints
for i in range(n_years):
    problem += sum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork, f"YearMaxOperation_{i}"
    problem += sum(quality[k] * amount[k, i] for k in range(n_mines)) == requiredquality[i] * sum(amount[k, i] for k in range(n_mines)), f"QualityRequirement_{i}"

for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i], f"Limit_{k}_{i}"
        if i > 0:
            problem += isoperated[k, i] >= isoperated[k, i-1], f"OperationSequence_{k}_{i}"

# Solve the problem
problem.solve()

# Collect results
output = {
    "isoperated": [[int(isoperated[k, i].varValue) for i in range(n_years)] for k in range(n_mines)],
    "amount": [[amount[k, i].varValue for i in range(n_years)] for k in range(n_mines)]
}

# Print results
import json
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')