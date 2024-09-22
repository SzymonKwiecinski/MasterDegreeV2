import pulp
import json

# Input data
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

# Extracting data from the input
NumParts = data['NumParts']
NumMachines = data['NumMachines']
Time = data['Time']
Profit = data['Profit']
Capacity = data['Capacity']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = pulp.LpVariable.dicts("quantity", range(NumParts), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(Profit[k] * quantity[k] for k in range(NumParts)), "Total_Profit"

# Constraints
for s in range(NumMachines):
    problem += pulp.lpSum(Time[k][s] * quantity[k] for k in range(NumParts)) <= Capacity[s], f"Capacity_Constraint_Shop_{s+1}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "quantity": [quantity[k].varValue for k in range(NumParts)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')