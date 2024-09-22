import pulp
import json

# Data from the provided JSON
data = {'alloy_quant': 1000, 
        'target': [300, 700], 
        'ratio': [[0.1, 0.9], 
                  [0.25, 0.75], 
                  [0.5, 0.5], 
                  [0.75, 0.25], 
                  [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Parameters
A = data['alloy_quant']
M = len(data['target'])
K = len(data['price'])
target = data['target']
ratio = data['ratio']
price = data['price']

# Decision Variables
x = pulp.LpVariable.dicts("alloy", range(K), lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
problem += pulp.lpSum(x[k] for k in range(K)) == A, "Total_Weight"

for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m], f"Metal_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Output the results
amounts = [x[k].varValue for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Amounts of each alloy: {amounts}')