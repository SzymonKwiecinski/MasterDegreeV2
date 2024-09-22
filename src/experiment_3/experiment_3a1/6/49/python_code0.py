import pulp
import json

# Data provided in the JSON format
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10]
}'''
data = json.loads(data_json)

# Parameters
time_required = data['time_required']  # Time required on each machine for each part
machine_costs = data['machine_costs']  # Cost of using each machine per hour
availability = data['availability']  # Available hours for each machine
prices = data['prices']  # Selling price per batch of each part
min_batches = data['min_batches']  # Minimum batches to produce for each part

# Number of machines and parts
num_machines = len(machine_costs)
num_parts = len(prices)

# Create the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) for m in range(num_machines))

problem += profit, "Total_Profit"

# Constraints
# Machine availability constraints
for m in range(num_machines):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m], 
                   f"Machine_Availability_Constraint_{m}")

# Minimum production requirements
for p in range(num_parts):
    problem += (batches[p] >= min_batches[p], f"Min_Production_Requirement_{p}")

# Solve the problem
problem.solve()

# Output results
batches_produced = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

print(f'Batches produced for each part: {batches_produced}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')