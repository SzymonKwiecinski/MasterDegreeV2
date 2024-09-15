import pulp

# Data from JSON
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

# Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0)  # Quantity of goods bought
S = pulp.LpVariable.dicts("S", range(N), lowBound=0)  # Quantity of goods sold
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, upBound=capacity)  # Inventory level

# Objective Function
problem += pulp.lpSum(price[t] * S[t] - cost[t] * B[t] - holding_cost * I[t] for t in range(N))

# Constraints
for t in range(N):
    # Inventory balance
    if t == 0:
        problem += I[t] == B[t] - S[t]  # Initial inventory is 0
    else:
        problem += I[t] == I[t-1] + B[t] - S[t]  # Inventory balance for t > 0

    # Non-negativity constraints are already defined in the variable bounds
    problem += I[t] >= 0
    problem += S[t] >= 0
    problem += B[t] >= 0
    problem += I[t] <= capacity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')