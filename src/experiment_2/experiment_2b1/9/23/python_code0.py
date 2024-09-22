import pulp
import json

# Input Data
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
    'strength': [2000, 1500, 1000], 
    'lessonewaste': [0.25, 0.2, 0.1], 
    'moreonewaste': [0.1, 0.05, 0.05], 
    'recruit': [500, 800, 500], 
    'costredundancy': [200, 500, 500], 
    'num_overman': 150, 
    'costoverman': [1500, 2000, 3000], 
    'num_shortwork': 50, 
    'costshort': [500, 400, 400]
}

# Parameters
K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=[data['recruit'][k] for k in range(K)], cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=data['num_shortwork'], cat='Integer')

# Constraints
for k in range(K):
    for i in range(I):
        current_strength = data['strength'][k] * (1 - data['moreonewaste'][k])  # Remaining strength after wastage
        effective_strength = current_strength + short_vars[k][i] * 0.5 + overmanning_vars[k][i]
        problem += effective_strength + recruit_vars[k][i] >= data['requirement'][k][i], f"Requirement_Constraint_{k}_{i}"

# Overmanning Constraint
for i in range(I):
    problem += pulp.lpSum(overmanning_vars[k][i] for k in range(K)) <= data['num_overman'], f"Overmanning_Constraint_{i}"

# Objective Function
cost = pulp.lpSum(recruit_vars[k][i] * 0 for k in range(K) for i in range(I)) + \
       pulp.lpSum(overmanning_vars[k][i] * data['costoverman'][k] for k in range(K) for i in range(I)) + \
       pulp.lpSum(short_vars[k][i] * data['costshort'][k] for k in range(K) for i in range(I)) + \
       pulp.lpSum((data['strength'][k] - (1 - data['moreonewaste'][k]) * data['strength'][k]) * data['costredundancy'][k] for k in range(K))

problem += cost

# Solve the problem
problem.solve()

# Output
recruit_output = [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)]
overmanning_output = [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)]
short_output = [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]

output = {
    "recruit": recruit_output,
    "overmanning": overmanning_output,
    "short": short_output
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')