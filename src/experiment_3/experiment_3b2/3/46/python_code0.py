import pulp
import json

# Input data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Set indices
A = range(len(data['available']))  # Alloys
S = range(len(data['steel_prices']))  # Steel types

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (A, S), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", S, lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in S) - \
         pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a][s] for a in A for s in S)
problem += profit

# Constraints

# Material balance for steel production
for s in S:
    problem += total_steel[s] == pulp.lpSum(alloy_amount[a][s] for a in A), f"Material_Balance_{s}"

# Availability of alloy
for a in A:
    problem += pulp.lpSum(alloy_amount[a][s] for s in S) <= data['available'][a], f"Alloy_Availability_{a}"

# Carbon content constraint
for s in S:
    problem += pulp.lpSum((data['carbon'][a] / 100) * alloy_amount[a][s] for a in A) >= \
               (data['carbon_min'][s] / 100) * total_steel[s], f"Carbon_Content_{s}"

# Nickel content constraint
for s in S:
    problem += pulp.lpSum((data['nickel'][a] / 100) * alloy_amount[a][s] for a in A) <= \
               (data['nickel_max'][s] / 100) * total_steel[s], f"Nickel_Content_{s}"

# Maximum 40% of alloy 1 in any steel
for s in S:
    problem += alloy_amount[0][s] <= 0.4 * total_steel[s], f"Max_Alloy1_{s}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')