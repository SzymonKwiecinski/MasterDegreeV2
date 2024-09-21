import pulp

# Data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0)  # Quantity bought in period t
S = pulp.LpVariable.dicts("S", range(N), lowBound=0)  # Quantity sold in period t
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, upBound=capacity)  # Inventory level at the end of period t

# Objective Function
profit = pulp.lpSum(price[t] * S[t] - cost[t] * B[t] - holding_cost * I[t] for t in range(N))
problem += profit

# Constraints
# Inventory balance constraint
problem += (I[0] == 0)  # Initial inventory
for t in range(1, N):
    problem += (I[t] == I[t-1] + B[t] - S[t])

# Non-negativity and capacity constraints
for t in range(N):
    problem += (I[t] >= 0)  # Non-negative inventory
    problem += (S[t] >= 0)  # Non-negative sales
    problem += (B[t] >= 0)  # Non-negative purchases
    problem += (I[t] <= capacity)  # Storage capacity

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')