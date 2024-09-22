import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective Function
profit_expr = (pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) -
                pulp.lpSum(data['machine_costs'][m] * 
                            (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) +
                             pulp.lpSum(setup_flag[p] * data['setup_time'][p] * (1 - (1 if m == 0 else 0)) for p in range(P)))
                            for m in range(M)))
problem += profit_expr

# Constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) +
                 pulp.lpSum(setup_flag[p] * data['setup_time'][p] * (1 - (1 if m == 0 else 0)) for p in range(P)) <= data['availability'][m])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')