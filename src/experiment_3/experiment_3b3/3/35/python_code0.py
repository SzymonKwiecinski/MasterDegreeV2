import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
C = data['capacity']
H = data['holding_cost']
P = data['price']
C_n = data['cost']
N = len(P)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("Stock", range(N+1), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum((P[n] * s[n] - C_n[n] * b[n] - H * x[n]) for n in range(N))
problem += profit

# Constraints
problem += (x[0] == 0, "Initial_Stock")

for n in range(N):
    problem += (x[n+1] == x[n] + b[n] - s[n], f"Stock_Balance_{n}")
    problem += (x[n] <= C, f"Capacity_Constraint_{n}")

problem += (x[N] == 0, "Final_Stock")

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')