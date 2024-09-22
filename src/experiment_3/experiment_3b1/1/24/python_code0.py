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

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
I = len(requiredquality)

# Create the problem
problem = pulp.LpProblem("Mining_Company_Problem", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", 
                                     ((k, i) for k in range(n_mines) for i in range(I)), 
                                     cat='Binary')

amount = pulp.LpVariable.dicts("amount", 
                               ((k, i) for k in range(n_mines) for i in range(I)), 
                               lowBound=0)

# Objective function
problem += pulp.lpSum((price * pulp.lpSum(amount[k, i] for k in range(n_mines)) 
                        - pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines))) 
                       / ((1 + discount) ** (i + 1)) for i in range(I)), "Total Profit"

# Constraints
# Work limit
for i in range(I):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork, f"Work_Limit_Year_{i + 1}"

# Quality constraint
for i in range(I):
    problem += pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines)) \
               == requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines)), \
               f"Quality_Constraint_Year_{i + 1}"

# Production limit
for k in range(n_mines):
    for i in range(I):
        problem += amount[k, i] <= limit[k] * isoperated[k, i], f"Production_Limit_Mine_{k + 1}_Year_{i + 1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')