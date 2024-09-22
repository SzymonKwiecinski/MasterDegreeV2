import pulp
import json

# Input data
data = {
    'n_mines': 4,
    'n_maxwork': 3,
    'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    'quality': [1.0, 0.7, 1.5, 0.5],
    'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0],
    'price': 10,
    'discount': 0.1
}

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", 
                                    ((k, i) for k in range(n_mines) for i in range(len(requiredquality))),
                                    cat='Binary')

amount = pulp.LpVariable.dicts("amount", 
                                ((k, i) for k in range(n_mines) for i in range(len(requiredquality))),
                                lowBound=0)

# Objective Function
profit = pulp.lpSum((amount[k, i] * price - royalty[k] * isoperated[k, i]) * 
                    (1 / ((1 + discount) ** (i + 1))) for k in range(n_mines) for i in range(len(requiredquality)))

problem += profit

# Constraints
# Required quality constraint
for i in range(len(requiredquality)):
    problem += (
        pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) ==
        requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines))
    )

# Maximum work constraint
for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

# Production limit constraint
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Solve the problem
problem.solve()

# Output results
isoperated_output = [[pulp.value(isoperated[k, i]) for i in range(len(requiredquality))] for k in range(n_mines)]
amount_output = [[pulp.value(amount[k, i]) for i in range(len(requiredquality))] for k in range(n_mines)]

result = {
    "isoperated": isoperated_output,
    "amount": amount_output
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')