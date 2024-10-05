import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
}

num_parts = len(data['prices'])
num_machines = len(data['machine_costs'])

# Create the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f"batches_{p}", lowBound=data['min_batches'][p], cat='Continuous') for p in range(num_parts)]

# Objective function
revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(num_parts))
cost = pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] 
                  for m in range(num_machines) for p in range(num_parts))

problem += revenue - cost, "Total Profit"

# Constraints
# Machine constraints for machines 1 to M-2
for m in range(num_machines - 2):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(num_parts)) <= data['availability'][m], f"Machine_{m+1}_Constraint"

# Combined constraint for the last two machines
problem += (
    pulp.lpSum(data['time_required'][num_machines - 2][p] * batches[p] for p in range(num_parts)) +
    pulp.lpSum(data['time_required'][num_machines - 1][p] * batches[p] for p in range(num_parts)) <= 
    data['availability'][num_machines - 2] + data['availability'][num_machines - 1],
    "Combined_Machine_Constraint"
)

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')