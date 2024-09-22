import pulp
import json

# Given data
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0)  # Alloy usage
y = pulp.LpVariable.dicts("y", range(S), lowBound=0)              # Total steel produced

# Objective Function
profit = pulp.lpSum(y[s] * data['steel_prices'][s] for s in range(S)) - \
         pulp.lpSum(x[a][s] * data['alloy_prices'][a] for a in range(A) for s in range(S))

problem += profit, "Total_Profit"

# Constraints
# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= data['available'][a], f"Available_Alloy_{a}"

# Carbon percentage constraints
for s in range(S):
    problem += pulp.lpSum(x[a][s] * data['carbon'][a] for a in range(A)) >= data['carbon_min'][s] * y[s], f"Carbon_Min_{s}"

# Nickel percentage constraints
for s in range(S):
    problem += pulp.lpSum(x[a][s] * data['nickel'][a] for a in range(A)) <= data['nickel_max'][s] * y[s], f"Nickel_Max_{s}"

# Alloy 1 usage constraint
problem += pulp.lpSum(x[0][s] for s in range(S)) <= 0.4 * pulp.lpSum(y[s] for s in range(S)), "Alloy_1_Usage"

# Solve the problem
problem.solve()

# Output result
alloy_use = [[pulp.value(x[a][s]) for a in range(A)] for s in range(S)]
total_steel = [pulp.value(y[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Format output as required
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')