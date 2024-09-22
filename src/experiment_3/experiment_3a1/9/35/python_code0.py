import pulp
import json

# Data input
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create the linear programming problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("buy_quantity", range(N), lowBound=0)  # Buy quantities
s = pulp.LpVariable.dicts("sell_quantity", range(N), lowBound=0)  # Sell quantities
x = pulp.LpVariable.dicts("stock", range(N), lowBound=0, upBound=capacity)  # Stock levels

# Objective Function
problem += pulp.lpSum((price[n] - cost[n]) * s[n] - holding_cost * x[n] for n in range(N)), "Total_Profit"

# Constraints
# Stock Balance Equation
for n in range(N):
    if n == 0:
        problem += x[n] == b[n] - s[n], f"Stock_Balance_{n+1}"
    else:
        problem += x[n] == x[n-1] + b[n] - s[n], f"Stock_Balance_{n+1}"

# Final Stock Constraint
problem += x[N-1] == 0, "Final_Stock_Constraint"

# Solve the problem
problem.solve()

# Print the results
for n in range(N):
    print(f"Buy quantity in period {n+1}: {b[n].varValue}")
    print(f"Sell quantity in period {n+1}: {s[n].varValue}")
    print(f"Stock in period {n+1}: {x[n].varValue}")

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')