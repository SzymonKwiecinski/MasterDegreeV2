import pulp
import json

# Data
data_str = '''
{
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
}
'''

data = json.loads(data_str)

# Parameters
requirement = data["requirement"]
strength = data["strength"]
lessonewaste = data["lessonewaste"]
moreonewaste = data["moreonewaste"]
recruit_cap = data["recruit"]
cost_redundancy = data["costredundancy"]
num_overman = data["num_overman"]
cost_overman = data["costoverman"]
num_shortwork = data["num_shortwork"]
cost_short = data["costshort"]

K = len(strength)  # number of manpower types
I = len(requirement[0])  # number of years

# Define problem
problem = pulp.LpProblem("Minimize Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function: Minimize redundancy costs
problem += pulp.lpSum(redundancy[k, i] * cost_redundancy[k] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            # Initial workforce constraint
            prev_strength = strength[k]
        else:
            prev_strength = (recruit[k, i-1] * (1 - lessonewaste[k]) + (prev_strength - recruit[k, i-1]) * (1 - moreonewaste[k]))

        # Workforce availability constraint
        workforce = (prev_strength + recruit[k, i] + overmanning[k, i] + short[k, i] / 2 - redundancy[k, i])
        problem += workforce >= requirement[k][i]

        # Recruitment cap
        problem += recruit[k, i] <= recruit_cap[k]

        # Short-time working cap
        problem += short[k, i] <= num_shortwork

        # Overmanning cap
        problem += overmanning[k, i] <= num_overman

# Solve the problem
problem.solve()

# Results
output = {
    "recruit": [[pulp.value(recruit[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k, i]) for i in range(I)] for k in range(K)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')