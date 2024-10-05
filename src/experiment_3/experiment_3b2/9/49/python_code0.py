import pulp
import json

# Data Parsing
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Variables
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)  # Number of products
M = len(machine_costs)  # Number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum(prices[p] * x[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M))
problem += profit

# Constraints
# Machine availability constraints for m = 1, ..., M-2
for m in range(M-2):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

# Combined availability constraint for Machine M and Machine M-1
problem += (pulp.lpSum(time_required[M-1][p] * x[p] for p in range(P)) + 
            pulp.lpSum(time_required[M-2][p] * x[p] for p in range(P))) <= (availability[M-1] + availability[M-2])

# Minimum production requirements
for p in range(P):
    problem += x[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')