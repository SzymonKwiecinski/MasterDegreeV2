import pulp
import json

# Data provided in JSON format
data = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10]
}'''

data = json.loads(data)

# Define decision variables
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches produced for each part
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

# Objective function
profit_terms = [
    (data['prices'][p] - sum(data['time_required[m][p]'] * data['machine_costs'][m] for m in range(M))) * x[p]
    for p in range(P)
]
problem += pulp.lpSum(profit_terms), "Total_Profit"

# Machine availability constraints
for m in range(M - 2):
    problem += (pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]), f"Machine_Availability_{m+1}"

# For machines M and M-1, combining availability
problem += (pulp.lpSum(data['time_required[M-1][p]'] * x[p] for p in range(P)) + 
             pulp.lpSum(data['time_required[M][p]'] * x[p] for p in range(P)) <= 
             data['availability'][M-1] + data['availability'][M]), "Combined_Machine_Availability"

# Minimum batch requirements
for p in range(P):
    problem += (x[p] >= data['min_batches'][p]), f"Min_Batches_{p+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')