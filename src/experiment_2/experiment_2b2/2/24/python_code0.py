from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value
from math import pow

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

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

n_years = len(requiredquality)

# Problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Decision variables
isoperated = [[LpVariable(f"isoperated_{k}_{i}", cat='Binary') for i in range(n_years)] for k in range(n_mines)]
amount = [[LpVariable(f"amount_{k}_{i}", lowBound=0) for i in range(n_years)] for k in range(n_mines)]

# Objective
discounted_revenue = lpSum([
    price * lpSum(amount[k][i] for k in range(n_mines)) / pow(1 + discount, i + 1) for i in range(n_years)
])

discounted_royalty = lpSum([
    lpSum(isoperated[k][i] * royalty[k] for k in range(n_mines)) / pow(1 + discount, i + 1) for i in range(n_years)
])

profit = discounted_revenue - discounted_royalty
problem += profit

# Constraints
for i in range(n_years):
    # Quality constraint for each year
    problem += lpSum(amount[k][i] * quality[k] for k in range(n_mines)) == lpSum(amount[k][i] for k in range(n_mines)) * requiredquality[i]

    # Max number of mines operated per year
    problem += lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork

    for k in range(n_mines):
        # Do not exceed limit of each mine
        problem += amount[k][i] <= limit[k] * isoperated[k][i]

        # If in any year a mine is operated, it must be operated in previous years or open
        if i > 0:
            problem += isoperated[k][i] >= isoperated[k][i - 1]

# Solve the problem
problem.solve()

# Results
solution = {
    "isoperated": [[int(isoperated[k][i].varValue) for i in range(n_years)] for k in range(n_mines)],
    "amount": [[amount[k][i].varValue for i in range(n_years)] for k in range(n_mines)]
}

print(solution)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')