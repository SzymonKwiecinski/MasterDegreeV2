import pulp
import json

# Data provided in JSON format
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10], 
    "extra_costs": [0, 15, 22.5], 
    "max_extra": [0, 80, 80]
}'''

# Load data
data = json.loads(data_json)

# Define sets
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create a problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)  # batches for parts
extra = pulp.LpVariable.dicts("extra", range(M), lowBound=0)  # extra hours for machines

# Objective function
profit = pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) \
         - pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) for m in range(M)) \
         - pulp.lpSum(data['extra_costs'][m] * extra[m] for m in range(M))

problem += profit, "Total_Profit"

# Constraints
# Machine availability
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) + extra[m] <= data['availability'][m] + data['max_extra'][m]), f"Availability_Constraint_{m}"

# Minimum production requirements
for p in range(P):
    problem += (b[p] >= data['min_batches'][p]), f"Min_Production_Constraint_{p}"

# Extra time constraints
for m in range(M):
    problem += (extra[m] >= 0, f"Extra_Nonnegativity_Constraint_{m}")
    problem += (extra[m] <= data['max_extra'][m], f"Max_Extra_Constraint_{m}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')