import pulp

# Data from the provided JSON
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Set of alloys and steel types
A = range(len(data['available']))  # Alloys: 0, 1, 2
S = range(len(data['steel_prices']))  # Steel types: 0, 1

# Create the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (A, S), lowBound=0)  # Amount of alloy used in each steel type
total_steel = pulp.LpVariable.dicts("total_steel", S, lowBound=0)  # Total amount of each steel produced

# Objective Function: Maximize profit
total_profit = pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in S) - \
               pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a][s] for a in A for s in S)

problem += total_profit, "Total_Profit"

# Constraints
# Material Balance for Each Steel
for s in S:
    problem += pulp.lpSum(alloy_amount[a][s] for a in A) == total_steel[s], f"Material_Balance_Steel_{s}"

# Carbon Requirement
for s in S:
    problem += (pulp.lpSum(data['carbon'][a] * alloy_amount[a][s] for a in A) >= 
                data['carbon_min'][s] * total_steel[s]), f"Carbon_Requirement_{s}"

# Nickel Constraint
for s in S:
    problem += (pulp.lpSum(data['nickel'][a] * alloy_amount[a][s] for a in A) <= 
                data['nickel_max'][s] * total_steel[s]), f"Nickel_Constraint_{s}"

# Alloy Availability
for a in A:
    problem += (pulp.lpSum(alloy_amount[a][s] for s in S) <= data['available'][a]), f"Alloy_Availability_{a}"

# Maximum Alloy 1 Usage
for s in S:
    problem += alloy_amount[0][s] <= 0.4 * total_steel[s], f"Max_Alloy_1_Usage_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')