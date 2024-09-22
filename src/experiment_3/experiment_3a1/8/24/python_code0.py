import pulp
import json

# Given data in JSON format
data_json = '''{
    "n_mines": 4,
    "n_maxwork": 3,
    "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    "quality": [1.0, 0.7, 1.5, 0.5],
    "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0],
    "price": 10,
    "discount": 0.1
}'''
data = json.loads(data_json)

# Parameters
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
I = len(requiredquality)

# Problem Definition
problem = pulp.LpProblem("Mining_Company_Optimization", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(I)), lowBound=0)

# Objective Function
profit = pulp.lpSum([((amount[k, i] * price) - (royalty[k] * isoperated[k, i])) * (1 + discount) ** -i for k in range(n_mines) for i in range(I)])
problem += profit, "Total_Profit"

# Constraints
# Operation Limits
for i in range(I):
    problem += pulp.lpSum([isoperated[k, i] for k in range(n_mines)]) <= n_maxwork, f"Max_Operations_Year_{i}"

# Ore Production Limits
for k in range(n_mines):
    for i in range(I):
        problem += amount[k, i] <= limit[k] * isoperated[k, i], f"Ore_Production_Limit_mine_{k}_year_{i}"

# Quality Constraints
for i in range(I):
    problem += pulp.lpSum([quality[k] * amount[k, i] for k in range(n_mines)]) == requiredquality[i] * pulp.lpSum([amount[k, i] for k in range(n_mines)]), f"Quality_Constraint_year_{i}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')