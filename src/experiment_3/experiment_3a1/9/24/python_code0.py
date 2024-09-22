import pulp

# Data from the JSON format
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
T = len(requiredquality)  # Number of years from required quality

# Define the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", (range(n_mines), range(T)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(n_mines), range(T)), lowBound=0)

# Objective Function
profit = pulp.lpSum([(price * pulp.lpSum(amount[k][i] for k in range(n_mines)) 
                      - pulp.lpSum(royalty[k] * isoperated[k][i] for k in range(n_mines))) / ((1 + discount) ** i)
                      for i in range(T)])

problem += profit

# Constraints
# Total amount of ore quality constraint
for i in range(T):
    problem += pulp.lpSum((quality[k] * amount[k][i]) / pulp.lpSum(amount[j][i] for j in range(n_mines)) 
                          for k in range(n_mines)) == requiredquality[i], f"Quality_Constraint_{i}"

# Maximum number of mines that can be operated
for i in range(T):
    problem += pulp.lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork, f"Max_Mines_Constraint_{i}"

# Ore production limit for each mine
for k in range(n_mines):
    for i in range(T):
        problem += amount[k][i] <= limit[k] * isoperated[k][i], f"Production_Limit_{k}_{i}"

# Solve the problem
problem.solve()

# Output results
isoperated_result = [[pulp.value(isoperated[k][i]) for k in range(n_mines)] for i in range(T)]
amount_result = [[pulp.value(amount[k][i]) for k in range(n_mines)] for i in range(T)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')