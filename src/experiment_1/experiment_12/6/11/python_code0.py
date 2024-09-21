import pulp

# Data from the JSON provided
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
N = len(data['price'])  # Number of periods

# Problem setup
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, cat='Continuous')

# Objective Function
objective = pulp.lpSum([data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t] for t in range(N)])
problem += objective

# Constraints
problem += (I[0] == 0, "Initial_Inventory_Constraint")  # Initial inventory

for t in range(N):
    problem += I[t] <= data['capacity'], f"Capacity_Constraint_{t}"
    if t > 0:
        problem += I[t] == I[t-1] + B[t] - S[t], f"Balance_Constraint_{t}"
    else:
        problem += I[t] == B[t] - S[t], f"Balance_Constraint_{t}"

# Solve the problem
problem.solve()

# Print the results
print(f"Status: {pulp.LpStatus[problem.status]}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")

# Optional: Print decision variables
for t in range(N):
    print(f"Period {t+1}: Buy {B[t].varValue}, Sell {S[t].varValue}, Inventory {I[t].varValue}")