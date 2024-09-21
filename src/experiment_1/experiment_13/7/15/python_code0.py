import pulp
import json

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])
M = len(data['machine_costs'])
TimeRequired = data['time_required']
MachineCosts = data['machine_costs']
Availability = data['availability']
Prices = data['prices']
MinBatches = data['min_batches']

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum([Prices[p] * x[p] for p in range(P)]) - pulp.lpSum(
    [MachineCosts[m] * pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) for m in range(M)]
)
problem += profit, "Total_Profit"

# Constraints
for m in range(M):
    problem += pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) <= Availability[m], f"Machine_Availability_{m+1}"

for p in range(P):
    problem += x[p] >= MinBatches[p], f"Min_Batches_{p+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')