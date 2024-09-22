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
problem = pulp.LpProblem("Mining_Company_Operations", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    (price * pulp.lpSum(amount[k, i] for k in range(n_mines)) 
     - pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines))) 
    * ((1 + discount) ** -i) 
    for i in range(n_years)
)

# Constraints
for i in range(n_years):
    # Maximum number of mines operated constraint
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

    # Quality constraint
    quality_expr = pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines))
    total_amount_expr = pulp.lpSum(amount[k, i] for k in range(n_mines))
    problem += quality_expr == requiredquality[i] * total_amount_expr

for k in range(n_mines):
    for i in range(n_years):
        # Limit constraint
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')