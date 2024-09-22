import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Create the Linear Program
problem = pulp.LpProblem("Warehouse_Problem", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum((sellquantity[n] * prices[n]) - (buyquantity[n] * costs[n]) - (holding_cost * stock[n]) for n in range(N))
problem += profit

# Constraints
# Capacity constraint for each period
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n], f"Stock_Initial_Period_{n}"
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock_Period_{n}"
    
    problem += stock[n] <= capacity, f"Capacity_Constraint_{n}"

# Final stock must be zero
problem += stock[N-1] == 0, "Final_Stock_Zero"

# Solve the problem
problem.solve()

# Collecting results
result = {
    "buyquantity": [buyquantity[n].varValue for n in range(N)],
    "sellquantity": [sellquantity[n].varValue for n in range(N)],
    "stock": [stock[n].varValue for n in range(N)]
}

# Print the results
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')