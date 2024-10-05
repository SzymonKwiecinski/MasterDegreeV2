import pulp

# Data provided
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

# Retrieving the number of years from the 'requiredquality' list
I = len(data['requiredquality'])
n = data['n_mines']

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n) for i in range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(
    (data['price'] * pulp.lpSum(amount[k, i] for k in range(n)) / ((1 + data['discount']) ** (i + 1))
    - pulp.lpSum(data['royalty'][k] * isoperated[k, i] for k in range(n))) for i in range(I)
)

# Constraints

# 1. Mine Operation Constraint
for i in range(I):
    problem += (pulp.lpSum(isoperated[k, i] for k in range(n)) <= data['n_maxwork'])

# 2. Quality Constraint
for i in range(I):
    problem += (pulp.lpSum(data['quality'][k] * amount[k, i] for k in range(n)) ==
                data['requiredquality'][i] * pulp.lpSum(amount[k, i] for k in range(n)))

# 3. Production Limit Constraint
for k in range(n):
    for i in range(I):
        problem += (amount[k, i] <= data['limit'][k] * isoperated[k, i])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')