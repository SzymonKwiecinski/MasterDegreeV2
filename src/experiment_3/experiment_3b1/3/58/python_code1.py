import pulp
import json

# Data from the provided JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Parameters
P = len(data['prices'])  # Number of different parts
M = len(data['machine_costs'])  # Number of different machines

# Create the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective Function
profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - pulp.lpSum(
    [data['machine_costs'][m] * (
        pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) + 
        pulp.lpSum(setup_flag[p] * data['setup_time'][p] for p in range(P) if m == 0)) 
    ) for m in range(M)]
)

problem += profit

# Constraints for machine time availability
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m]

# Setup time constraint for machine 1
problem += pulp.lpSum(setup_flag[p] * data['setup_time'][p] for p in range(P)) <= data['availability'][0]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')