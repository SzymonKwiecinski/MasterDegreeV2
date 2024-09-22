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

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
is_operated = pulp.LpVariable.dicts("is_operated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0, cat='Continuous')

# Objective Function
profit_terms = []
for i in range(n_years):
    earnings = price * pulp.lpSum(amount[k, i] for k in range(n_mines))
    expenses = pulp.lpSum(royalty[k] * is_operated[k, i] for k in range(n_mines))
    profit_terms.append((earnings - expenses) * (1 + discount) ** -i)

problem += pulp.lpSum(profit_terms)

# Constraints
# Maximum mines operated per year
for i in range(n_years):
    problem += pulp.lpSum(is_operated[k, i] for k in range(n_mines)) <= n_maxwork

# Quality constraint for blended ore
for i in range(n_years):
    weighted_quality = pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines))
    total_amount = pulp.lpSum(amount[k, i] for k in range(n_mines))
    problem += weighted_quality == requiredquality[i] * total_amount

# Production limit per mine
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * is_operated[k, i]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')