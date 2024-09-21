import pulp

# Data from the JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Initialize the problem
problem = pulp.LpProblem("OptimalProductionOfSpareParts", pulp.LpMaximize)

# Extracting data
K = len(data['profit'])  # Number of spare parts
S = len(data['capacity'])  # Number of machines

# Parameters
Time = data['time']
Profit = data['profit']
Capacity = data['capacity']

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(K)])

# Constraints
# Capacity constraints for each machine
for s in range(S):
    problem += pulp.lpSum([Time[k][s] * x[k] for k in range(K)]) <= Capacity[s]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')