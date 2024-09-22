import pulp
import json

# Input data in JSON format
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Extracting data from the input
num_products = data['NumProducts']
num_machines = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Creating a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Defining decision variables for the quantity of each product to produce
quantity = pulp.LpVariable.dicts("quantity", range(num_products), lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(num_products)])

# Adding constraints for each machine (stage)
for s in range(num_machines):
    problem += pulp.lpSum([produce_time[k][s] * quantity[k] for k in range(num_products)]) <= available_time[s]

# Solving the problem
problem.solve()

# Preparing the output
output = {
    "quantity": [quantity[k].varValue for k in range(num_products)]
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# If you need to see the output structure:
print(json.dumps(output))