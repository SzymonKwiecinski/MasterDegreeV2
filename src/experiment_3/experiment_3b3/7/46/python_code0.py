import pulp

# Data from JSON
data = {
    'available': [40, 50, 80], 
    'carbon': [3, 4, 3.5], 
    'nickel': [1, 1.5, 1.8], 
    'alloy_prices': [380, 400, 440], 
    'steel_prices': [650, 600], 
    'carbon_min': [3.6, 3.4], 
    'nickel_max': [1.5, 1.7]
}

# Constants
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", (s for s in range(S)), lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Objective Function
problem += (
    pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) -
    pulp.lpSum(data['alloy_prices'][a] * alloy_amount[(a, s)] for a in range(A) for s in range(S))
)

# Constraints
# 1. Alloy availability constraint
for a in range(A):
    problem += pulp.lpSum(alloy_amount[(a, s)] for s in range(S)) <= data['available'][a]

# 2. Carbon content constraint for each steel type
for s in range(S):
    problem += (
        pulp.lpSum(data['carbon'][a] * alloy_amount[(a, s)] for a in range(A)) >= data['carbon_min'][s] * total_steel[s]
    )

# 3. Nickel content constraint for each steel type
for s in range(S):
    problem += (
        pulp.lpSum(data['nickel'][a] * alloy_amount[(a, s)] for a in range(A)) <= data['nickel_max'][s] * total_steel[s]
    )

# 4. Maximum allowable percentage of alloy 1
problem += (
    pulp.lpSum(alloy_amount[(0, s)] for s in range(S)) <= 
    0.4 * pulp.lpSum(total_steel[s] for s in range(S))
)

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')