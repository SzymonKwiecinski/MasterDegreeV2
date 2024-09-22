import pulp
import json

# Load the data
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extract parameters
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(requirement)      # Number of manpower categories
I = len(requirement[0])   # Number of years

# Define the problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(costredundancy[k] * (strength[k] - lessonewaste[k] * strength[k] - moreonewaste[k] * (strength[k] - lessonewaste[k] * strength[k]) + recruit_vars[k, i] + overmanning_vars[k, i] - short_vars[k, i]) for k in range(K) for i in range(I)), "Total_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        problem += (strength[k] -
                    lessonewaste[k] * strength[k] -
                    moreonewaste[k] * (strength[k] - lessonewaste[k] * strength[k]) +
                    recruit_vars[k, i] +
                    overmanning_vars[k, i] -
                    short_vars[k, i] == requirement[k][i]), f"Manpower_Balance_{k}_{i}"

# Recruitment limit
for k in range(K):
    problem += pulp.lpSum(recruit_vars[k, i] for i in range(I)) <= recruit[k], f"Recruitment_Limit_{k}"

# Overmanning limit
for k in range(K):
    problem += pulp.lpSum(overmanning_vars[k, i] for i in range(I)) <= num_overman, f"Overmanning_Limit_{k}"

# Short-time working limit
for k in range(K):
    problem += pulp.lpSum(short_vars[k, i] for i in range(I)) <= num_shortwork, f"Short_Work_Limit_{k}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')