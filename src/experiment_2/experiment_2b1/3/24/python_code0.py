import json
import pulp

# Input data
data = {'n_mines': 4, 'n_maxwork': 3, 
        'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 
        'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 
        'quality': [1.0, 0.7, 1.5, 0.5], 
        'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 
        'price': 10, 
        'discount': 0.1}

# Problem parameters
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", (range(n_mines), range(len(requiredquality))), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(n_mines), range(len(requiredquality))), lowBound=0)

# Objective function: maximize profit
profit = pulp.lpSum([(price * pulp.lpSum(amount[k][i] for k in range(n_mines))) - 
                      pulp.lpSum(royalty[k] * isoperated[k][i] for k in range(n_mines))) / ((1 + discount) ** i) 
                      for i in range(len(requiredquality))])

problem += profit

# Constraints
# Each year the total extracted quality must equal the required quality
for i in range(len(requiredquality)):
    problem += pulp.lpSum(quality[k] * amount[k][i] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[k][i] for k in range(n_mines))

# Each mine's production must not exceed its limit
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k][i] <= limit[k] * isoperated[k][i]

# At most n_maxwork mines can operate in a year
for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork

# Solve the problem
problem.solve()

# Prepare output
output_isoperated = [[pulp.value(isoperated[k][i]) for i in range(len(requiredquality))] for k in range(n_mines)]
output_amount = [[pulp.value(amount[k][i]) for i in range(len(requiredquality))] for k in range(n_mines)]

output = {
    "isoperated": output_isoperated,
    "amount": output_amount
}

# Print results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')