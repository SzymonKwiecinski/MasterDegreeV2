import pulp

# Data from the problem
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extract data
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create the linear programming problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", (t for t in range(1, N + 1)), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("S", (t for t in range(1, N + 1)), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("I", (t for t in range(1, N + 1)), lowBound=0, cat='Continuous')

# Objective Function: Maximize total profit
problem += pulp.lpSum([price[t - 1] * S[t] - cost[t - 1] * B[t] - holding_cost * I[t] for t in range(1, N + 1)])

# Constraints
# Initial inventory constraint
problem += I[1] == B[1] - S[1]  # Initial inventory is zero, hence I_0 = 0

# Inventory balance constraints
for t in range(2, N + 1):
    problem += I[t] == I[t - 1] + B[t] - S[t]

# Storage capacity constraints
for t in range(1, N + 1):
    problem += I[t] <= capacity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')