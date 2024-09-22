import pulp

# Parameters
data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 
        'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 
        'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}

n_mines = data['n_mines']
n_years = len(data['requiredquality'])
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0)

# Problem
problem = pulp.LpProblem("Mining_Operations", pulp.LpMaximize)

# Objective Function
revenue = {i: price * pulp.lpSum(amount[k, i] for k in range(n_mines)) for i in range(n_years)}
cost = {i: pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines)) for i in range(n_years)}
present_value_profit = pulp.lpSum((revenue[i] - cost[i]) / ((1 + discount) ** i) for i in range(n_years))
problem += present_value_profit

# Constraints
# Blended quality constraint
for i in range(n_years):
    problem += (pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines)) ==
                requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines)))

# Ore production limit for each mine and year
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Maximum number of mines operated in each year
for i in range(n_years):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

# Solve the problem
problem.solve()

# Output results
isoperated_output = [[pulp.value(isoperated[k, i]) for i in range(n_years)] for k in range(n_mines)]
amount_output = [[pulp.value(amount[k, i]) for i in range(n_years)] for k in range(n_mines)]

print("Operation Status (0=Not operated, 1=Operated):")
for k in range(n_mines):
    print(f"Mine {k+1}: {isoperated_output[k]}")

print("\nAmount of Ore Produced:")
for k in range(n_mines):
    print(f"Mine {k+1}: {amount_output[k]}")

print(f'\n (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')