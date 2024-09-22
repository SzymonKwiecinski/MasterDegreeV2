import pulp

# Data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Indices
A = len(data['available'])
S = len(data['steel_prices'])

# Problem
problem = pulp.LpProblem("SteelProduction", pulp.LpMaximize)

# Decision variables
X = pulp.LpVariable.dicts("X", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
T = pulp.LpVariable.dicts("T", (s for s in range(S)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['steel_prices'][s] * T[s] for s in range(S)) - \
           pulp.lpSum(data['alloy_prices'][a] * X[(a, s)] for a in range(A) for s in range(S))

# Constraints

# 1. Availability of Alloys
for a in range(A):
    problem += pulp.lpSum(X[(a, s)] for s in range(S)) <= data['available'][a]

# 2. Carbon Requirement for Steel
for s in range(S):
    problem += pulp.lpSum((data['carbon'][a] / 100) * X[(a, s)] for a in range(A)) >= data['carbon_min'][s] * T[s]

# 3. Nickel Requirement for Steel
for s in range(S):
    problem += pulp.lpSum((data['nickel'][a] / 100) * X[(a, s)] for a in range(A)) <= data['nickel_max'][s] * T[s]

# 4. Alloy Usage Limitation
problem += pulp.lpSum(X[(0, s)] for s in range(S)) <= 0.4 * pulp.lpSum(T[s] for s in range(S))

# Solve
problem.solve()

# Output
alloy_use = {(a, s): X[(a, s)].varValue for a in range(A) for s in range(S)}
total_steel = {s: T[s].varValue for s in range(S)}
total_profit = pulp.value(problem.objective)

print("Alloy Usage (tons):", alloy_use)
print("Total Steel Produced (tons):", total_steel)
print(f"Total Profit: <OBJ>{total_profit}</OBJ>")