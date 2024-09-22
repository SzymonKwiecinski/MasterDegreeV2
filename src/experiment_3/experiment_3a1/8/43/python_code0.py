import pulp
import json

# Data provided in JSON format
data = json.loads('{"available": [240000, 8000, 75000], "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]], "prices": [40, 38, 9], "costs": [30, 26, 7], "demands": [10000, 2000, 10000]}')

# Extracting data from JSON
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create the linear programming problem
problem = pulp.LpProblem("WildSportsProfitMaximization", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)  # x_j >= 0

# Objective function: Maximize total profit
profit = pulp.lpSum((prices[j] - costs[j]) * x[j] for j in range(M))
problem += profit

# Adding raw material constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i]

# Adding demand constraints
for j in range(M):
    problem += x[j] <= demands[j]

# Solve the problem
problem.solve()

# Print results
for j in range(M):
    print(f'Product {j+1} production amount: {x[j].varValue}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')