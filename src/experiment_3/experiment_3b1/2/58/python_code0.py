import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Parameters
P = len(data['prices'])
M = len(data['machine_costs'])

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + 
                                                 pulp.lpSum(setup_flags[p] * data['setup_time'][p] for p in range(P))) 
                  for m in range(M))

problem += profit

# Constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + 
                 pulp.lpSum(setup_flags[p] * data['setup_time'][p] for p in range(P))) <= data['availability'][m], f"Machine_Availability_{m}")

# Linking setup_flags to batches
for p in range(P):
    problem += setup_flags[p] >= (batches[p] > 0), f"Setup_Flag_Constraint_{p}"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')