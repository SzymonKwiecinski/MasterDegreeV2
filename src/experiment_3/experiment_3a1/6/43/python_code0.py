import pulp

# Data from the provided JSON
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Extracting data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']
M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function
profit = pulp.lpSum((prices[j] - costs[j]) * amounts[j] for j in range(M))
problem += profit

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * amounts[j] for j in range(M)) <= available[i]

# Constraints for demand
for j in range(M):
    problem += amounts[j] <= demands[j]

# Solve the problem
problem.solve()

# Print the output
for j in range(M):
    print(f'Optimal amount of product {j}: {amounts[j].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')