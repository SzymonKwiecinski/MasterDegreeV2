import pulp

# Input Data
data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}

# Problem Parameters
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
years = len(requiredquality)

# Create Problem
problem = pulp.LpProblem("Mining_Operation", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(years)), lowBound=0, cat='Continuous')

# Objective Function: Maximize Discounted Profit
problem += pulp.lpSum([
    (
        price * pulp.lpSum([amount[k, i] for k in range(n_mines)]) -
        pulp.lpSum([royalty[k] * isoperated[k, i] for k in range(n_mines)])
    ) / ((1 + discount) ** i)
    for i in range(years)
])

# Constraints

# Limit on mine production
for k in range(n_mines):
    for i in range(years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Required Quality
for i in range(years):
    problem += pulp.lpSum([quality[k] * amount[k, i] for k in range(n_mines)]) == requiredquality[i] * pulp.lpSum([amount[k, i] for k in range(n_mines)])

# Maximum mines operated each year
for i in range(years):
    problem += pulp.lpSum([isoperated[k, i] for k in range(n_mines)]) <= n_maxwork

# Solve Problem
problem.solve()

# Prepare Output
output = {
    "isoperated": [[pulp.value(isoperated[k, i]) for i in range(years)] for k in range(n_mines)],
    "amount": [[pulp.value(amount[k, i]) for i in range(years)] for k in range(n_mines)]
}

# Print Output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')