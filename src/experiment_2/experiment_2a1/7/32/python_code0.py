import json
import pulp

# Input data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Extracting input data
num_products = data['NumProducts']
num_machines = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: quantity of each product to produce
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Integer') for k in range(num_products)]

# Objective function: maximize total profit
problem += pulp.lpSum(profit[k] * quantities[k] for k in range(num_products)), "Total_Profit"

# Constraints: production time for each machine
for s in range(num_machines):
    problem += (pulp.lpSum(produce_time[k][s] * quantities[k] for k in range(num_products)) <= available_time[s]), f"Machine_{s}_Time_Constraint")

# Solve the problem
problem.solve()

# Output the quantities produced
quantities_output = {f'quantity_{k}': quantities[k].varValue for k in range(num_products)}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Optionally, you can print the quantities
print(json.dumps({"quantity": list(quantities_output.values())}))