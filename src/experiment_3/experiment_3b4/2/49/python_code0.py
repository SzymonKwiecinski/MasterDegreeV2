import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(len(data['prices']))]

# Objective Function
total_revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(len(data['prices'])))
total_cost = pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] 
                        for m in range(len(data['machine_costs'])) 
                        for p in range(len(data['prices'])))

problem += total_revenue - total_cost, "Total_Profit"

# Constraints
# Minimum Batch Requirement
for p in range(len(data['prices'])):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}"

# Machine Availability Constraints
for m in range(len(data['machine_costs']) - 2):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(len(data['prices'])))
                <= data['availability'][m]), f"Availability_Constraint_{m}"

# Shared availability for last two machines
problem += (pulp.lpSum(data['time_required'][len(data['machine_costs'])-1][p] * batches[p] for p in range(len(data['prices']))) + 
            pulp.lpSum(data['time_required'][len(data['machine_costs'])-2][p] * batches[p] for p in range(len(data['prices'])))
            <= data['availability'][len(data['machine_costs'])-1] + data['availability'][len(data['machine_costs'])-2]), "Shared_Availability_Constraint"

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')