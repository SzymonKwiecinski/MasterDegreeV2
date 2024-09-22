import pulp
import json

# Load data from JSON format
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
I = len(requiredquality)  # Number of years

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(I)), lowBound=0)

# Objective Function
profit = pulp.lpSum(
    (pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) * price 
     - pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines)) 
     - pulp.lpSum(amount[k, i] * discount for k in range(n_mines))) * (1 + discount) ** (-i)
    for i in range(I)
)
problem += profit

# Constraints

# Maximum number of mines operated per year
for i in range(I):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

# Limit on ore extraction
for k in range(n_mines):
    for i in range(I):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Quality constraint for blended ore
for i in range(I):
    total_amount = pulp.lpSum(amount[k, i] for k in range(n_mines))
    problem += (total_amount > 0) >> (pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) / total_amount == requiredquality[i])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')