import pulp
import json

data = {'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}

# Extract data
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)  # number of alloys
S = len(steel_prices)  # number of steel types

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

# Objective Function
problem += pulp.lpSum(total_steel[s] * steel_prices[s] for s in range(S)) - pulp.lpSum(alloy_amount[(a, s)] * alloy_prices[a] for a in range(A) for s in range(S)), "Total_Profit"

# Constraints for each steel type
for s in range(S):
    # Carbon constraint
    problem += (
        pulp.lpSum(alloy_amount[(a, s)] * carbon[a] for a in range(A)) >= total_steel[s] * carbon_min[s],
        f"Carbon_Constraint_{s}"
    )
    # Nickel constraint
    problem += (
        pulp.lpSum(alloy_amount[(a, s)] * nickel[a] for a in range(A)) <= total_steel[s] * nickel_max[s],
        f"Nickel_Constraint_{s}"
    )
    # Total steel produced from alloys
    problem += (
        total_steel[s] == pulp.lpSum(alloy_amount[(a, s)] for a in range(A)),
        f"Total_Steel_Produced_Constraint_{s}"
    )

# Constraint for alloy usage
for a in range(A):
    problem += (
        pulp.lpSum(alloy_amount[(a, s)] for s in range(S)) <= available[a],
        f"Alloy_Usage_Constraint_{a}"
    )

# Constraint for maximum use of alloy 1
problem += (
    pulp.lpSum(alloy_amount[(0, s)] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S)),
    "Max_Alloy_1_Usage"
)

# Solve the problem
problem.solve()

# Prepare output
alloy_use = [[pulp.value(alloy_amount[(a, s)]) for a in range(A)] for s in range(S)]
total_steel_produced = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Output result
result = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_produced,
    "total_profit": total_profit
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')