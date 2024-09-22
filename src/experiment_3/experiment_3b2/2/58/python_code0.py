import pulp
import json

# Data provided in JSON format
data = '{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}'
data = json.loads(data)

# Extracting data from the loaded JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Define sets and indices
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines
Large = max(availability)  # A large number for binary constraints

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * time_required[m][p] * batches[p] for m in range(M) for p in range(P)) - \
         pulp.lpSum(machine_costs[0] * setup_time[p] * setup_flag[p] for p in range(P))

problem += profit

# Constraints
# Availability constraints for each machine
for m in range(M):
    if m == 0:
        problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                     pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P))) <= availability[m]
    else:
        problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m])

# Binary setup indicator constraint
for p in range(P):
    problem += batches[p] <= Large * setup_flag[p]

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')