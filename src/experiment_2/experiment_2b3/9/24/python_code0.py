import pulp

# Extract data from JSON
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

# Initialize problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
K = data['n_mines']
I = len(data['requiredquality'])
is_operated = pulp.LpVariable.dicts("is_operated", ((k, i) for k in range(K) for i in range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective Function: Maximize discounted profit 
total_profit = 0
for i in range(I):
    year_profit = pulp.lpSum(data['price'] * amount[k, i] - is_operated[k, i] * data['royalty'][k] 
                             for k in range(K))
    # Apply discount
    total_profit += year_profit / ((1 + data['discount']) ** i)
problem += total_profit

# Constraints
for i in range(I):
    # Blended quality must meet the requirement
    problem += pulp.lpSum(amount[k, i] * data['quality'][k] for k in range(K)) == data['requiredquality'][i] * pulp.lpSum(amount[k, i] for k in range(K))
    # Limit the number of operated mines
    problem += pulp.lpSum(is_operated[k, i] for k in range(K)) <= data['n_maxwork']
    for k in range(K):
        # Production cannot exceed the limit of the mine
        problem += amount[k, i] <= data['limit'][k] * is_operated[k, i]

# Solve the problem
problem.solve()

# Gather results
isoperated = [[int(is_operated[k, i].varValue) for i in range(I)] for k in range(K)]
amount_produced = [[amount[k, i].varValue for i in range(I)] for k in range(K)]

# Output results
output = {
    "isoperated": isoperated,
    "amount": amount_produced
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')