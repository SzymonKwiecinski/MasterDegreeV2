import pulp

# Data from input
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Number of alloys and steel types
A = len(data['available'])
S = len(data['steel_prices'])

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_amount = [[pulp.LpVariable(f"alloy_amount_{a}_{s}", 0) for a in range(A)] for s in range(S)]
total_steel = [pulp.LpVariable(f"total_steel_{s}", 0) for s in range(S)]

# Constraints
for s in range(S):
    # Total steel produced constraint
    problem += (pulp.lpSum(alloy_amount[a][s] for a in range(A)) == total_steel[s], f"Total_Steel_{s}")

    # Carbon constraint
    problem += (pulp.lpSum(data['carbon'][a] * alloy_amount[a][s] for a in range(A)) >= data['carbon_min'][s] * total_steel[s], f"Carbon_{s}")

    # Nickel constraint
    problem += (pulp.lpSum(data['nickel'][a] * alloy_amount[a][s] for a in range(A)) <= data['nickel_max'][s] * total_steel[s], f"Nickel_{s}")

    # Alloy 1 constraint (max 40%)
    problem += (alloy_amount[0][s] <= 0.4 * total_steel[s], f"Alloy1_Limit_{s}")

for a in range(A):
    # Availability constraint for each alloy
    problem += (pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= data['available'][a], f"Availability_Alloy_{a}")

# Objective function
problem += (pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) - 
            pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a][s] for a in range(A) for s in range(S)), 
            "Total_Profit")

# Solve the problem
problem.solve()

# Prepare the output in the given format
output = {
    "alloy_use": [[pulp.value(alloy_amount[a][s]) for a in range(A)] for s in range(S)],
    "total_steel": [pulp.value(total_steel[s]) for s in range(S)],
    "total_profit": pulp.value(problem.objective)
}

# Print the output
print(output)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")