import pulp

# Data from the problem
data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 
        'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 
        'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
years = len(requiredquality)

# Initialize the problem
problem = pulp.LpProblem("Mine_Operation", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(years)), lowBound=0, cat='Continuous')

# Objective function: Maximize the discounted profit
discounted_profit = pulp.lpSum(
    pulp.lpSum(price * amount[k, i] for k in range(n_mines)) / ((1 + discount) ** i) -
    pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines)) / ((1 + discount) ** i)
    for i in range(years)
)
problem += discounted_profit

# Constraints
# At most n_maxwork mines can be operated each year
for i in range(years):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

# Amount from each mine cannot exceed its limit
for k in range(n_mines):
    for i in range(years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Required quality constraint for each year
for i in range(years):
    problem += pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) == \
               requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines))

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "isoperated": [[int(isoperated[k, i].varValue) for i in range(years)] for k in range(n_mines)],
    "amount": [[amount[k, i].varValue for i in range(years)] for k in range(n_mines)]
}

print(output)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")