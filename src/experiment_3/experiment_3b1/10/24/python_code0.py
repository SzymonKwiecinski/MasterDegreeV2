import pulp
import json

# Data provided in JSON format
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

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

# Create the problem
problem = pulp.LpProblem("Mining_Operations_Profit_Maximization", pulp.LpMaximize)

# Variables
isoperated = pulp.LpVariable.dicts("isoperated", (range(n_mines), range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(n_mines), range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(
    (price * pulp.lpSum(amount[k][i] for k in range(n_mines)) / ((1 + discount)**(i + 1)) - 
    pulp.lpSum(royalty[k] * isoperated[k][i] for k in range(n_mines))) 
    for i in range(I)
)

# Constraints

# Operating Mines Limit
for i in range(I):
    problem += pulp.lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork

# Quality Constraint
for i in range(I):
    problem += pulp.lpSum(quality[k] * amount[k][i] for k in range(n_mines)) == requiredquality[i] * \
               pulp.lpSum(amount[k][i] for k in range(n_mines))

# Production Limits
for k in range(n_mines):
    for i in range(I):
        problem += amount[k][i] <= limit[k] * isoperated[k][i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')