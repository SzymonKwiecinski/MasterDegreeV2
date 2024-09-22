import pulp
import json

# Input data in JSON format
data = '{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}'

# Load data from JSON
input_data = json.loads(data)

# Extracting data
time_required = input_data['time_required']
machine_costs = input_data['machine_costs']
availability = input_data['availability']
prices = input_data['prices']
min_batches = input_data['min_batches']
standard_cost = input_data['standard_cost']
overtime_cost = input_data['overtime_cost']
overtime_hour = input_data['overtime_hour']
min_profit = input_data['min_profit']

# Problem definition
P = len(prices)  # Number of products
M = len(machine_costs)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Machine time availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_Machine_{m}"

# Calculate total cost for labor on Machine 1
labor_cost = (pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)]) * standard_cost 
               + pulp.lpMax(0, pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)]) - overtime_hour) * (overtime_cost - standard_cost))

# Ensure profit exceeds minimum profit
problem += profit - labor_cost >= min_profit, "Min_Profit_Constraint"

# Solve the problem
problem.solve()

# Prepare output
batches_result = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')