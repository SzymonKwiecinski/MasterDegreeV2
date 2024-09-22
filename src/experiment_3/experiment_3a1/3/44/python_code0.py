import pulp
import json

# Data provided in JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Extracting the data
time_required = data['time_required']  # Time required on machines for each part
machine_costs = data['machine_costs']  # Cost per hour for machines
availability = data['availability']  # Available hours for machines
prices = data['prices']  # Selling prices for parts
min_batches = data['min_batches']  # Minimum required batches for parts

# Number of parts (P) and machines (M)
P = len(prices)  # Number of different parts
M = len(machine_costs)  # Number of different machines

# Create the linear programming problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision variables: number of batches produced for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += profit, "Total_Profit"

# Constraints
# Machine time constraints
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_Time_Constraint_{m}")

# Minimum production requirements
for p in range(P):
    problem += (batches[p] >= min_batches[p], f"Min_Production_Requirement_{p}")

# Solve the problem
problem.solve()

# Output results
for p in range(P):
    print(f"Batches produced for part {p + 1}: {batches[p].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')