import pulp
import json

# Input data
data_json = """{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10]
}"""

data = json.loads(data_json)

# Parameters
P = len(data["prices"])  # Number of parts
M = len(data["machine_costs"])  # Number of machines
TimeRequired = data["time_required"]  # Time required to produce one batch of part p on machine m
MachineCosts = data["machine_costs"]  # Cost associated with using machine m
Availability = data["availability"]  # Availability of machine m per month
Prices = data["prices"]  # Selling price of one batch of part p
MinBatches = data["min_batches"]  # Minimum number of batches of part p to be produced

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(Prices[p] * x[p] for p in range(P)) - \
           pulp.lpSum(MachineCosts[m] * pulp.lpSum(TimeRequired[m][p] * x[p] for p in range(P)) for m in range(M))

# Constraints

# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum(TimeRequired[m][p] * x[p] for p in range(P)) <= Availability[m], f"Availability_Constraint_{m}"

# Minimum production requirement
for p in range(P):
    problem += x[p] >= MinBatches[p], f"MinBatches_Constraint_{p}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')