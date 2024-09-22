import pulp

# Data from the provided JSON
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
C = data['capacity']
h = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Create the Linear Programming problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision variables
b = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')  # Buying amounts
s = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')  # Selling amounts
x = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')  # Stock amounts

# Objective Function
problem += pulp.lpSum(prices[n] * s[n] - costs[n] * b[n] - h * x[n] for n in range(N)), "Total_Profit"

# Constraints

# Initial stock condition
problem += (x[0] == 0, "Initial_Stock")

# Stock balance constraints
for n in range(N):
    if n == 0:
        problem += (x[n] == b[n] - s[n], f"Stock_Balance_{n}")
    else:
        problem += (x[n] == x[n-1] + b[n] - s[n], f"Stock_Balance_{n}")

# Capacity constraints
for n in range(N):
    problem += (x[n] <= C, f"Capacity_Constraint_{n}")

# Final stock condition
problem += (x[N-1] == 0, "Final_Stock")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')