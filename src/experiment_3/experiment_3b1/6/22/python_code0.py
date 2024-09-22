import pulp
import json

# Data in JSON format
data_json = '''{
    "requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
    "strength": [2000, 1500, 1000], 
    "lessonewaste": [0.25, 0.2, 0.1], 
    "moreonewaste": [0.1, 0.05, 0.05], 
    "recruit": [500, 800, 500], 
    "costredundancy": [200, 500, 500], 
    "num_overman": 150, 
    "costoverman": [1500, 2000, 3000], 
    "num_shortwork": 50, 
    "costshort": [500, 400, 400]
}'''

data = json.loads(data_json)

# Parameters
K = len(data['requirement'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the Linear Programming problem
problem = pulp.LpProblem("Workforce_Management", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * overmanning_vars[k][i] for k in range(K) for i in range(I)), "Total_Redundancy_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        waste = data['lessonewaste'][k] * recruit_vars[k][i] + data['moreonewaste'][k] * (data['strength'][k] - recruit_vars[k][i])
        problem += (data['strength'][k] - waste + recruit_vars[k][i] + overmanning_vars[k][i] - short_vars[k][i] >= data['requirement'][k][i]), f"Manpower_Requirement_Constraint_{k}_{i}"

for k in range(K):
    problem += (pulp.lpSum(recruit_vars[k][i] for i in range(I)) <= data['recruit'][k]), f"Recruit_Constraint_{k}"

for k in range(K):
    problem += (pulp.lpSum(overmanning_vars[k][i] for i in range(I)) <= data['num_overman']), f"Overmanning_Constraint_{k}"

for k in range(K):
    problem += (pulp.lpSum(short_vars[k][i] for i in range(I)) <= data['num_shortwork']), f"Short_Work_Constraint_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')