import pulp
import json

# Input data
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
num_products = data['NumProducts']
quantity = pulp.LpVariable.dicts("quantity", range(num_products), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in range(num_products)), "Total_Profit"

# Constraints
for s in range(data['NumMachines']):
    problem += (pulp.lpSum(data['ProduceTime'][k][s] * quantity[k] for k in range(num_products)) <= data['AvailableTime'][s]), f"Time_Constraint_Machine_{s}"

# Solve the problem
problem.solve()

# Output
output = {
    "quantity": [quantity[k].varValue for k in range(num_products)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')