import pulp
import json

# Define the data
data = json.loads("{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}")

# Parameters
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0)  # Amount of alloy a used in steel type s
y = pulp.LpVariable.dicts("y", range(S), lowBound=0)  # Total amount of steel type s produced

# Objective function
profit = pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - pulp.lpSum(data['alloy_prices'][a] * pulp.lpSum(x[a][s] for s in range(S)) for a in range(A))
problem += profit, "Total Profit"

# Constraints
# Alloy availability
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= data['available'][a], f"Alloy_Availability_{a}"

# Carbon content constraints
for s in range(S):
    problem += (pulp.lpSum(x[a][s] * data['carbon'][a] for a in range(A)) / y[s] >= data['carbon_min'][s]), f"Carbon_Content_{s}"

# Nickel content constraints
for s in range(S):
    problem += (pulp.lpSum(x[a][s] * data['nickel'][a] for a in range(A)) / y[s] <= data['nickel_max'][s]), f"Nickel_Content_{s}"

# Alloy 1 restriction
problem += pulp.lpSum(x[0][s] for s in range(S)) <= 0.4 * pulp.lpSum(y[s] for s in range(S)), "Alloy_1_Restriction"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')