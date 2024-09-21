import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Number of periods (N)
N = len(data['price'])

# Model
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision variables
B = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(N+1), lowBound=0, cat='Continuous')

# Initial inventory
problem += I[0] == 0

# Objective function
problem += pulp.lpSum([data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t] for t in range(N)])

# Constraints
for t in range(N):
    # Inventory balance
    problem += I[t+1] == I[t] + B[t] - S[t]
    # Capacity constraint
    problem += I[t] <= data['capacity']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')