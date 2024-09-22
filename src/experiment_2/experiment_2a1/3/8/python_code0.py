import pulp
import json

# Input data
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

# Problem parameters
K = data['NumParts']
S = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = pulp.LpVariable.vector("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output results
output_quantity = [quantity[k].varValue for k in range(K)]
print(json.dumps({"quantity": output_quantity}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')