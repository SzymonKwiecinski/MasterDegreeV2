import pulp
import json

# Given data
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), lowBound=0)
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), cat='Binary')

# Objective function
problem += pulp.lpSum(
    (price * (pulp.lpSum(amount[k, i] for k in range(n_mines)) - pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines)))) / ((1 + discount) ** i)
    for i in range(len(requiredquality))
), "Total_Profit"

# Constraints
for i in range(len(requiredquality)):
    problem += pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines)), f"Quality_Constraint_{i}"

for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] <= limit[k] * isoperated[k, i], f"Limit_Constraint_{k}_{i}"

for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork, f"Max_Work_Constraint_{i}"

for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] >= 0, f"Non_Negativity_Constraint_{k}_{i}"

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')