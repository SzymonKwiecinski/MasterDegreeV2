from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

# Parse data
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}
num_products = data['NumProducts']
num_machines = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Define the LP problem
problem = LpProblem("Profit_Maximization", LpMaximize)

# Define decision variables
quantities = [LpVariable(f"quantity_{k}", lowBound=0) for k in range(num_products)]

# Objective function
problem += lpSum(profit[k] * quantities[k] for k in range(num_products)), "Total_Profit"

# Constraints
for s in range(num_machines):
    problem += lpSum(produce_time[k][s] * quantities[k] for k in range(num_products)) <= available_time[s], f"Machine_{s}_Capacity"

# Solve the problem
problem.solve()

# Output results
output = {
    "quantity": [value(quantities[k]) for k in range(num_products)]
}

print(output)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>') 