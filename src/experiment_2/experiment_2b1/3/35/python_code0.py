import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extract data from the input
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Define the number of periods
N = len(prices)

# Create the problem variable
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQty", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("SellQty", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective Function: Maximize Profit
profit = pulp.lpSum([(prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

# Constraints

# Capacity constraint for each period
for n in range(N):
    if n == 0:
        problem += (stock[n] == buyquantity[n] - sellquantity[n]), f"Stock_Constraint_{n}"
    else:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]), f"Stock_Constraint_{n}"
    
    problem += (buyquantity[n] <= capacity), f"Capacity_Constraint_{n}"
    
# End of period stock must be zero
problem += (stock[N-1] == 0), "End_Stock_Zero_Constraint"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Show output
print(json.dumps(output))