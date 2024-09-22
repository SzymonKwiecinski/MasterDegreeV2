import pulp
import json

# Data input
data = json.loads('{"processing_times": {"central": {"isolate": [10, 6, 8], "scan": [6, 4, 6]}, "distributed": {"isolate": [12, 9, 12], "scan": [18, 10, 15]}}, "costs": {"central": 150, "distributed": 70}, "max_hours": {"central_max_hours": 16, "distributed_max_hours": 33}}')

# Parameters
N = len(data['processing_times']['central']['isolate'])
T_central = data['processing_times']['central']
T_distributed = data['processing_times']['distributed']
cost_central = data['costs']['central']
cost_distributed = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Define the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in ['isolate', 'scan']), cat='Binary')
y = pulp.LpVariable.dicts("y", ((i, j) for i in range(N) for j in ['isolate', 'scan']), cat='Binary')

# Objective function
problem += pulp.lpSum(x[i, j] * T_central[j][i] * cost_central + 
                       y[i, j] * T_distributed[j][i] * cost_distributed 
                       for i in range(N) for j in ['isolate', 'scan']), "Total_Cost"

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i, j] + y[i, j] for j in ['isolate', 'scan']) == 1, f"One_Intervention_Constraint_{i}"

problem += pulp.lpSum(x[i, 'isolate'] * T_central['isolate'][i] + x[i, 'scan'] * T_central['scan'][i] for i in range(N)) <= max_central, "Central_Time_Limit"
problem += pulp.lpSum(y[i, 'isolate'] * T_distributed['isolate'][i] + y[i, 'scan'] * T_distributed['scan'][i] for i in range(N)) <= max_distributed, "Distributed_Time_Limit"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')