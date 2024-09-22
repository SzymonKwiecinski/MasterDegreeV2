import pulp
import json

# Data provided
data = json.loads('{"NumParts": 5, "NumMachines": 2, "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "Profit": [30, 20, 40, 25, 10], "Capacity": [700, 1000]}')

# Sets
K = range(data['NumParts'])
S = range(data['NumMachines'])

# Parameters
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantity = pulp.LpVariable.dicts("quantity", K, lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in K), "Total_Profit"

# Constraints
for s in S:
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in K) <= capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output results
quantities = [quantity[k].varValue for k in K]
print(f'Optimal Quantities: {quantities}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')