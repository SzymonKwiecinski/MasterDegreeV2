import pulp
import json

# Data input
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

# Create the problem
problem = pulp.LpProblem("Warehouse_Operations_Optimization", pulp.LpMaximize)

# Decision Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(1, N + 1)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(1, N + 1)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0) for n in range(1, N + 1)]

# Objective Function
profit = pulp.lpSum([(price[n-1] * sellquantity[n-1]) - (cost[n-1] * buyquantity[n-1]) - (holding_cost * stock[n-1]) for n in range(1, N + 1)])
problem += profit, "Total_Profit"

# Constraints
# Stock balance for each period
for n in range(1, N + 1):
    if n == 1:
        problem += stock[n-1] == buyquantity[n-1] - sellquantity[n-1], f"Stock_Balance_Period_{n}"
    else:
        problem += stock[n-1] == stock[n-2] + buyquantity[n-1] - sellquantity[n-1], f"Stock_Balance_Period_{n}"

# Warehouse capacity constraint
for n in range(1, N + 1):
    problem += stock[n-1] <= capacity, f"Capacity_Constraint_{n}"

# Final stock constraint
problem += stock[N-1] == 0, "Final_Stock_Constraint"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "buyquantity": [buyquantity[n].varValue for n in range(N)],
    "sellquantity": [sellquantity[n].varValue for n in range(N)],
    "stock": [stock[n].varValue for n in range(N)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print output
print(json.dumps(output, indent=4))