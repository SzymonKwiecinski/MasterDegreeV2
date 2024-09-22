import pulp
import json

# Input data
data = {'available': [40, 50, 80], 
        'carbon': [3, 4, 3.5], 
        'nickel': [1, 1.5, 1.8], 
        'alloy_prices': [380, 400, 440], 
        'steel_prices': [650, 600], 
        'carbon_min': [3.6, 3.4], 
        'nickel_max': [1.5, 1.7]}

# Constants
A = len(data['available'])
S = len(data['steel_prices'])

# Create the problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Decision variables
alloy_use = pulp.LpVariable.dicts("alloy_use", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", (s for s in range(S)), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum((data['steel_prices'][s] * total_steel[s]) - (pulp.lpSum(data['alloy_prices'][a] * alloy_use[(a, s)] for a in range(A) for s in range(S))) for s in range(S))
problem += profit

# Constraints
for a in range(A):
    problem += pulp.lpSum(alloy_use[(a, s)] for s in range(S)) <= data['available'][a], f"Available_alloy_{a}"

for s in range(S):
    problem += pulp.lpSum(alloy_use[(a, s)] * data['carbon'][a] for a in range(A)) >= total_steel[s] * data['carbon_min'][s], f"Carbon_min_{s}"
    problem += pulp.lpSum(alloy_use[(a, s)] * data['nickel'][a] for a in range(A)) <= total_steel[s] * data['nickel_max'][s], f"Nickel_max_{s}"

# Constraint for Alloy 1
problem += pulp.lpSum(alloy_use[(0, s)] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S)), "Max_alloy_1"

# Solve the problem
problem.solve()

# Results
alloy_distribution = [[pulp.value(alloy_use[(a, s)]) for a in range(A)] for s in range(S)]
total_steel_produced = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "alloy_use": alloy_distribution,
    "total_steel": total_steel_produced,
    "total_profit": total_profit
}

# Print output
print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')