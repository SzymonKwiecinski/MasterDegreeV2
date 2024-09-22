import pulp

# Data from JSON
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
I = len(requiredquality)
K = n_mines

# Create the problem
problem = pulp.LpProblem("MiningOperations", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(K) for i in range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective Function
profit = pulp.lpSum([(price * pulp.lpSum(amount[k, i] for k in range(K)) - 
                      pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(K))) * 
                      (1 + discount) ** (-i) for i in range(I)])
problem += profit

# Constraints
# 1. Maximum number of mines operated per year
for i in range(I):
    problem += pulp.lpSum(isoperated[k, i] for k in range(K)) <= n_maxwork

# 2. Required ore quality per year
for i in range(I):
    problem += pulp.lpSum(amount[k, i] * quality[k] for k in range(K)) == requiredquality[i]

# 3. Limit of ore extraction from each mine
for k in range(K):
    for i in range(I):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Solve the problem
problem.solve()

# Output results
isoperated_result = [[pulp.value(isoperated[k, i]) for i in range(I)] for k in range(K)]
amount_result = [[pulp.value(amount[k, i]) for i in range(I)] for k in range(K)]

print("isoperated:", isoperated_result)
print("amount:", amount_result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')