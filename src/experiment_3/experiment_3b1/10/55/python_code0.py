import pulp
import json

# Load the data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

# Problem setup
problem = pulp.LpProblem("Auto_Parts_Manufacturer_Problem", pulp.LpMaximize)

# Decision Variables
P = len(data['prices'])  # Number of different parts
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))

# Calculate total production time
total_time = pulp.lpSum(
    data['time_required'][m][p] * x[p] for m in range(len(data['time_required'])) for p in range(P)
)

# Labor cost calculation
labor_cost = pulp.lpSum([
    data['standard_cost'] * data['overtime_hour'] if total_time <= data['overtime_hour'] 
    else data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (total_time - data['overtime_hour'])
])

# Full objective
total_profit = profit - pulp.lpSum(data['machine_costs'][m] * total_time for m in range(len(data['machine_costs']))) - labor_cost
problem += total_profit

# Constraints

# Machine Availability Constraints
M = len(data['availability'])  # Number of different machines
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m], f"Availability_Constraint_{m}"

# Minimum Batches Requirement
for p in range(P):
    problem += x[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}"

# Minimum Profit Requirement
problem += total_profit >= data['min_profit'], "Min_Profit_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')