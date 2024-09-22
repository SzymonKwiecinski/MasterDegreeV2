import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extract parameters from input data
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Number of periods
N = len(prices)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

# Constraints
# Capacity and stock management
stock[0] = buyquantity[0] - sellquantity[0]
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]
    
# Capacity constraint for stock
for n in range(N):
    problem += stock[n] <= capacity

# Final empty stock condition
problem += stock[N-1] == 0

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