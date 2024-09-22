import pulp
import json

data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

# Extract data from the input
K = data['NumParts']
S = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Create the 'prob' variable to contain the problem data
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create decision variables
quantities = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Continuous')

# Define the objective function
problem += pulp.lpSum(profit[k] * quantities[k] for k in range(K)), "Total_Profit"

# Define constraints based on machine capacity
for s in range(S):
    problem += (pulp.lpSum(time[k][s] * quantities[k] for k in range(K)) <= capacity[s]), f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "quantity": [quantities[k].varValue for k in range(K)]
}

# Print the result
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')