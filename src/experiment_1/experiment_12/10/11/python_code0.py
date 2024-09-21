import pulp

# Data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Problem setup
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0) for t in range(N)]  # Quantity of goods bought
S = [pulp.LpVariable(f'S_{t}', lowBound=0) for t in range(N)]  # Quantity of goods sold
I = [pulp.LpVariable(f'I_{t}', lowBound=0) for t in range(N)]  # Inventory level

# Objective Function
profit = pulp.lpSum(prices[t] * S[t] - costs[t] * B[t] - holding_cost * I[t] for t in range(N))
problem += profit

# Constraints
problem += (I[0] == 0)  # Initial inventory constraint

for t in range(N):
    if t > 0:
        problem += (I[t] == I[t-1] + B[t] - S[t])  # Inventory balance constraint
    problem += (I[t] <= capacity)  # Storage capacity constraint

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')