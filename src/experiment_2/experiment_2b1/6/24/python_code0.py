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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), 0, 1, pulp.LpBinary)
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), 0)

# Objective function
revenue = pulp.lpSum([price * amount[(k, i)] for k in range(n_mines) for i in range(len(requiredquality))])
royalty_cost = pulp.lpSum([royalty[k] * pulp.lpSum([isoperated[(k, i)] for i in range(len(requiredquality))]) for k in range(n_mines)])
discounted_revenue = pulp.lpSum([revenue / (1 + discount) ** i for i in range(len(requiredquality))])
problem += discounted_revenue - royalty_cost, "Total_Profit"

# Constraints
for i in range(len(requiredquality)):
    problem += pulp.lpSum([amount[(k, i)] * quality[k] for k in range(n_mines)]) == requiredquality[i], f"Quality_Requirement_{i}"

for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[(k, i)] <= limit[k] * isoperated[(k, i)], f"Limit_Constraint_{k}_{i}"

for i in range(len(requiredquality)):
    problem += pulp.lpSum([isoperated[(k, i)] for k in range(n_mines)]) <= n_maxwork, f"Max_Work_Constraint_{i}"

# Solve the problem
problem.solve()

# Output results
isoperated_result = [[pulp.value(isoperated[(k, i)]) for i in range(len(requiredquality))] for k in range(n_mines)]
amount_result = [[pulp.value(amount[(k, i)]) for i in range(len(requiredquality))] for k in range(n_mines)]

output = {
    "isoperated": isoperated_result,
    "amount": amount_result
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')