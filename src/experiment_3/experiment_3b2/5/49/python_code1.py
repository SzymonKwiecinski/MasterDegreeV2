import pulp
import json

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['time_required'])  # Number of machines
time_matrix = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([prices[p] * x[p] - 
                     pulp.lpSum([machine_costs[m] * time_matrix[m][p] * x[p] for m in range(M)])
                     for p in range(P)])
problem += profit, "Total_Profit"

# Constraints

# Minimum Production Requirement
for p in range(P):
    problem += x[p] >= min_batches[p], f"MinProduction_{p+1}"

# Machine Time Availability
for m in range(M - 2):
    problem += pulp.lpSum([time_matrix[m][p] * x[p] for p in range(P)]) <= availability[m], f"MachineAvailability_{m+1}"

# Handling the shared availability for last two machines
problem += (pulp.lpSum([time_matrix[M-2][p] * x[p] for p in range(P)]) + 
            pulp.lpSum([time_matrix[M-1][p] * x[p] for p in range(P)]) <= 
            (availability[M-1] + availability[M-2])), "CombinedMachineAvailability"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')