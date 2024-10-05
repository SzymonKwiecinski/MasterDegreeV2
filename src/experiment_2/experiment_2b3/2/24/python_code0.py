import pulp

data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 
        'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 
        'quality': [1.0, 0.7, 1.5, 0.5], 
        'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 
        'price': 10, 'discount': 0.1}

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

problem = pulp.LpProblem("Mining_Problem", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isOperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("Amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0)

# Objective function
profit = pulp.lpSum([
    ((price * pulp.lpSum(amount[k, i] for k in range(n_mines))) - 
    pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines))) / ((1 + discount) ** i) 
    for i in range(n_years)
])
problem += profit

# Constraints
for i in range(n_years):
    # The number of operated mines in any year must not exceed the limit
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

    # The blended ore must meet the required quality for each year
    problem += pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) == (
               pulp.lpSum(amount[k, i] for k in range(n_mines)) * requiredquality[i])

for k in range(n_mines):
    for i in range(n_years):
        # The amount of ore from a mine cannot exceed its limit
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "isoperated": [[int(isoperated[k, i].varValue) for i in range(n_years)] for k in range(n_mines)],
    "amount": [[amount[k, i].varValue for i in range(n_years)] for k in range(n_mines)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')