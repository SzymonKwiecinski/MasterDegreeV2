import pulp

# Data provided
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

C = data['capacity']
H = data['holding_cost']
P = data['price']
C_cost = data['cost']

N = len(P)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Variables
b = pulp.LpVariable.dicts("buy", range(N), lowBound=0, cat='Continuous')  # Buy quantities
s = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')  # Sell quantities
x = pulp.LpVariable.dicts("stock", range(N), lowBound=0, cat='Continuous')  # Stock levels

# Objective function
problem += pulp.lpSum(P[n] * s[n] - C_cost[n] * b[n] - H * x[n] for n in range(N)), "Total_Profit"

# Constraints
# Stock balance for each period
for n in range(N):
    if n == 0:
        problem += x[n] == b[n] - s[n], f"Stock_Balance_{n+1}"
    else:
        problem += x[n] == x[n-1] + b[n] - s[n], f"Stock_Balance_{n+1}"
    
    # Capacity constraint
    problem += x[n] <= C, f"Capacity_Constraint_{n+1}"

# Final stock should be zero
problem += x[N-1] == 0, "Final_Stock_Zero"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')