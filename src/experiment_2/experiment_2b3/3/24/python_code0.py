import pulp

# Parse the input data from JSON format
data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Time periods (years)
T = len(requiredquality)

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(T)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(T)), lowBound=0, cat='Continuous')

# Objective function: Maximize the discounted profit
profit = pulp.lpSum([
    ((pulp.lpSum(amount[k, i] for k in range(n_mines)) * price -
      pulp.lpSum(isoperated[k, i] * royalty[k] for k in range(n_mines))) /
     ((1 + discount) ** i))
    for i in range(T)
])
problem += profit

# Constraints

# Limit the number of mines that can be operated each year
for i in range(T):
    problem += (pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork, f"Max_Mines_Operated_Year_{i}")

# The ore from the mines must meet the quality requirements each year
for i in range(T):
    problem += (pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) ==
                pulp.lpSum(amount[k, i] for k in range(n_mines)) * requiredquality[i], f"Quality_Requirement_Year_{i}")

# The amount produced by each mine should not exceed its limit and should be zero if not operated
for i in range(T):
    for k in range(n_mines):
        problem += (amount[k, i] <= limit[k] * isoperated[k, i], f"Limit_Amount_Mine_{k}_Year_{i}")

# Solve the problem
problem.solve()

# Prepare the results
output = {
    "isoperated": [[int(pulp.value(isoperated[k, i])) for i in range(T)] for k in range(n_mines)],
    "amount": [[pulp.value(amount[k, i]) for i in range(T)] for k in range(n_mines)]
}

# Print the output
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')