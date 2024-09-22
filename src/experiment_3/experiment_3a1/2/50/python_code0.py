import pulp
import json

# Load data from JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Define variables
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Decision variables
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0)  # b_p
extra_hours = pulp.LpVariable.dicts("extra", range(M), lowBound=0)  # extra_m

# Objective function
profit = pulp.lpSum((data['prices'][p] * batches[p] - 
                     pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] 
                     for m in range(M)) - 
                     pulp.lpSum(data['extra_costs'][m] * extra_hours[m] for m in range(M))) 
                    for p in range(P))
problem += profit, "Total_Profit"

# Constraints
# Minimum batch requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}"

# Machine time availability
for m in range(M):
    problem += (pulp.lpSum(data['time_required[m][p]'] * batches[p] for p in range(P)) <= 
                 data['availability'][m] + extra_hours[m]), f"Machine_Time_Availability_{m}"

# Extra time limit
for m in range(M):
    problem += extra_hours[m] <= data['max_extra'][m], f"Extra_Time_Limit_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')