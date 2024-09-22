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

# Variables
n_mines = data['n_mines']
n_periods = len(data['requiredquality'])

# Define the Linear Programming problem
problem = pulp.LpProblem("Mining_Optimization", pulp.LpMaximize)

# Decision Variables
amounts = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_periods)), lowBound=0, cat='Continuous')
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(n_periods)), cat='Binary')

# Objective Function
objective = sum((data['price'] * sum(amounts[k, i] for k in range(n_mines)) -
                 sum(data['royalty'][k] * isoperated[k, i] for k in range(n_mines))) /
                ((1 + data['discount']) ** i)
                for i in range(n_periods))
problem += objective

# Constraints

# Operating mines per period constraint
for i in range(n_periods):
    problem += sum(isoperated[k, i] for k in range(n_mines)) <= data['n_maxwork']

# Amount limit constraint
for k in range(n_mines):
    for i in range(n_periods):
        problem += amounts[k, i] <= data['limit'][k] * isoperated[k, i]

# Quality requirement constraint
for i in range(n_periods):
    total_amount = sum(amounts[k, i] for k in range(n_mines))
    if total_amount > 0:
        problem += (sum(data['quality'][k] * amounts[k, i] for k in range(n_mines)) ==
                    data['requiredquality'][i] * total_amount)

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')