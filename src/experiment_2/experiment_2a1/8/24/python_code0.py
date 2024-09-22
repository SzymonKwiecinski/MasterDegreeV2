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

# Create the model
prob = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))),
                                     cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))),
                                 lowBound=0)

# Objective function
profit_terms = [
    (price * sum(amount[k, i] for k in range(n_mines)) - sum(royalty[k] * isoperated[k, i] for k in range(n_mines)))
    * (1 / ((1 + discount) ** i)) for i in range(len(requiredquality))
]
prob += pulp.lpSum(profit_terms), "Total_Profit"

# Constraints
for i in range(len(requiredquality)):
    prob += pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) == requiredquality[i], f"Quality_Constraint_{i}"

for i in range(len(requiredquality)):
    prob += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork, f"Max_Work_Constraint_{i}"

for k in range(n_mines):
    for i in range(len(requiredquality)):
        prob += amount[k, i] <= limit[k] * isoperated[k, i], f"Mining_Limit_Constraint_{k}_{i}"

# Solve the problem
prob.solve()

# Prepare output
isoperated_output = [[pulp.value(isoperated[k, i]) for i in range(len(requiredquality))] for k in range(n_mines)]
amount_output = [[pulp.value(amount[k, i]) for i in range(len(requiredquality))] for k in range(n_mines)]

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(prob.objective)}</OBJ>')

# Return structured output
output = {
    "isoperated": isoperated_output,
    "amount": amount_output
}
output