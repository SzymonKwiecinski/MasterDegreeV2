import pulp

# Data extracted from JSON format
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

# Model definition
problem = pulp.LpProblem("Maximize_NPV_of_Profits", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(data['n_mines']) for i in range(len(data['requiredquality']))), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(data['n_mines']) for i in range(len(data['requiredquality']))), lowBound=0)

# Objective function
problem += pulp.lpSum(
    (data['price'] / (1 + data['discount']) ** (i + 1)) * 
    (pulp.lpSum(amount[k, i] for k in range(data['n_mines'])) - 
     pulp.lpSum(data['royalty'][k] * isoperated[k, i] for k in range(data['n_mines'])))
    for i in range(len(data['requiredquality'])))
    
# Constraints
# Quality constraint
for i in range(len(data['requiredquality'])):
    problem += pulp.lpSum(amount[k, i] * data['quality'][k] for k in range(data['n_mines'])) == data['requiredquality'][i] * pulp.lpSum(amount[k, i] for k in range(data['n_mines']))

# Limit constraint
for k in range(data['n_mines']):
    for i in range(len(data['requiredquality'])):
        problem += amount[k, i] <= data['limit'][k] * isoperated[k, i]

# Max work constraint
for i in range(len(data['requiredquality'])):
    problem += pulp.lpSum(isoperated[k, i] for k in range(data['n_mines'])) <= data['n_maxwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')