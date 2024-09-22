import pulp
import json

# Data from JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Indices
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                                          (setup_time[p] * setup_flag[p] if m == 0 else 0)) for m in range(M))

problem += profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
                 (pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P)) if m == 0 else 0)) <= availability[m])

# Setup constraint for machine 1
for p in range(P):
    problem += setup_flag[p] >= batches[p] / (batches[p] + 1) if batches[p] > 0 else 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')