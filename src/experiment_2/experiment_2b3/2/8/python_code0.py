from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

# Parse the data
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Define the LP problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Define the decision variables
quantity = [LpVariable(f"quantity_{k}", lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective function
problem += lpSum(profit[k] * quantity[k] for k in range(num_parts))

# Constraints
for s in range(num_machines):
    problem += lpSum(time[k][s] * quantity[k] for k in range(num_parts)) <= capacity[s]

# Solve the problem
problem.solve()

# Gather the results
results = {
    "quantity": [value(quantity[k]) for k in range(num_parts)]
}

# Print the results
print(results)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')