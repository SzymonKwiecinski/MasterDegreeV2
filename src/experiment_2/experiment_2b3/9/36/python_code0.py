from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

# Parse the input data from JSON
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)  # Number of available alloys
M = len(target)  # Number of metals

# Create the LP problem instance
problem = LpProblem("Alloy_Optimization", LpMinimize)

# Decision variables: amount of each alloy to purchase
amount_vars = [LpVariable(f"amount_{k}", lowBound=0) for k in range(K)]

# Objective function: Minimize the total cost of alloys
problem += lpSum(prices[k] * amount_vars[k] for k in range(K)), "Total_Cost"

# Constraint: The sum of all alloys should equal the required alloy quantity
problem += lpSum(amount_vars) == alloy_quant, "Total_Alloy_Quantity"

# Constraints: Achieve the target composition of metals
for m in range(M):
    problem += lpSum(ratios[k][m] * amount_vars[k] for k in range(K)) == target[m], f"Target_Metal_{m}"

# Solve the problem
problem.solve()

# Extract the results
amounts = [amount_vars[k].varValue for k in range(K)]

solution = {
    "amount": amounts
}

print(solution)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')