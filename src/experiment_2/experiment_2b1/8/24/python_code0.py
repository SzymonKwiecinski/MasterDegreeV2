import pulp

# Data input from JSON format
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

# Create the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", 
                                     ((k, i) for k in range(n_mines) for i in range(len(requiredquality))),
                                     cat='Binary')

amount = pulp.LpVariable.dicts("amount", 
                                 ((k, i) for k in range(n_mines) for i in range(len(requiredquality))),
                                 lowBound=0, cat='Continuous')

# Objective function: maximize profit
profit = pulp.lpSum((amount[k, i] * price - royalty[k] * isoperated[k, i]) * ((1 + discount) ** -i) 
                    for k in range(n_mines) for i in range(len(requiredquality)))

problem += profit

# Constraints
for i in range(len(requiredquality)):
    problem += pulp.lpSum(amount[k, i] for k in range(n_mines)) == pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines)) * requiredquality[i]

for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Solve the problem
problem.solve()

# Output the results
isoperated_output = [[pulp.value(isoperated[k, i]) for i in range(len(requiredquality))] for k in range(n_mines)]
amount_output = [[pulp.value(amount[k, i]) for i in range(len(requiredquality))] for k in range(n_mines)]

result = {
    'isoperated': isoperated_output,
    'amount': amount_output
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')