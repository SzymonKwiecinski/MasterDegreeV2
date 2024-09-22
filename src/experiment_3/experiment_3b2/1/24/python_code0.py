import pulp

# Data input
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_NPV", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", (range(data['n_mines']), range(len(data['requiredquality']))), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(data['n_mines']), range(len(data['requiredquality']))), lowBound=0)

# Objective Function: Maximize NPV
nv_terms = []
for i in range(len(data['requiredquality'])):
    present_value = (data['price'] * pulp.lpSum(amount[k][i] for k in range(data['n_mines'])) - 
                     pulp.lpSum(data['royalty'][k] * isoperated[k][i] for k in range(data['n_mines']))) / ((1 + data['discount']) ** i)
    nv_terms.append(present_value)
problem += pulp.lpSum(nv_terms)

# Constraints
# Maximum number of mines operated per year
for i in range(len(data['requiredquality'])):
    problem += pulp.lpSum(isoperated[k][i] for k in range(data['n_mines'])) <= data['n_maxwork']

# Production limits
for k in range(data['n_mines']):
    for i in range(len(data['requiredquality'])):
        problem += amount[k][i] <= data['limit'][k] * isoperated[k][i]

# Quality requirement
for i in range(len(data['requiredquality'])):
    problem += pulp.lpSum(data['quality'][k] * amount[k][i] for k in range(data['n_mines'])) == data['requiredquality'][i] * pulp.lpSum(amount[k][i] for k in range(data['n_mines']))

# Opening requirement
for k in range(data['n_mines']):
    for i in range(1, len(data['requiredquality'])):
        problem += isoperated[k][i] <= isoperated[k][i-1]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')