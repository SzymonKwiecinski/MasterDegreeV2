import pulp

# Data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

N = len(data['price'])  # Number of periods
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

# Create the LP problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([price[t] * S[t] - cost[t] * B[t] - holding_cost * I[t] for t in range(N)])

# Constraints
# Initial inventory
problem += I[0] == 0

for t in range(N):
    problem += I[t] <= capacity  # Storage capacity
    if t > 0:
        problem += I[t] == I[t-1] + B[t] - S[t]  # Inventory balance
    else:
        problem += I[t] == B[t] - S[t]  # First period balance specific case

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')