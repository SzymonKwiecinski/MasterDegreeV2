import pulp
import json

# Load data from the provided JSON format
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}")

# Extract data for easier access
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Initialize the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Variables: number of batches produced for each part
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] - pulp.lpSum(machine_costs[m] * (time_required[m][p] / 100) * batches[p] for m in range(M)) for p in range(P))
problem += profit, "Total_Profit"

# Constraints

# Machine availability constraints
problem += pulp.lpSum(pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)) <= pulp.lpSum(availability), "Machine_Availability"

# Minimum production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p+1}"

# Solve the problem
problem.solve()

# Print the results
for p in range(P):
    print(f'Batches produced for part {p+1}: {batches[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')