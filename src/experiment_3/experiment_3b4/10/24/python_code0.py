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

# Constants
K = data['n_mines']
I = len(data['requiredquality'])
price = data['price']
discount = data['discount']

# Problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
# isoperated_{k,i} => Binary variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(K) for i in range(I)), cat='Binary')

# amount_{k,i} => Continuous variables
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
discounted_profit = pulp.lpSum([
    (1 / ((1 + discount) ** i)) * (
        price * pulp.lpSum([amount[k, i] for k in range(K)]) -
        pulp.lpSum([data['royalty'][k] * isoperated[k, i] for k in range(K)])
    ) for i in range(I)
])
problem += discounted_profit

# Constraints
# Quality Constraints
for i in range(I):
    problem += pulp.lpSum([amount[k, i] * data['quality'][k] for k in range(K)]) == data['requiredquality'][i] * pulp.lpSum([amount[k, i] for k in range(K)])

# Capacity Constraints
for k in range(K):
    for i in range(I):
        problem += amount[k, i] <= data['limit'][k] * isoperated[k, i]

# Operational Constraints
for i in range(I):
    problem += pulp.lpSum([isoperated[k, i] for k in range(K)]) <= data['n_maxwork']

# Solve the problem
problem.solve()

# Output
print(f'Objective Value: <OBJ>{pulp.value(problem.objective)}</OBJ>')