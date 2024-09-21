import pulp

# Problem data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Number of periods
N = len(data['price'])

# Create the Linear Programming problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f"B_{t}", lowBound=0, cat='Continuous') for t in range(N)]
S = [pulp.LpVariable(f"S_{t}", lowBound=0, cat='Continuous') for t in range(N)]
I = [pulp.LpVariable(f"I_{t}", lowBound=0, cat='Continuous') for t in range(N)]

# Objective Function
profit = [
    data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t]
    for t in range(N)
]
problem += pulp.lpSum(profit), "Total_Profit"

# Constraints
for t in range(N):
    # Non-negative inventory constraint
    problem += I[t] >= 0, f"Inventory_Non_Negative_{t}"

    # Non-negative sales constraint
    problem += S[t] >= 0, f"Sales_Non_Negative_{t}"

    # Non-negative purchases constraint
    problem += B[t] >= 0, f"Purchases_Non_Negative_{t}"

    # Storage capacity constraint
    problem += I[t] <= data['capacity'], f"Capacity_Constraint_{t}"

# Inventory balance constraints
problem += I[0] == 0 + B[0] - S[0], "Initial_Inventory_Balance"
for t in range(1, N):
    problem += I[t] == I[t-1] + B[t] - S[t], f"Inventory_Balance_{t}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')