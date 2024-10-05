import pulp

# Data from the JSON
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Number of products and machines
K = data['NumProducts']
S = data['NumMachines']

# Extracting the relevant data
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K))

# Constraints
# Production time constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')