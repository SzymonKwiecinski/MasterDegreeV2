import pulp
import json

# Data in JSON format
data = '''
{
    "available": [40, 50, 80],
    "carbon": [3, 4, 3.5],
    "nickel": [1, 1.5, 1.8],
    "alloy_prices": [380, 400, 440],
    "steel_prices": [650, 600],
    "carbon_min": [3.6, 3.4],
    "nickel_max": [1.5, 1.7]
}
'''
data = json.loads(data)

# Decision Variables
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create the problem
problem = pulp.LpProblem("Alloy_and_Steel_Production", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0)  # Alloy usage
y = pulp.LpVariable.dicts("y", range(S), lowBound=0)  # Steel produced

# Objective Function
problem += pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - \
           pulp.lpSum(data['alloy_prices'][a] * x[a][s] for a in range(A) for s in range(S))

# Constraints
# Alloy Usage Constraints
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= data['available'][a]

# Steel Production Constraints
for s in range(S):
    problem += pulp.lpSum(x[a][s] for a in range(A)) == y[s]

# Carbon Requirement Constraints
for s in range(S):
    problem += (pulp.lpSum(data['carbon'][a] * x[a][s] for a in range(A)) >= data['carbon_min'][s] * y[s])

# Nickel Constraint
for s in range(S):
    problem += (pulp.lpSum(data['nickel'][a] * x[a][s] for a in range(A)) <= data['nickel_max'][s] * y[s])

# Alloy 1 Constraint
for s in range(S):
    problem += (x[0][s] <= 0.4 * y[s])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')