import pulp
import json

# Data in JSON format
data = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "setup_time": [12, 8, 4, 0]
}'''

data = json.loads(data)

# Define parameters
time_required = data['time_required']  # M x P matrix
machine_costs = data['machine_costs']  # M array
availability = data['availability']      # M array
prices = data['prices']                  # P array
setup_time = data['setup_time']          # P array

M = len(machine_costs)  # Number of machines
P = len(prices)         # Number of parts

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)  # Number of batches produced
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')  # Setup flags

# Objective function
total_profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
               pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
               pulp.lpSum(setup_flags[p] * setup_time[p] * (1 if m == 0 else 0) for p in range(P))) for m in range(M))

problem += total_profit

# Constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                 pulp.lpSum(setup_flags[p] * setup_time[p] * (1 if m == 0 else 0) for p in range(P)) <= 
                 availability[m])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')