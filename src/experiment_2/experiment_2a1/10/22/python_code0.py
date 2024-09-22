import pulp
import json

# Input data in JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extract data
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limit = data['recruit']
cost_redundancy = data['costredundancy']
num_overman = data['num_overman']
cost_overman = data['costoverman']
num_shortwork = data['num_shortwork']
cost_short = data['costshort']

K = len(requirement)  # Number of manpower types
I = len(requirement[0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=lambda k: recruit_limit[k])
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=num_shortwork)

# Objective Function
problem += pulp.lpSum(cost_redundancy[k] * (strength[k] + pulp.lpSum(recruit[k, i] for i in range(I)) - pulp.lpSum(overmanning[k, i] for i in range(I)) - pulp.lpSum(short[k, i] for i in range(I)) - (strength[k] * (1 - moreonewaste[k]))) for k in range(K))

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower balance constraint
        problem += (strength[k] + pulp.lpSum(recruit[k, j] for j in range(i + 1)) - (strength[k] * (1 - moreonewaste[k]) + (strength[k] * lessonewaste[k] * (1 if i == 0 else 0)) + pulp.lpSum(overmanning[k, j] for j in range(I)) + pulp.lpSum(short[k, j] for j in range(I))) >= requirement[k][i])

# Overmanning constraint
for i in range(I):
    problem += pulp.lpSum(overmanning[k, i] for k in range(K)) <= num_overman

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k, i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')