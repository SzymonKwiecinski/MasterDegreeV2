import pulp
import json

# Data from the provided JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision Variables
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
extra = pulp.LpVariable.dicts("extra", range(M), lowBound=0, upBound=data['max_extra'], cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
costs = pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra[m]) for m in range(M))
extra_costs = pulp.lpSum(data['extra_costs'][m] * extra[m] for m in range(M))
problem += profit - costs - extra_costs, "Total_Profit"

# Constraints
# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra[m], f"Availability_Constraint_{m}"

# Minimum Batches Requirement
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}"

# Solve the problem
problem.solve()

# Output results
for p in range(P):
    print(f'Batches for part {p + 1}: {batches[p].varValue}')
for m in range(M):
    print(f'Extra hours for machine {m + 1}: {extra[m].varValue}')
    
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')