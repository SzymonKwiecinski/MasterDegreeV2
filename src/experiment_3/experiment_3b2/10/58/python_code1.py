import pulp
import json

# Data in JSON format
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "setup_time": [12, 8, 4, 0]
}'''
data = json.loads(data_json)

# Sets and indices
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) \
         - pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] 
                      for m in range(M) for p in range(P)) \
         - pulp.lpSum(data['setup_time'][p] * setup_flags[p] * data['machine_costs'][0] for p in range(P))

problem += profit

# Constraints

# Machine Availability
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) +
                 (pulp.lpSum(data['setup_time'][p] * setup_flags[p] for p in range(P)) if m == 0 else 0) 
                 <= data['availability'][m]), f"Availability_Constraint_{m}")

# Linking setup flags to production
U = 1000  # Example upper limit for production
for p in range(P):
    problem += (batches[p] <= U * setup_flags[p], f"Linking_Constraint_{p}")

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')