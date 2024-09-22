import pulp

# Data from the problem
data = {'n_mines': 4, 
        'n_maxwork': 3, 
        'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 
        'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 
        'quality': [1.0, 0.7, 1.5, 0.5], 
        'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 
        'price': 10, 
        'discount': 0.1}

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
problem = pulp.LpProblem("Mining_Optimization", pulp.LpMaximize)

# Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0)

# Objective: Maximize discounted profit
profit = []
for i in range(n_years):
    revenue = pulp.lpSum(amount[(k, i)] for k in range(n_mines)) * price
    royalties = pulp.lpSum(royalty[k] * isoperated[(k, i)] for k in range(n_mines))
    discounted_profit = (revenue - royalties) / ((1 + discount) ** i)
    profit.append(discounted_profit)
problem += pulp.lpSum(profit)

# Constraints
for i in range(n_years):
    problem += pulp.lpSum(isoperated[(k, i)] for k in range(n_mines)) <= n_maxwork, f"max_worked_mines_year_{i}"
    for k in range(n_mines):
        problem += amount[(k, i)] <= limit[k] * isoperated[(k, i)], f"max_limit_mine_{k}_year_{i}"
    problem += pulp.lpSum(quality[k] * amount[(k, i)] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[(k, i)] for k in range(n_mines)), f"quality_year_{i}"

# Solve
problem.solve()

# Output
output = {
    "isoperated": [[pulp.value(isoperated[(k, i)]) for i in range(n_years)] for k in range(n_mines)],
    "amount": [[pulp.value(amount[(k, i)]) for i in range(n_years)] for k in range(n_mines)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')