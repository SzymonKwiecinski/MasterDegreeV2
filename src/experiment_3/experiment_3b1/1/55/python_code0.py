import json
import pulp

# Data provided in the JSON format
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

# Model parameters
num_parts = len(data['prices'])
num_machines = len(data['machine_costs'])
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Create the linear programming problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0)

# Objective function
labor_hours = pulp.lpSum(time_required[0][p] * batches[p] for p in range(num_parts))  # Using Machine 1
labor_cost = pulp.lpSum([
    standard_cost * labor_hours,
    overtime_cost * (labor_hours - overtime_hour) if labor_hours > overtime_hour else 0
])
total_profit = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts)) - \
               pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) for m in range(num_machines)) - labor_cost

problem += total_profit, "Total_Profit"

# Constraints
# Batch production constraints
for p in range(num_parts):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Machine availability constraints
for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m], f"Machine_Availability_{m}"

# Profit constraint
problem += total_profit >= min_profit, "Min_Profit_Constraint"

# Solve the problem
problem.solve()

# Display the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')