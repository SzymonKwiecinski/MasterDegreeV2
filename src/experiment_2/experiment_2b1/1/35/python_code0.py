import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Problem parameters
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Stock_Management", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buy", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", range(N), lowBound=0, cat='Continuous')

# Objective Function: Maximize profit
profit = pulp.lpSum([(prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

# Constraints
# Stock balance constraints
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}"
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}"
    
    # Capacity constraint
    problem += stock[n] <= capacity, f"Capacity_Constraint_{n}"

# End condition: warehouse must be empty at the last period
problem += stock[N-1] == 0, "Final_Stock_Condition"

# Solve the problem
problem.solve()

# Output results
output = {
    "buyquantity": [buyquantity[n].varValue for n in range(N)],
    "sellquantity": [sellquantity[n].varValue for n in range(N)],
    "stock": [stock[n].varValue for n in range(N)],
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')