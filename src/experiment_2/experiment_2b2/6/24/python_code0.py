# Importing necessary libraries
import pulp
import json

# Reading the data
data = '''{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}'''
data = json.loads(data.replace("'", "\""))

# Extracting variables
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

# Number of years
I = len(requiredquality)

# Creating the problem
problem = pulp.LpProblem("Mining_Optimization", pulp.LpMaximize)

# Decision variables - amount of ore extracted from mine k in year i
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(I)), lowBound=0)

# Decision variables - whether a mine is operated in year i
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(I)), cat='Binary')

# Objective function - maximizing discounted profit
profit = pulp.lpSum([(price * pulp.lpSum([amount[(k, i)] for k in range(n_mines)]) * (1 - discount)**i) - 
                     (pulp.lpSum([isoperated[(k, i)] * royalty[k] for k in range(n_mines)]) * (1 - discount)**i)
                     for i in range(I)])
problem += profit

# Constraints
# 1. Each year's ore output must have the required quality
for i in range(I):
    problem += pulp.lpSum([quality[k] * amount[(k, i)] for k in range(n_mines)]) == requiredquality[i] * pulp.lpSum([amount[(k, i)] for k in range(n_mines)])

# 2. A mine's output cannot exceed its limit when operated
for k in range(n_mines):
    for i in range(I):
        problem += amount[(k, i)] <= limit[k] * isoperated[(k, i)]

# 3. At most n_maxwork mines can be operated each year
for i in range(I):
    problem += pulp.lpSum([isoperated[(k, i)] for k in range(n_mines)]) <= n_maxwork

# Solving the problem
problem.solve()

# Retrieving and formatting results
output = {
    "isoperated": [[int(isoperated[(k, i)].varValue) for i in range(I)] for k in range(n_mines)],
    "amount": [[amount[(k, i)].varValue for i in range(I)] for k in range(n_mines)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')