import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Number of periods
N = len(prices)

# Create the problem
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum((sellquantity[n] * prices[n] - buyquantity[n] * costs[n] - holding_cost * stock[n] 
                     for n in range(N)))
problem += profit, "Total_Profit"

# Constraints
# Stock balance constraints
stock[0] = buyquantity[0] - sellquantity[0]
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

# Capacity constraints
for n in range(N):
    problem += buyquantity[n] <= capacity, f"Cap_Constraint_{n}"
    problem += stock[n] <= capacity, f"Stock_Constraint_{n}"

# The stock must be empty at the end of the last period
problem += stock[N-1] == 0, "Final_Stock_Empty"

# Solve the problem
problem.solve()

# Prepare output data
output = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')