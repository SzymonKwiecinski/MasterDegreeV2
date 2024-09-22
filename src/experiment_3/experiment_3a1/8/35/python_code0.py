import pulp

# Data from the JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
C = data['capacity']
H = data['holding_cost']
P = data['price']
C_cost = data['cost']
N = len(P)

# Create the problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0)  # Buy quantities
s = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0)  # Sell quantities
x = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, upBound=C)  # Stock levels

# Objective Function
profit_terms = [P[n] * s[n] - C_cost[n] * b[n] - H * x[n] for n in range(N)]
problem += pulp.lpSum(profit_terms), "Total_Profit"

# Constraints
problem += (x[0] == 0, "Initial_Stock_Constraint")  # x_0 = 0
for n in range(1, N):
    problem += (x[n] == x[n-1] + b[n] - s[n], f"Stock_Constraint_{n}")

for n in range(N):
    problem += (x[n] <= C, f"Capacity_Constraint_{n}")

problem += (x[N-1] == 0, "Final_Stock_Constraint")  # x_N = 0

# Solve the problem
problem.solve()

# Output the results
for n in range(N):
    print(f'Buy Quantity b[{n}] = {b[n].varValue}')
    print(f'Sell Quantity s[{n}] = {s[n].varValue}')
    print(f'Stock x[{n}] = {x[n].varValue}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')