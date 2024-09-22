import pulp

# Define data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'setup_time': [12, 8, 4, 0]
}
U = 1000  # Large upper bound for batches

# Number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective Function
objective = (
    pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
    - pulp.lpSum(data['machine_costs'][m] * (
        pulp.lpSum(data['time_required'][m][p] * batches[p] + (
            data['setup_time'][p] * setup_flag[p] if m == 0 else 0) for p in range(P))
    ) for m in range(M))
)
problem += objective

# Constraints
# Machine Time Constraints
for m in range(M):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * batches[p] + (
            data['setup_time'][p] * setup_flag[p] if m == 0 else 0) for p in range(P))
        <= data['availability'][m]
    )

# Setup Constraints
for p in range(P):
    problem += (setup_flag[p] >= batches[p] / U)

# Solve the problem
problem.solve()

# Print the Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')