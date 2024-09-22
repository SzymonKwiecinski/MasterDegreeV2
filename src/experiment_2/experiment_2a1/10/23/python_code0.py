import pulp
import json

data = {'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
        'strength': [2000, 1500, 1000], 
        'lessonewaste': [0.25, 0.2, 0.1], 
        'moreonewaste': [0.1, 0.05, 0.05], 
        'recruit': [500, 800, 500], 
        'costredundancy': [200, 500, 500], 
        'num_overman': 150, 
        'costoverman': [1500, 2000, 3000], 
        'num_shortwork': 50, 
        'costshort': [500, 400, 400]}

K = len(data['strength'])
I = len(data['requirement'][0])
requirements = data['requirement']
strengths = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

# Define the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective function
total_cost = (
    pulp.lpSum(costredundancy[k] * (strengths[k] - pulp.lpSum(recruit_vars[k][i] for i in range(I))) for k in range(K)) + 
    pulp.lpSum(costoverman[k] * overmanning_vars[k][i] for k in range(K) for i in range(I)) +
    pulp.lpSum(costshort[k] * short_vars[k][i] for k in range(K) for i in range(I))
)

problem += total_cost

# Constraints
for k in range(K):
    for i in range(I):
        problem += (strengths[k] - pulp.lpSum(recruit_vars[k][j] for j in range(i + 1)) +
                     pulp.lpSum(overmanning_vars[k][j] for j in range(I)) -
                     pulp.lpSum(short_vars[k][j] for j in range(I)) >= requirements[k][i] - (num_overman if i == I-1 else 0), f"Manpower_Constraint_{k}_{i}")

# Recruitment constraints
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k][i] <= recruit[k], f"Recruit_Limit_{k}_{i}"

# Short work limits
for k in range(K):
    for i in range(I):
        problem += short_vars[k][i] <= num_shortwork, f"Short_Work_Limit_{k}_{i}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')