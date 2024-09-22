import pulp
import json

data = json.loads('{"available": [240000, 8000, 75000], "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]], "prices": [40, 38, 9], "costs": [30, 26, 7], "demands": [10000, 2000, 10000]}')

# Extracting data from the loaded JSON
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function: Maximize total profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amounts[j] for j in range(M)])
problem += profit

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amounts[j] for j in range(M)]) <= available[i]

# Constraints for demand
for j in range(M):
    problem += amounts[j] <= demands[j]

# Solve the problem
problem.solve()

# Preparing the output
result = {
    "amount": [amounts[j].varValue for j in range(M)],
    "total_profit": pulp.value(problem.objective)
}

# Printing the result
print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')