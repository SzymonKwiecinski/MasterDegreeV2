import pulp

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

# Extracting data into variables for easier reference
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
problem = pulp.LpProblem("Mining_Company_Problem", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0)

# Objective function
objective = pulp.lpSum(
    [(price * amount[k, i] - royalty[k] * isoperated[k, i]) * (1 + discount) ** -i 
     for k in range(n_mines) for i in range(n_years)]
)
problem += objective

# Constraints
# Constraint 1: Maximum number of mines operating
for i in range(n_years):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

# Constraint 2: Required quality in each year
for i in range(n_years):
    total_amount = pulp.lpSum(amount[k, i] for k in range(n_mines))
    weighted_quality = pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines))
    problem += weighted_quality == requiredquality[i] * total_amount

# Constraint 3: Upper limit on extracted ore
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')