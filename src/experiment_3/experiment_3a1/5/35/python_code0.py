import pulp
import json

# Given data in dictionary format
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

# Create the problem variable
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Decision variables
b = pulp.LpVariable.dicts("buy", range(1, N + 1), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("sell", range(1, N + 1), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("stock", range(1, N + 1), lowBound=0, upBound=C, cat='Continuous')

# Objective function
profit = pulp.lpSum(p[n - 1] * s[n] - c[n - 1] * b[n] - h * x[n] for n in range(1, N + 1))
problem += profit, "Total_Profit"

# Constraints
problem += (x[1] == b[1] - s[1]), "Stock_1"
for n in range(2, N + 1):
    problem += (x[n] == x[n - 1] + b[n] - s[n]), f"Stock_{n}"

problem += (x[N] == 0), "Empty_End"

# Solve the problem
problem.solve()

# Collecting results
buyquantity = [b[n].varValue for n in range(1, N + 1)]
sellquantity = [s[n].varValue for n in range(1, N + 1)]
stock = [x[n].varValue for n in range(1, N + 1)]

# Output the results
result = {
    "buyquantity": buyquantity,
    "sellquantity": sellquantity,
    "stock": stock
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the result in JSON format
print(json.dumps(result))