import pulp
import json

# Data from JSON
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extracting data
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

K = range(len(strength))
I = range(len(requirement[0]))

# Create the problem
problem = pulp.LpProblem("ManpowerManagement", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (K, I), lowBound=0)
overmanning_vars = pulp.LpVariable.dicts("overmanning", (K, I), lowBound=0)
short_vars = pulp.LpVariable.dicts("short", (K, I), lowBound=0)

# Objective Function
problem += pulp.lpSum(costredundancy[k] * recruit_vars[k][i] + 
                      costoverman[k] * overmanning_vars[k][i] + 
                      costshort[k] * short_vars[k][i] 
                      for k in K for i in I)

# Constraints
for k in K:
    for i in I:
        # Current manpower
        problem += (strength[k] - 
                     pulp.lpSum(lessonewaste[k] * recruit_vars[k][j] for j in range(i + 1)) - 
                     moreonewaste[k] * strength[k] * (i + 1) + 
                     recruit_vars[k][i] + 
                     overmanning_vars[k][i] - 
                     short_vars[k][i] == requirement[k][i])

# Wastage for less than one year
for k in K:
    for i in I:
        if i > 0:
            problem += pulp.lpSum(recruit_vars[k][j] * lessonewaste[k] for j in range(i)) <= strength[k]

# Wastage for more than one year
for k in K:
    for i in I:
        if i > 0:
            problem += pulp.lpSum(strength[k] * moreonewaste[k] for j in range(i)) <= strength[k]

# Recruitment limits
for k in K:
    for i in I:
        problem += recruit_vars[k][i] <= recruit[k]

# Overmanning limits
for k in K:
    problem += pulp.lpSum(overmanning_vars[k][i] for i in I) <= num_overman

# Short-time working limits
for k in K:
    for i in I:
        problem += short_vars[k][i] <= num_shortwork

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')