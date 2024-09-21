import pulp

# Data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
N = len(data['price'])

# Constants
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

# Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0) for t in range(N)]  # Purchases
S = [pulp.LpVariable(f'S_{t}', lowBound=0) for t in range(N)]  # Sales
I = [pulp.LpVariable(f'I_{t}', lowBound=0, upBound=capacity) for t in range(N)]  # Inventory

# Objective Function
problem += pulp.lpSum(price[t] * S[t] - cost[t] * B[t] - holding_cost * I[t] for t in range(N))

# Initial inventory constraint
problem += (I[0] == 0)

# Inventory balance and constraints
for t in range(1, N):
    problem += (I[t] == I[t-1] + B[t] - S[t])

# Non-negativity and storage capacity constraints
for t in range(N):
    problem += (I[t] >= 0)
    problem += (S[t] >= 0)
    problem += (B[t] >= 0)
    problem += (I[t] <= capacity)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')