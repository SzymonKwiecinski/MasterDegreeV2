import pulp
import json

# Load data from the provided JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Parameters
time_required = data['time_required']  # Time required to produce one batch of each part on each machine
machine_costs = data['machine_costs']  # Costs associated with using each machine
availability = data['availability']      # Availability of each machine per month
prices = data['prices']                  # Selling price of one batch of each part
min_batches = data['min_batches']        # Minimum number of batches for each part

# Problem Setup
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

# Objective Function
problem += pulp.lpSum(prices[p] * x[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M))

# Constraints
# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

# Minimum production requirement
for p in range(P):
    problem += x[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')