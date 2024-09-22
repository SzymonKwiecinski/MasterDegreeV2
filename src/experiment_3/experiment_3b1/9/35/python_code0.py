import pulp
import json

# Data provided in JSON format
data_json = '{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}'
data = json.loads(data_json)

# Parameters
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Create problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum([prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N)])

# Constraints
problem += (stock[0] == 0)  # Initial condition

for n in range(N):
    if n > 0:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n])  # Stock balance
    problem += (stock[n] <= capacity)  # Capacity constraint
    problem += (buyquantity[n] >= 0)  # Non-negativity constraint for buy quantity
    problem += (sellquantity[n] >= 0)  # Non-negativity constraint for sell quantity
    problem += (stock[n] >= 0)  # Non-negativity constraint for stock

problem += (stock[N-1] == 0)  # Final condition

# Solve the problem
problem.solve()

# Output results
buyquantity_result = [buyquantity[n].varValue for n in range(N)]
sellquantity_result = [sellquantity[n].varValue for n in range(N)]
stock_result = [stock[n].varValue for n in range(N)]

print(f'Buy Quantity: {buyquantity_result}')
print(f'Sell Quantity: {sellquantity_result}')
print(f'Stock: {stock_result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')