import pulp
import json

# Data provided in JSON format
data = json.loads('{"processing_times": {"central": {"isolate": [10, 6, 8], "scan": [6, 4, 6]}, "distributed": {"isolate": [12, 9, 12], "scan": [18, 10, 15]}}, "costs": {"central": 150, "distributed": 70}, "max_hours": {"central_max_hours": 16, "distributed_max_hours": 33}}')

# Extracting data from JSON
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

N = len(processing_times['central']['isolate'])

# Create the linear programming problem
problem = pulp.LpProblem("Network_Intrusion_Intervention", pulp.LpMinimize)

# Decision Variables
central_isolate = pulp.LpVariable.dicts("x_central_isolate", range(N), cat='Binary')
central_scan = pulp.LpVariable.dicts("x_central_scan", range(N), cat='Binary')
distributed_isolate = pulp.LpVariable.dicts("x_distributed_isolate", range(N), cat='Binary')
distributed_scan = pulp.LpVariable.dicts("x_distributed_scan", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum(costs['central'] * (processing_times['central']['isolate'][i] * central_isolate[i] + 
                                            processing_times['central']['scan'][i] * central_scan[i]) 
                       + costs['distributed'] * (processing_times['distributed']['isolate'][i] * distributed_isolate[i] + 
                                                  processing_times['distributed']['scan'][i] * distributed_scan[i]) 
                       for i in range(N))

# Constraints
problem += pulp.lpSum(processing_times['central']['isolate'][i] * central_isolate[i] + 
                      processing_times['central']['scan'][i] * central_scan[i] for i in range(N)) <= max_hours['central_max_hours']

problem += pulp.lpSum(processing_times['distributed']['isolate'][i] * distributed_isolate[i] + 
                      processing_times['distributed']['scan'][i] * distributed_scan[i] for i in range(N)) <= max_hours['distributed_max_hours']

for i in range(N):
    problem += central_isolate[i] + central_scan[i] + distributed_isolate[i] + distributed_scan[i] == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')