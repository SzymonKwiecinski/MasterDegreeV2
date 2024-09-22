import pulp
import json

# Data input
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

# Extracting input data
K = data['NumParts']
S = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += (pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s]), f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Prepare the output
quantities = [quantity[k].varValue for k in range(K)]

output = {
    "quantity": quantities
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')