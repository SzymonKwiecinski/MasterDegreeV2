import pulp
import json

# Input data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Problem parameters
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Define variables
buyquantity = pulp.LpVariable.dicts("buy", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", range(N), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum([(price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

# Constraints
# Capacity constraints
problem += pulp.lpSum([buyquantity[n] for n in range(N)]) - pulp.lpSum([sellquantity[n] for n in range(N)]) <= capacity, "CapacityConstraint"
# Stock calculation constraints
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n], f"StockBalancePeriod_{n}"
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"StockBalancePeriod_{n}"

# Ensure the warehouse is empty at the end
problem += stock[N-1] == 0, "FinalStockEmpty"

# Solve the problem
problem.solve()

# Output results
results = {
    "buyquantity": [buyquantity[n].varValue for n in range(N)],
    "sellquantity": [sellquantity[n].varValue for n in range(N)],
    "stock": [stock[n].varValue for n in range(N)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the results
print(json.dumps(results))