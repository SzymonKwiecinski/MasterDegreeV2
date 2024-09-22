import pulp
import json

# Input data
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Problem Parameters
K = len(data['strength'])  # number of manpower categories
I = len(data['requirement'][0])  # number of years

# Create the problem variable
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), 0, None, pulp.LpInteger)
overmanning_vars = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), 0, None, pulp.LpInteger)
short_vars = pulp.LpVariable.dicts("Short", (range(K), range(I)), 0, None, pulp.LpInteger)

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - 
           (data['requirement'][k][i] - 
           (data['lessonewaste'][k] * data['strength'][k] + 
            data['moreonewaste'][k] * data['strength'][k] - 
            recruit_vars[k][i] -
            overmanning_vars[k][i] -
            short_vars[k][i] / 2))) 
           for k in range(K) for i in range(I)), "Total_Cost"

# Constraints
# Strength Constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] + 
                     pulp.lpSum(recruit_vars[k][j] for j in range(i + 1)) - 
                     pulp.lpSum(overmanning_vars[k][j] for j in range(i + 1)) - 
                     pulp.lpSum(short_vars[k][j] for j in range(i + 1)) -
                     data['requirement'][k][i] >= 0, f'Strength_Constraint_{k}_{i}')

# Recruitment Limits
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k][i] <= data['recruit'][k], f'Recruit_Limit_{k}_{i}'

# Overmanning Constraints
for k in range(K):
    for i in range(I):
        problem += overmanning_vars[k][i] <= data['num_overman'], f'Overmanning_Limit_{k}_{i}'

# Short-time working Constraints
for k in range(K):
    for i in range(I):
        problem += short_vars[k][i] <= data['num_shortwork'], f'Short_Time_Work_Limit_{k}_{i}'

# Solve the problem
problem.solve()

# Output Results
recruit_output = [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)]
overmanning_output = [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)]
short_output = [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]

output = {
    "recruit": recruit_output,
    "overmanning": overmanning_output,
    "short": short_output
}

print(json.dumps(output, indent=4))

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')