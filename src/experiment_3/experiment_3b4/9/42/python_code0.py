import pulp

# Data from JSON
data = {'numdepot': [3, 3, 4], 
        'numport': [1, 6, 3], 
        'price': 3.0, 
        'distance': [[0.0, 2.0, 5.0], 
                     [2.0, 0.0, 3.0], 
                     [5.0, 3.0, 0.0]]}

numdepots = len(data['numdepot'])
numports = len(data['numport'])

# Initialize the problem
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", 
                          ((i, j) for i in range(numdepots) for j in range(numports)), 
                          lowBound=0, 
                          cat='Continuous')

# Objective function
problem += pulp.lpSum((x[i, j] / 2) * data['price'] * data['distance'][i][j] 
                      for i in range(numdepots) 
                      for j in range(numports))

# Constraints
# Depot Capacity Constraints
for i in range(numdepots):
    problem += pulp.lpSum(x[i, j] for j in range(numports)) <= data['numdepot'][i]

# Port Demand Constraints
for j in range(numports):
    problem += pulp.lpSum(x[i, j] for i in range(numdepots)) == data['numport'][j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')