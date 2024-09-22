import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extracting data from the input
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

# Number of periods
N = len(price)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum((sellquantity[n] * price[n] - buyquantity[n] * cost[n] - stock[n] * holding_cost) for n in range(N))
problem += profit

# Constraints
# Capacity constraints
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n], f"Stock_Constraint_{n}"
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock_Constraint_{n}"
    
    problem += stock[n] <= capacity, f"Capacity_Constraint_{n}"

# Final stock must be zero
problem += stock[N-1] == 0, "Final_Stock_Constraint"

# Solve the problem
problem.solve()

# Output results
output = {
    "buyquantity": [buyquantity[n].varValue for n in range(N)],
    "sellquantity": [sellquantity[n].varValue for n in range(N)],
    "stock": [stock[n].varValue for n in range(N)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')