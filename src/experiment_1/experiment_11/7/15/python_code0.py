import pulp
import json

# Data in JSON format
data = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10]
}'''

# Load the data
data = json.loads(data)

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines
TimeRequired = data['time_required']  # Time required for each machine and part
MachineCosts = data['machine_costs']  # Cost associated with each machine
Availability = data['availability']  # Availability of each machine
Prices = data['prices']  # Selling prices for each part
MinBatches = data['min_batches']  # Minimum number of batches for each part

# Create the Linear Programming Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum([Prices[p] * x[p] for p in range(P)]) - \
         pulp.lpSum([MachineCosts[m] * pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) for m in range(M)])

problem += profit, "Total_Profit"

# Constraints
# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) <= Availability[m], f"Machine_{m+1}_Availability"

# Minimum production requirement
for p in range(P):
    problem += x[p] >= MinBatches[p], f"Min_Batches_{p+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')