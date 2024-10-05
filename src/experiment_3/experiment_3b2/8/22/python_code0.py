import pulp
import json

# Data provided in JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extract data
requirements = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(requirements)  # Number of skill categories
I = len(requirements[0])  # Number of years for planning

# Create the problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, upBound=[recruit[k] for k in range(K)], cat='Continuous')
o = pulp.LpVariable.dicts("Overman", (range(K), range(I)), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("ShortTime", (range(K), range(I)), lowBound=0, upBound=num_shortwork, cat='Continuous')

# Objective Function
problem += pulp.lpSum(costredundancy[k] * (strength[k] + x[k][i] - requirements[k][i] - o[k][i] - 0.5 * s[k][i]) for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        problem += (strength[k] + x[k][i] * (1 - lessonewaste[k] if i == 0 else 1) * (1 - moreonewaste[k] if i > 0 else 1) + o[k][i] + 0.5 * s[k][i] >= requirements[k][i])

for i in range(I):
    problem += (pulp.lpSum(o[k][i] for k in range(K)) <= num_overman)

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')