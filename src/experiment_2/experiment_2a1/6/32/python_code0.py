import pulp
import json

# Input Data
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Extract parameters
K = data['NumProducts']
S = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= available_time[s], f"Available_Time_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the result
output = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')