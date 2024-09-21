import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Problem Definition
N = len(data['price'])
problem = pulp.LpProblem("OptimalTradingStrategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, upBound=data['capacity'], cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t] for t in range(N))
problem += profit

# Constraints
# Inventory balance and initial inventory
problem += I[0] == 0  # Initial inventory
for t in range(N):
    if t > 0:
        problem += I[t] == I[t - 1] + B[t] - S[t]  # Inventory balance
    problem += I[t] >= 0  # Non-negative inventory
    problem += S[t] >= 0  # Non-negative sales
    problem += B[t] >= 0  # Non-negative purchases
    problem += I[t] <= data['capacity']  # Storage capacity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')