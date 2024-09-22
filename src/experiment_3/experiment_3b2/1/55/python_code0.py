import pulp
import json

# Data from the JSON format
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define variables
num_parts = len(data['prices'])
x = pulp.LpVariable.dicts("x", range(num_parts), lowBound=data['min_batches'], cat='Continuous')

# Define Labor Cost for Machine 1
time_1 = data['time_required'][0]
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']

# Objective function
profit_expr = pulp.lpSum(data['prices'][p] * x[p] for p in range(num_parts))
cost_expr = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(num_parts)) for m in range(len(data['machine_costs'])))
labor_cost = pulp.lpSum(standard_cost * pulp.lpSum(time_1[p] * x[p] for p in range(num_parts)) if pulp.lpSum(time_1[p] * x[p] for p in range(num_parts)) <= overtime_hour else (standard_cost * overtime_hour + overtime_cost * (pulp.lpSum(time_1[p] * x[p] for p in range(num_parts)) - overtime_hour)))

problem += profit_expr - cost_expr - labor_cost, "Total_Profit"

# Constraints
# Machine availability constraints
for m in range(1, len(data['availability'])):  # Skip first machine as it's tested separately
    problem += pulp.lpSum(data['time_required[m][p]'] * x[p] for p in range(num_parts)) <= data['availability'][m], f"Available_Machine_{m}"

# Overtime constraint for machine 1
problem += pulp.lpSum(time_1[p] * x[p] for p in range(num_parts)) <= overtime_hour, "Overtime_Hours_Machine_1"

# Minimum profit constraint
problem += profit_expr - cost_expr - labor_cost >= data['min_profit'], "Minimum_Profit"

# Non-negativity constraints (already included in variable definition)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')