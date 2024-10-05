import pulp

# Parse the problem data from JSON
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Number of alloys and steels
A = len(data['available'])
S = len(data['steel_prices'])

# Initialize the Linear Program
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("AlloyAmt", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("TotalSteel", (s for s in range(S)), lowBound=0)

# Objective Function: Maximize profit
profit = (
    pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) -
    pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a, s] for a in range(A) for s in range(S))
)
problem += profit

# Constraints
# Alloy availability constraint
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= data['available'][a]

# Ensure total steel is produced from alloy amounts
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a, s] for a in range(A)) == total_steel[s]

# Steel composition constraints
for s in range(S):
    # Carbon constraint
    problem += pulp.lpSum(data['carbon'][a] * alloy_amount[a, s] for a in range(A)) >= data['carbon_min'][s] * total_steel[s]
    # Nickel constraint
    problem += pulp.lpSum(data['nickel'][a] * alloy_amount[a, s] for a in range(A)) <= data['nickel_max'][s] * total_steel[s]

# Maximum 40% of alloy 1 constraint in any steel
for s in range(S):
    problem += alloy_amount[0, s] <= 0.4 * total_steel[s]

# Solve the Linear Program
problem.solve()

# Prepare output
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel_values = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_values,
    "total_profit": total_profit
}

print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')