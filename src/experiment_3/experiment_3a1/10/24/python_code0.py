import pulp

# Data from the provided JSON format
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

# Model Initialization
problem = pulp.LpProblem("Mining_Operations", pulp.LpMaximize)

# Variables
I = len(data['requiredquality'])
n_mines = data['n_mines']

isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(I)), 
                                             cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(I)), 
                                        lowBound=0)

# Objective Function
profit = pulp.lpSum((data['price'] * pulp.lpSum(amount[k, i] for k in range(n_mines)) - 
                     pulp.lpSum(data['royalty'][k] * isoperated[k, i] for k in range(n_mines))) / 
                     ((1 + data['discount']) ** (i + 1)) for i in range(I))

problem += profit

# Constraints

# 1. Operating mines constraint
for i in range(I):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= data['n_maxwork']

# 2. Quality blending constraint
for i in range(I):
    problem += pulp.lpSum(data['quality'][k] * amount[k, i] for k in range(n_mines)) == \
               data['requiredquality'][i] * pulp.lpSum(amount[k, i] for k in range(n_mines))

# 3. Amount produced constraint
for k in range(n_mines):
    for i in range(I):
        problem += amount[k, i] <= data['limit'][k] * isoperated[k, i]

# Solve the Problem
problem.solve()

# Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')