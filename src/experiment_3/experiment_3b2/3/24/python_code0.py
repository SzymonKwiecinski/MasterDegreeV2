import pulp
import json

# Load data
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

# Parameters from data
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Create the LP problem
problem = pulp.LpProblem("Mining_Company_Problem", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), 0, 1, pulp.LpBinary)
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), lowBound=0)

# Objective function
problem += pulp.lpSum(
    (1 / ((1 + discount) ** (i + 1))) * (price * pulp.lpSum(amount[k, i] for k in range(n_mines)) - pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines)))
    for i in range(len(requiredquality))),
    "Total_Profit"
)

# Constraints
# 1. Limit on number of operating mines
for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork, f"Max_Working_Mines_{i}"

# 2. Limit on ore extraction
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] <= limit[k] * isoperated[k, i], f"Ore_Extraction_Limit_{k}_{i}"

# 3. Blended quality requirement
for i in range(len(requiredquality)):
    problem += pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines)) >= requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines)), f"Quality_Requirement_{i}"

# 4. Production and operation consistency
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] <= limit[k] * isoperated[k, i], f"Consistent_Production_{k}_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')