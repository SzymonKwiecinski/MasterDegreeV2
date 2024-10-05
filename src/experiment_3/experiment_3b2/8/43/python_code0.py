import pulp
import json

# Data
data = json.loads('{"available": [240000, 8000, 75000], "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]], "prices": [40, 38, 9], "costs": [30, 26, 7], "demands": [10000, 2000, 10000]}')

# Parameters
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of resources

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

# Objective function
problem += pulp.lpSum([(prices[j] - costs[j]) * x[j] for j in range(M)]), "Total_Profit"

# Constraints
# Resource constraints
for i in range(N):
    problem += (pulp.lpSum([requirements[i][j] * x[j] for j in range(M)]) <= available[i]), f"Resource_Constraint_{i+1}"

# Demand constraints
for j in range(M):
    problem += (x[j] <= demands[j]), f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')