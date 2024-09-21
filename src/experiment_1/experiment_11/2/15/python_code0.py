import pulp
import json

# Data input
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10]
}'''

# Load data
data = json.loads(data_json)

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines
TimeRequired = data['time_required']  # Time required for each machine-part combination
MachineCosts = data['machine_costs']  # Costs associated with each machine
Availability = data['availability']  # Availability of each machine
Prices = data['prices']  # Selling prices of each part
MinBatches = data['min_batches']  # Minimum batches required for each part

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum([Prices[p] * x[p] for p in range(P)]) - \
           pulp.lpSum([MachineCosts[m] * pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) for m in range(M)])

# Constraints
# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) <= Availability[m]

# Minimum production requirement
for p in range(P):
    problem += x[p] >= MinBatches[p]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')