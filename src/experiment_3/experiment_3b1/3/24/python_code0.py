import pulp
import json

data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
I = len(requiredquality)  # number of years

# Create a LP problem
problem = pulp.LpProblem("Mining_Company_Optimization", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum((price * pulp.lpSum(amount[k, i] for k in range(n_mines)) / ((1 + discount) ** (i + 1)) - 
                       pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines))) 
                       for i in range(I)), "Total_Profit"

# Constraints

# 1. Operating Limits
for i in range(I):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork, f"Operating_Limit_{i}"

# 2. Production Amounts
for k in range(n_mines):
    for i in range(I):
        problem += amount[k, i] <= limit[k] * isoperated[k, i], f"Production_Amount_{k}_{i}"

# 3. Blending Constraint
for i in range(I):
    problem += pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[j, i] for j in range(n_mines)), f"Blending_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')