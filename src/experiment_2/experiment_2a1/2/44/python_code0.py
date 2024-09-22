import pulp
import json

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)      # Number of parts
M = len(machine_costs)  # Number of machines

# Define the Linear Programming problem
problem = pulp.LpProblem('Maximize_Profit', pulp.LpMaximize)

# Define decision variables
batches = pulp.LpVariable.dicts('Batches', range(P), lowBound=0, cat='Continuous')

# Define the objective function
problem += pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] / 100 for p in range(P)) for m in range(M)), "Total_Profit"

# Add constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p], f'Min_Batches_Constraint_{p}'

# Add constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f'Machine_Availability_Constraint_{m}'

# Solve the problem
problem.solve()

# Create output
output = {
    "batches": [batches[p].varValue for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')