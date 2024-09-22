import pulp
import json

# Input data
data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0],
        'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5],
        'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}

# Parameters
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
isoperated = pulp.LpVariable.dicts("isoperated", (range(n_mines), range(len(requiredquality))), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(n_mines), range(len(requiredquality))), lowBound=0)

# Objective Function: Maximize profit
profit = pulp.lpSum(
    (price * pulp.lpSum(amount[k][i] for k in range(n_mines)) - 
     pulp.lpSum(royalty[k] * isoperated[k][i] for k in range(n_mines))) / ((1 + discount) ** i)
    for i in range(len(requiredquality))
)
problem += profit

# Constraints
# Quality blending constraint
for i in range(len(requiredquality)):
    problem += pulp.lpSum((quality[k] * amount[k][i] for k in range(n_mines))) == requiredquality[i] * pulp.lpSum(amount[k][i] for k in range(n_mines))

# Ore limit constraint
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k][i] <= limit[k] * isoperated[k][i]

# Max work constraint
for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork

# Solve the problem
problem.solve()

# Output results
isoperated_result = [[isoperated[k][i].varValue for i in range(len(requiredquality))] for k in range(n_mines)]
amount_result = [[amount[k][i].varValue for i in range(len(requiredquality))] for k in range(n_mines)]

output = {
    "isoperated": isoperated_result,
    "amount": amount_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')