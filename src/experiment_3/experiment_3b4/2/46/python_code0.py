import pulp

# Problem data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Sets
alloys = range(len(data['available']))
steel_types = range(len(data['steel_prices']))

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("AlloyAmount", (alloys, steel_types), 0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("TotalSteel", steel_types, 0, cat='Continuous')

# Objective Function
problem += (
    pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in steel_types) -
    pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a][s] for a in alloys for s in steel_types)
), "Total Profit"

# Constraints
# Material Balance
for s in steel_types:
    problem += (total_steel[s] == pulp.lpSum(alloy_amount[a][s] for a in alloys)), f"MaterialBalance_Steel_{s}"

# Carbon Requirement
for s in steel_types:
    problem += (
        pulp.lpSum(data['carbon'][a] * alloy_amount[a][s] for a in alloys) >= 
        data['carbon_min'][s] * total_steel[s]
    ), f"CarbonRequirement_Steel_{s}"

# Nickel Limitation
for s in steel_types:
    problem += (
        pulp.lpSum(data['nickel'][a] * alloy_amount[a][s] for a in alloys) <= 
        data['nickel_max'][s] * total_steel[s]
    ), f"NickelLimitation_Steel_{s}"

# Alloy Availability
for a in alloys:
    problem += (
        pulp.lpSum(alloy_amount[a][s] for s in steel_types) <= data['available'][a]
    ), f"AlloyAvailability_Alloy_{a}"

# Alloy 1 Usage Limitation
for s in steel_types:
    problem += (
        alloy_amount[0][s] <= 0.4 * total_steel[s]
    ), f"Alloy1UsageLimitation_Steel_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')