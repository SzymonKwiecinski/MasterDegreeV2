import pulp
import json

# Problem Data
data_json = '''<DATA>
{'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}</DATA>'''
data = json.loads(data_json)

# Extract Parameters
requirement = data["requirement"]
strength = data["strength"]
lessonewaste = data["lessonewaste"]
moreonewaste = data["moreonewaste"]
recruit = data["recruit"]
costredundancy = data["costredundancy"]
num_overman = data["num_overman"]
costoverman = data["costoverman"]
num_shortwork = data["num_shortwork"]
costshort = data["costshort"]

# Constants
K = len(strength)
I = len(requirement[0])

# Problem
problem = pulp.LpProblem("MinimizeRedundancy", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, upBound=num_overman, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=num_shortwork, cat='Integer')
redundancy_vars = pulp.LpVariable.dicts("redundancy", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(costredundancy[k] * redundancy_vars[k][i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    current_strength = strength[k]
    for i in range(I):
        if i == 0:
            wastage = current_strength * moreonewaste[k]
            next_strength = (
                current_strength 
                - wastage 
                + recruit_vars[k][i] 
                - redundancy_vars[k][i] 
                + overmanning_vars[k][i] 
                + 0.5 * short_vars[k][i]
            )
        else:
            wastage = next_strength * moreonewaste[k]
            next_strength = (
                next_strength 
                - wastage 
                + recruit_vars[k][i] 
                - redundancy_vars[k][i] 
                + overmanning_vars[k][i] 
                + 0.5 * short_vars[k][i]
            )
        
        # Meet requirements, allow overmanning and short-working
        problem += (
            next_strength 
            + overmanning_vars[k][i] 
            + 0.5 * short_vars[k][i] 
            >= requirement[k][i]
        )
        
        # Recruitment limits
        problem += recruit_vars[k][i] <= recruit[k]

# Solve Problem
problem.solve()

# Results
output = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')