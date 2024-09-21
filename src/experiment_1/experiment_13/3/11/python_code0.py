import pulp

# Data from the provided JSON format
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
N = len(data['price'])  # Number of periods
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision variables
B = pulp.LpVariable.dicts("Buy", range(N), lowBound=0)  # Quantity bought
S = pulp.LpVariable.dicts("Sell", range(N), lowBound=0)  # Quantity sold
I = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, upBound=capacity)  # Inventory levels

# Objective function
profit = pulp.lpSum(prices[t] * S[t] - costs[t] * B[t] - holding_cost * I[t] for t in range(N))
problem += profit

# Constraints
# Inventory balance and initial condition
problem += I[0] == 0  # Initial inventory
for t in range(N):
    if t > 0:
        problem += I[t] == I[t - 1] + B[t] - S[t]  # Inventory balance
    problem += I[t] >= 0  # Non-negative inventory
    problem += S[t] >= 0  # Non-negative sales
    problem += B[t] >= 0  # Non-negative purchases
    problem += I[t] <= capacity  # Storage capacity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')