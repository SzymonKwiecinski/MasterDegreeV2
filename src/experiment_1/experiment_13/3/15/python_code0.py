import pulp
import json

# Load data from JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Define parameters
time_required = data['time_required']  # Time required to produce one batch of part p on machine m
machine_costs = data['machine_costs']  # Cost associated with using machine m
availability = data['availability']      # Availability of machine m per month
prices = data['prices']                  # Selling price of one batch of part p
min_batches = data['min_batches']        # Minimum number of batches of part p to be produced

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(prices[p] * x[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M))
problem += profit

# Constraints
# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m}"

# Minimum production requirement
for p in range(P):
    problem += x[p] >= min_batches[p], f"MinBatches_Constraint_{p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')