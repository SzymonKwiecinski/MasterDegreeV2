import pulp
import json

# Input data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Extracting data from the input
K = data['NumProducts']  # Number of products
S = data['NumMachines']   # Number of stages (machines)
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Integer') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total Profit"

# Constraints
for s in range(S):
    problem += (pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= available_time[s]), f"Available_Time_Stage_{s+1}"

# Solve the problem
problem.solve()

# Output the production quantities
output = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')