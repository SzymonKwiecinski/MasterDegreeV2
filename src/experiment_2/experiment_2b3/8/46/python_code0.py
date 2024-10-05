import pulp

# Load data from the JSON format
data = {
    "available": [40, 50, 80],
    "carbon": [3, 4, 3.5],
    "nickel": [1, 1.5, 1.8],
    "alloy_prices": [380, 400, 440],
    "steel_prices": [650, 600],
    "carbon_min": [3.6, 3.4],
    "nickel_max": [1.5, 1.7]
}

# Extract data
available = data["available"]
carbon = data["carbon"]
nickel = data["nickel"]
alloy_prices = data["alloy_prices"]
steel_prices = data["steel_prices"]
carbon_min = data["carbon_min"]
nickel_max = data["nickel_max"]

# Number of alloys (A) and types of steel (S)
A = len(available)
S = len(steel_prices)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: amount of alloy a used in steel s
alloy_amount = pulp.LpVariable.dicts("alloy_amount",
                                     ((a, s) for a in range(A) for s in range(S)),
                                     lowBound=0, cat='Continuous')

# Decision variables: amount of steel type s produced
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum([
    (steel_prices[s] - pulp.lpSum(alloy_prices[a] * alloy_amount[a, s] for a in range(A)))
    for s in range(S)
])
problem += profit

# Constraints

# Alloy availability
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= available[a], f"Alloy_Availability_{a}"

# Carbon percentage for each steel
for s in range(S):
    problem += pulp.lpSum(carbon[a] * alloy_amount[a, s] for a in range(A)) >= carbon_min[s] * total_steel[s], f"Carbon_Content_{s}"

# Nickel percentage for each steel
for s in range(S):
    problem += pulp.lpSum(nickel[a] * alloy_amount[a, s] for a in range(A)) <= nickel_max[s] * total_steel[s], f"Nickel_Content_{s}"

# Total steel amount per type
for s in range(S):
    problem += total_steel[s] == pulp.lpSum(alloy_amount[a, s] for a in range(A)), f"Total_Steel_{s}"

# Constraint: No more than 40% of alloy 1
for s in range(S):
    problem += alloy_amount[0, s] <= 0.4 * total_steel[s], f"Alloy_1_Limit_{s}"

# Solve the problem
problem.solve()

# Retrieve results
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel_produced = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Printing the output in specified format
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_produced,
    "total_profit": total_profit
}

print(output)

# Print the objective value in the specified format
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')