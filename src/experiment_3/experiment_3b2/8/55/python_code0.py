import pulp
import json

# Load data from JSON format
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}")

# Define sets and indices
M = len(data['machine_costs'])  # Number of machines
P = len(data['prices'])  # Number of parts

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective function components
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))

cost_machines = pulp.lpSum(
    data['time_required'][m][p] * batches[p] * data['machine_costs'][m] 
    for m in range(1, M) for p in range(P)
)

time_machine1 = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))

standard_cost = pulp.lpMin(time_machine1, data['overtime_hour']) * data['standard_cost']
overtime_cost = pulp.lpMax(0, time_machine1 - data['overtime_hour']) * data['overtime_cost']

# Complete objective function
problem += profit - (cost_machines + standard_cost + overtime_cost), "Total_Profit"

# Constraints
# Machine availability constraints
for m in range(1, M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Availability_Constraint_{m}"

# Minimum batches constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}"

# Profit constraint
problem += profit - cost_machines - (standard_cost + overtime_cost) >= data['min_profit'], "Min_Profit_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')