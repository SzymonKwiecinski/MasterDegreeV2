import pulp

# Input Data
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
setup_time = [12, 8, 4, 0]

# Constants
M = len(machine_costs)  # Number of machines
P = len(prices)         # Number of parts

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flags_{p}', cat='Binary') for p in range(P)]

# Objective Function
problem += pulp.lpSum([prices[p] * batches[p] - 
                       pulp.lpSum(machine_costs[m] * time_required[m][p] * batches[p] for m in range(M))
                       for p in range(P)])

# Constraints

# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Setup Time Constraint for Machine 1
for p in range(P):
    problem += (setup_time[p] * setup_flags[p] + 
                pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))) <= availability[0]

# Solve Problem
problem.solve()

# Print Results
batches_result = [batches[p].varValue for p in range(P)]
setup_flags_result = [setup_flags[p].varValue for p in range(P)]

print(f'Batches Produced: {batches_result}')
print(f'Setup Flags: {setup_flags_result}')
print(f'Total Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')