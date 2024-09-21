import pulp

# Define the data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Unpacking the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define the decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective function
profit = (
    pulp.lpSum(prices[p] * x[p] for p in range(P)) -
    pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M))
)
problem += profit

# Constraints

# Machine time availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

# Minimum production requirements
for p in range(P):
    problem += x[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Output the optimal number of batches for each part
for p in range(P):
    print(f'Number of batches of part {p+1}: {x[p].varValue}')
    
# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')