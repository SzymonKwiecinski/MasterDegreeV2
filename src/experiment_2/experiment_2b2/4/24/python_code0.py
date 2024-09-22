from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpBinary, value

# Input data
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
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

# Problem
problem = LpProblem("Mining_Profit_Maximization", LpMaximize)

# Variables
isoperated = [[LpVariable(f'isoperated_{k}_{i}', cat=LpBinary) for i in range(n_years)] for k in range(n_mines)]
amount = [[LpVariable(f'amount_{k}_{i}', lowBound=0, cat='Continuous') for i in range(n_years)] for k in range(n_mines)]

# Constraints

# Limit constraints for each mine
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k][i] <= limit[k] * isoperated[k][i], f'Limit_{k}_{i}'

# Maximum number of mines operated per year
for i in range(n_years):
    problem += lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork, f'Max_Work_{i}'

# Quality constraints
for i in range(n_years):
    problem += lpSum(amount[k][i] * quality[k] for k in range(n_mines)) == requiredquality[i] * lpSum(amount[k][i] for k in range(n_mines)), f'Quality_{i}'

# Revenue calculation
revenue = lpSum((lpSum(amount[k][i] for k in range(n_mines)) * price) / ((1 + discount) ** i) for i in range(n_years))

# Cost calculation (Royalties)
royalty_cost = lpSum(isoperated[k][i] * royalty[k] / ((1 + discount) ** i) for k in range(n_mines) for i in range(n_years))

# Objective function: Maximize profit
problem += revenue - royalty_cost

# Solve
problem.solve()

# Prepare output
output = {
    "isoperated": [[int(isoperated[k][i].varValue) for i in range(n_years)] for k in range(n_mines)],
    "amount": [[amount[k][i].varValue for i in range(n_years)] for k in range(n_mines)]
}

print(output)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')