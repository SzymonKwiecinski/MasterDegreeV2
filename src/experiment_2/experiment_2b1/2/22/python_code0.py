import pulp
import json

data_json = '''{'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}'''
data = json.loads(data_json.replace("'", "\""))

K = len(data['requirement'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')

# Objective Function: Minimize redundancy costs
costs_redundancy = pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] + pulp.lpSum(recruit_vars[k][i] for i in range(I)) - pulp.lpSum(overmanning_vars[k][i] for i in range(I)) - pulp.lpSum(short_vars[k][i] for i in range(I)) - data['requirement'][k][i]) for k in range(K) for i in range(I))
problem += costs_redundancy

# Constraints
for k in range(K):
    for i in range(I):
        # Strength after wastage = Current strength - leaving workers + recruits - overmanning - short
        current_strength = (data['strength'][k] * (1 - data['moreonewaste'][k])) - (data['lessonewaste'][k] * recruit_vars[k][i])
        problem += (current_strength + pulp.lpSum(recruit_vars[k][j] for j in range(I)) - pulp.lpSum(overmanning_vars[k][j] for j in range(I)) - pulp.lpSum(short_vars[k][j] for j in range(I)) >= data['requirement'][k][i], f"Manpower_Requirement_Constraint_{k}_{i}")

# Overmanning and Short-time working constraints
for k in range(K):
    problem += pulp.lpSum(overmanning_vars[k][i] for i in range(I)) <= data['num_overman'], f"Overmanning_Constraint_{k}"
    problem += pulp.lpSum(short_vars[k][i] for i in range(I)) <= data['num_shortwork'], f"Short_time_Working_Constraint_{k}"

# Recruitment constraints
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k][i] <= data['recruit'][k], f"Recruitment_Limit_Constraint_{k}_{i}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[recruit_vars[k][i].varValue for i in range(I)] for k in range(K)],
    "overmanning": [[overmanning_vars[k][i].varValue for i in range(I)] for k in range(K)],
    "short": [[short_vars[k][i].varValue for i in range(I)] for k in range(K)]
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')