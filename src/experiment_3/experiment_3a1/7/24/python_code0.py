import pulp

# Data from the provided JSON
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

# Create the problem
problem = pulp.LpProblem("Mining_Company_Operations", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", 
                                     ((k, i) for k in range(n_mines) for i in range(n_years)), 
                                     cat='Binary')

amount = pulp.LpVariable.dicts("amount", 
                                 ((k, i) for k in range(n_mines) for i in range(n_years)), 
                                 lowBound=0)

# Objective function
problem += pulp.lpSum(
    [(pulp.lpSum(price * amount[k, i] for k in range(n_mines)) - 
      pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines))) * 
     (1 + discount) ** (-i) for i in range(n_years)]
)

# Constraints
# Constraint 1: Maximum number of mines operating in any year
for i in range(n_years):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

# Constraint 2: Required blended quality
for i in range(n_years):
    problem += pulp.lpSum(quality[k] * (amount[k, i] / pulp.lpSum(amount[j, i] for j in range(n_mines))) for k in range(n_mines)) == requiredquality[i]

# Constraint 3: Amount limit per mine based on operation
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')