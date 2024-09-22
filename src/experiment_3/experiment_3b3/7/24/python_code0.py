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

# Parameters
n_mines = data['n_mines']
n_years = len(data['requiredquality'])
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Problem
problem = pulp.LpProblem("Mining_Company_Operations", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0, cat='Continuous')

# Objective
objective = pulp.lpSum(
    [(price * pulp.lpSum([amount[k, i] for k in range(n_mines)]) / ((1 + discount) ** (i + 1))
      - pulp.lpSum([royalty[k] * isoperated[k, i] for k in range(n_mines)])) for i in range(n_years)]
)
problem += objective

# Constraints

# Mine Operation Limit
for i in range(n_years):
    problem += pulp.lpSum([isoperated[k, i] for k in range(n_mines)]) <= n_maxwork

# Quality Requirement
for i in range(n_years):
    problem += pulp.lpSum([quality[k] * amount[k, i] for k in range(n_mines)]) == requiredquality[i] * pulp.lpSum([amount[j, i] for j in range(n_mines)])

# Production Limit
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Solve the problem
problem.solve()

# Output Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')