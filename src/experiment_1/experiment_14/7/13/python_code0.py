import pulp

# Data input
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Extracting data
Time = data['time']
Profit = data['profit']
Capacity = data['capacity']

# Number of different spare parts and machines
K = len(Profit)
S = len(Capacity)

# Define the problem
problem = pulp.LpProblem("OptimalProductionOfSpareParts", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(K)), "Total Profit"

# Constraints
# Machine time constraints
for s in range(S):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(K)) <= Capacity[s], f"MachineCapacity{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')