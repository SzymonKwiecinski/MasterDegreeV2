import pulp
import json

# Data provided in JSON format
data = json.loads('{"M": 4, "N": 5, "Available": [10, 20, 15, 35, 25], "Requirements": [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], "Prices": [7, 10, 5, 9]}')

# Variables
M = data['M']
N = data['N']
available = data['Available']
req = data['Requirements']
price = data['Prices']

# Create the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function
problem += pulp.lpSum([price[j] * amount[j] for j in range(M)]), "Total_Revenue"

# Constraints
for i in range(N):
    problem += pulp.lpSum([req[j][i] * amount[j] for j in range(M)]) <= available[i], f"Raw_Material_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the optimal amount of each good
optimal_amounts = [amount[j].varValue for j in range(M)]
print("Optimal amounts of goods produced:", optimal_amounts)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')