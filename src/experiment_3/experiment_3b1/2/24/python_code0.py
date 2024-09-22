import pulp

# Data from the provided JSON
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

# Create the LP problem
problem = pulp.LpProblem("MiningOperations", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), lowBound=0)

# Objective Function
problem += pulp.lpSum([(price * amount[k, i] - royalty[k] * (1 - isoperated[k, i])) / ((1 + discount)**(i + 1)) 
                        for k in range(n_mines) for i in range(len(requiredquality))])

# Constraints

# Production and Quality Constraint
for i in range(len(requiredquality)):
    problem += pulp.lpSum([quality[k] * amount[k, i] for k in range(n_mines)]) \
               == requiredquality[i] * pulp.lpSum([amount[k, i] for k in range(n_mines)])

# Extraction Limit Constraint
for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

# Operating Mines Limit Constraint
for i in range(len(requiredquality)):
    problem += pulp.lpSum([isoperated[k, i] for k in range(n_mines)]) <= n_maxwork

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')