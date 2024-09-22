import pulp
import json

data = json.loads("""{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}""")

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Create the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("isoperated", (range(n_mines), range(len(requiredquality))), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(n_mines), range(len(requiredquality))), lowBound=0)

# Objective Function
profits = [price * discount ** i * sum(amount[k][i] for k in range(n_mines)) - sum(royalty[k] * isoperated[k][i] for k in range(n_mines)) for i in range(len(requiredquality))]
problem += pulp.lpSum(profits)

# Constraints
# At most n_maxwork mines can be operated each year
for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k][i] for k in range(n_mines)) <= n_maxwork

# The quality of the blended ore must be equal to required quality
for i in range(len(requiredquality)):
    problem += pulp.lpSum(quality[k] * amount[k][i] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[k][i] for k in range(n_mines))

# Limit the amount produced by each mine according to its limit
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k][i] <= limit[k] * isoperated[k][i]
        
# Solve the problem
problem.solve()

# Preparing output
isoperated_output = [[pulp.value(isoperated[k][i]) for i in range(len(requiredquality))] for k in range(n_mines)]
amount_output = [[pulp.value(amount[k][i]) for i in range(len(requiredquality))] for k in range(n_mines)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output format
output = {
    "isoperated": isoperated_output,
    "amount": amount_output
}