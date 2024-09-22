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

# Parameters
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create the problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

# Objective Function
profit = pulp.lpSum([data['steel_prices'][s] * total_steel[s] for s in range(S)]) - \
         pulp.lpSum([data['alloy_prices'][a] * pulp.lpSum([alloy_amount[a][s] for s in range(S)]) for a in range(A)])
problem += profit

# Constraints
# Alloy Availability
for a in range(A):
    problem += pulp.lpSum([alloy_amount[a][s] for s in range(S)]) <= data['available'][a]

# Steel Production
for s in range(S):
    problem += total_steel[s] == pulp.lpSum([alloy_amount[a][s] for a in range(A)])

# Carbon Content
for s in range(S):
    problem += (pulp.lpSum([data['carbon'][a] * alloy_amount[a][s] for a in range(A)]) / total_steel[s]) >= data['carbon_min'][s]

# Nickel Content
for s in range(S):
    problem += (pulp.lpSum([data['nickel'][a] * alloy_amount[a][s] for a in range(A)]) / total_steel[s]) <= data['nickel_max'][s]

# Alloy 1 Constraint
problem += pulp.lpSum([alloy_amount[0][s] for s in range(S)]) <= \
           0.4 * pulp.lpSum([total_steel[s] for s in range(S)])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')