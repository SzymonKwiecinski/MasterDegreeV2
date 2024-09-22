import pulp
import json

# Input data
data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 
        'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 
        'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Create the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), 0, 1, pulp.LpBinary)
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), 0)

# Objective Function
profit = pulp.lpSum(price * amount[k, i] for k in range(n_mines) for i in range(len(requiredquality))) \
         - pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines) for i in range(len(requiredquality)))
problem += profit

# Constraints
# 1. Blending quality requirement
for i in range(len(requiredquality)):
    problem += pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines))

# 2. Limits on each mine
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# 3. Max number of mines operated each year
for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

# Solve the problem
problem.solve()

# Collecting results
isoperated_result = [[pulp.value(isoperated[k, i]) for i in range(len(requiredquality))] for k in range(n_mines)]
amount_result = [[pulp.value(amount[k, i]) for i in range(len(requiredquality))] for k in range(n_mines)]

# Output results
output = {
    "isoperated": isoperated_result,
    "amount": amount_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')