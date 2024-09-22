import pulp
import json

# Data from the provided JSON format
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Define the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Define sets
A = range(len(data['available']))  # Alloys
S = range(len(data['steel_prices']))  # Steel types

# Decision Variables
x = pulp.LpVariable.dicts("x", (A, S), lowBound=0)  # Amount of alloy a used for steel type s
y = pulp.LpVariable.dicts("y", S, lowBound=0)        # Total amount of steel type s produced

# Objective Function
profit = pulp.lpSum(data['steel_prices'][s] * y[s] for s in S) - pulp.lpSum(data['alloy_prices'][a] * pulp.lpSum(x[a][s] for s in S) for a in A)
problem += profit

# Constraints
# Alloy availability constraint
for a in A:
    problem += pulp.lpSum(x[a][s] for s in S) <= data['available'][a]

# Carbon percentage constraints
for s in S:
    problem += (pulp.lpSum(x[a][s] * data['carbon'][a] for a in A) >= data['carbon_min'][s] * y[s])

# Nickel percentage constraints
for s in S:
    problem += (pulp.lpSum(x[a][s] * data['nickel'][a] for a in A) <= data['nickel_max'][s] * y[s])

# Maximum usage of alloy 1
problem += (pulp.lpSum(x[0][s] for s in S) <= 0.4 * pulp.lpSum(y[s] for s in S))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')