import pulp
import json

# Input data
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Extracting parameters for convenience
num_products = data['NumProducts']
num_machines = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = pulp.LpVariable.dicts("Quantity", range(num_products), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(num_products)), "Total_Profit"

# Constraints
for s in range(num_machines):
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(num_products)) <= available_time[s], f"Time_Constraint_Machine_{s}"

# Solve the problem
problem.solve()

# Output results
result = {
    "quantity": [quantity[k].varValue for k in range(num_products)]
}

print(json.dumps(result))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')