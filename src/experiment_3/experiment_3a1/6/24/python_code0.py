import pulp
import json

# Data provided in JSON format
data = json.loads("{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}")

# Extracting data
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", (range(n_mines), range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(n_mines), range(n_years)), lowBound=0)

# Objective function
profit = pulp.lpSum([ (price * pulp.lpSum([amount[k][i] for k in range(n_mines)]) / (1 + discount) ** (i + 1)) - 
                       pulp.lpSum([royalty[k] * isoperated[k][i] for k in range(n_mines)]) 
                       for i in range(n_years)])
problem += profit

# Constraints
# Mining Limitation
for i in range(n_years):
    problem += pulp.lpSum([isoperated[k][i] for k in range(n_mines)]) <= n_maxwork

# Ore Quality Requirement
for i in range(n_years):
    problem += pulp.lpSum([quality[k] * amount[k][i] for k in range(n_mines)]) == requiredquality[i] * pulp.lpSum([amount[k][i] for k in range(n_mines)])

# Extraction Limit
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k][i] <= limit[k] * isoperated[k][i]

# Open Mine Condition
for k in range(n_mines):
    problem += pulp.lpSum([isoperated[k][i] for i in range(n_years)]) <= 1

# Solve the problem
problem.solve()

# Output results
isoperated_result = [[pulp.value(isoperated[k][i]) for i in range(n_years)] for k in range(n_mines)]
amount_result = [[pulp.value(amount[k][i]) for i in range(n_years)] for k in range(n_mines)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print("Is Operated:")
print(isoperated_result)
print("Amount:")
print(amount_result)