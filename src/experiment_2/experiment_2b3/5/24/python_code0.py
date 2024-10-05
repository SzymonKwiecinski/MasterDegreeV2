import pulp

# Input data
data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

I = len(requiredquality)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(I)), lowBound=0)
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(I)), cat='Binary')

# Objective function
# Maximize profit = revenue - royalties
objective = pulp.lpSum([(price * pulp.lpSum(amount[(k, i)] for k in range(n_mines)) - pulp.lpSum(royalty[k] * isoperated[(k, i)] for k in range(n_mines))) / ((1 + discount) ** i) for i in range(I)])
problem += objective

# Constraints
# Constraint 1: Limit on the number of mines that can be operated each year
for i in range(I):
    problem += pulp.lpSum(isoperated[(k, i)] for k in range(n_mines)) <= n_maxwork

# Constraint 2: Maximum production limit per mine
for k in range(n_mines):
    for i in range(I):
        problem += amount[(k, i)] <= limit[k] * isoperated[(k, i)]

# Constraint 3: Quality requirement for blended ore each year
for i in range(I):
    total_amount = pulp.lpSum(amount[(k, i)] for k in range(n_mines))
    problem += pulp.lpSum(quality[k] * amount[(k, i)] for k in range(n_mines)) == requiredquality[i] * total_amount

# Solve the problem
problem.solve()

# Output results
isoperated_result = [[pulp.value(isoperated[(k, i)]) for i in range(I)] for k in range(n_mines)]
amount_result = [[pulp.value(amount[(k, i)]) for i in range(I)] for k in range(n_mines)]

output = {
    "isoperated": isoperated_result,
    "amount": amount_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')