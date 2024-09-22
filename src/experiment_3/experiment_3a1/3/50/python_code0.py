import pulp
import json

# Input data in JSON format
data = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10],
    "extra_costs": [0, 15, 22.5],
    "max_extra": [0, 80, 80]
}'''

# Load the data
params = json.loads(data)

# Set up the problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Decision Variables
P = len(params['prices'])  # Number of parts
M = len(params['machine_costs'])  # Number of machines

batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra = pulp.LpVariable.dicts("extra", range(M), lowBound=0)

# Objective Function
profit = pulp.lpSum(params['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(params['extra_costs'][m] * extra[m] for m in range(M))
problem += profit, "Total_Profit"

# Constraints

# Time constraints for each machine
for m in range(M):
    problem += (pulp.lpSum(params['time_required'][m][p] * batches[p] for p in range(P)) <=
                 params['availability'][m] + extra[m]), f"Time_Constraint_{m}"

# Minimum production requirements
for p in range(P):
    problem += (batches[p] >= params['min_batches'][p]), f"Min_Production_{p}"

# Extra time purchase limits
for m in range(M):
    problem += (extra[m] <= params['max_extra'][m]), f"Max_Extra_{m}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')