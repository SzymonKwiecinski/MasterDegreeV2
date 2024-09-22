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
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

# Problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("Buy", range(1, N+1), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("Sell", range(1, N+1), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("Stock", range(1, N+1), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([p[n-1] * s[n] - c[n-1] * b[n] - h * x[n] for n in range(1, N+1)])
problem += profit, "Total Profit"

# Constraints
for n in range(1, N+1):
    if n == 1:
        problem += (x[n] == b[n] - s[n]), f"Stock_Balance_Initial_{n}"
    else:
        problem += (x[n] == x[n-1] + b[n] - s[n]), f"Stock_Balance_{n}"
    problem += (x[n] <= C), f"Capacity_{n}"
    problem += (s[n] <= x[n] + b[n-1]), f"Stock_Availability_{n}"  # Changed x[n-1] to x[n] and b[n] to b[n-1]

# Final stock must be zero
problem += (x[N] == 0), "Final_Stock_Zero"

# Solve the problem
problem.solve()

# Output the results
for n in range(1, N+1):
    print(f"Period {n}: Buy {b[n].varValue}, Sell {s[n].varValue}, Stock {x[n].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')