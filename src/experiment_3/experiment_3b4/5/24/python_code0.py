import pulp

# Data
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

# Indices
K = data['n_mines']
I = len(data['requiredquality'])

# Create the LP problem
problem = pulp.LpProblem("Mining_Optimization", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(K) for i in range(I)), cat='Binary')

# Objective function: Maximize the total discounted profit
objective = pulp.lpSum(
    (data['price'] / (1 + data['discount'])**i) * pulp.lpSum(amount[k, i] for k in range(K))
    - pulp.lpSum(data['royalty'][k] * (1 - isoperated[k, i]) / (1 + data['discount'])**i for k in range(K))
    for i in range(I)
)
problem += objective

# Constraints

# Maximum number of mines operated at the same time
for i in range(I):
    problem += pulp.lpSum(isoperated[k, i] for k in range(K)) <= data['n_maxwork']

# Amount extracted cannot exceed limit if not operated
for k in range(K):
    for i in range(I):
        problem += amount[k, i] <= data['limit'][k] * isoperated[k, i]

# Blend quality requirement
for i in range(I):
    total_amount = pulp.lpSum(amount[k, i] for k in range(K))
    problem += pulp.lpSum(amount[k, i] * data['quality'][k] for k in range(K)) == data['requiredquality'][i] * total_amount

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')