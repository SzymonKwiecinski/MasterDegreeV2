import pulp

# Define the data
data = {
    "available": [240000, 8000, 75000],
    "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    "prices": [40, 38, 9],
    "costs": [30, 26, 7],
    "demands": [10000, 2000, 10000]
}

# Unpack the data
available = data["available"]
requirements = data["requirements"]
prices = data["prices"]
costs = data["costs"]
demands = data["demands"]

# Number of products and materials
M = len(prices)  # Number of products
N = len(available)  # Number of materials

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'product_{j}', lowBound=0, upBound=demands[j], cat='Integer') for j in range(M)]

# Add objective function (maximize profit)
profit = sum((prices[j] - costs[j]) * x[j] for j in range(M))
problem += profit

# Add constraints for raw materials
for i in range(N):
    problem += sum(requirements[j][i] * x[j] for j in range(M)) <= available[i]

# Solve the problem
problem.solve()

# Collect the results
amount_produced = [pulp.value(x[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

# Print the solution
print({
    "amount": amount_produced,
    "total_profit": total_profit
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')