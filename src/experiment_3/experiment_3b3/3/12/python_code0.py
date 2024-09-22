import pulp

# Data
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Problem
problem = pulp.LpProblem("Currency_Exchange_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(N) for j in range(N)], lowBound=0, cat='Continuous')
final_N = pulp.LpVariable("final_N", cat='Continuous')

# Objective Function
problem += final_N, "Maximize Final Currency Amount"

# Constraints

# Balance Constraints
for i in range(N):
    problem += Start[i] + pulp.lpSum(x[(i, j)] for j in range(N)) - pulp.lpSum(x[(k, i)] for k in range(N)) <= Limit[i], f"Balance_Constraint_{i}"

# Currency Conversion Constraints
problem += final_N == Start[N-1] + pulp.lpSum(x[(i, N-1)] for i in range(N)) - pulp.lpSum(x[(N-1, j)] for j in range(N)), "Currency_Conversion_Constraint"

# Cyclic Wealth Constraints
# These are usually complex to represent directly in LP without specific cycle enumeration. We skip direct cycle checking as it requires a different approach such as graph-theoretic algorithms outside LP scope.
# However, ensure no arbitrage using a simple approximation check (e.g., ensuring direct paths do not multiply wealth):

for i in range(N):
    for j in range(N):
        if i != j:
            problem += Rate[i][j] * Rate[j][i] <= 1, f"Rate_Cycle_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')