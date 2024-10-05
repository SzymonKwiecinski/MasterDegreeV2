import pulp
import json

# Extracting data from the JSON format
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

# Initialize the Linear Program
problem = pulp.LpProblem("Mining_Operation_NPV_Maximization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((k,i) for k in range(n_mines) for i in range(n_years)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k,i) for k in range(n_mines) for i in range(n_years)), cat='Binary')

# Objective function
problem += pulp.lpSum((1 / ((1 + discount) ** (i + 1))) * 
                      (price * x[(k,i)] - royalty[k] * y[(k,i)]) 
                      for k in range(n_mines) 
                      for i in range(n_years))

# Constraints

# Max number of mines operated each year
for i in range(n_years):
    problem += pulp.lpSum(y[(k,i)] for k in range(n_mines)) <= n_maxwork

# Production limit based on operation
for k in range(n_mines):
    for i in range(n_years):
        problem += x[(k,i)] <= limit[k] * y[(k,i)]

# Blended quality requirement
for i in range(n_years):
    quality_constraint = pulp.lpSum((x[(k,i)] * quality[k]) for k in range(n_mines))
    total_ore = pulp.lpSum(x[(m,i)] for m in range(n_mines))
    problem += quality_constraint == requiredquality[i] * total_ore

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')