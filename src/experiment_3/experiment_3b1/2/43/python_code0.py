import pulp
import json

# Data in JSON format
data = json.loads('{"available": [240000, 8000, 75000], "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]], "prices": [40, 38, 9], "costs": [30, 26, 7], "demands": [10000, 2000, 10000]}')

# Parameters
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create the problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([(prices[j] - costs[j]) * x[j] for j in range(M)]), "Total_Profit"

# Raw material constraints
for i in range(N):
    problem += pulp.lpSum([requirements[i][j] * x[j] for j in range(M)]) <= available[i], f"RawMaterialConstraint_{i}"

# Demand constraints
for j in range(M):
    problem += x[j] <= demands[j], f"DemandConstraint_{j}"

# Solve the problem
problem.solve()

# Print results
for j in range(M):
    print(f'Amount produced of product {j+1}: {x[j].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')