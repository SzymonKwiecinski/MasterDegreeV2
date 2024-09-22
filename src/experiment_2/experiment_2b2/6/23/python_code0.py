import pulp

# Data input
data = {'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}

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

K = len(requirement)  # Number of manpower categories
I = len(requirement[0])  # Number of years

# Initialize problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overman_vars = pulp.LpVariable.dicts("Overman", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=num_overman, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=num_shortwork, cat='Integer')

# Objective function: Minimize costs
problem += pulp.lpSum(costredundancy[k] * (pulp.lpSum(recruit_vars[k, i] for i in range(I)) + strength[k] - requirement[k][0] - (
   moreonewaste[k] * (strength[k] - recruit_vars[k, 0]) - lessonewaste[k] * recruit_vars[k, 0])) 
   + costoverman[k] * overman_vars[k, i] + costshort[k] * short_vars[k, i] for k in range(K) for i in range(I))

# Constraints

# Initial supply constraints (for year 1)
for k in range(K):
    problem += (strength[k] - moreonewaste[k] * strength[k] + recruit_vars[k, 0] - (1 - lessonewaste[k]) * recruit_vars[k, 0]
                + overman_vars[k, 0] + 0.5 * short_vars[k, 0] >= requirement[k][0], f"Initial_Constraint_{k}")

# Keeping track of supply and redundancy for subsequent years
for k in range(K):
    for i in range(1, I):
        problem += (strength[k] * (1 - moreonewaste[k]) +
                    recruit_vars[k, i - 1] * lessonewaste[k] + recruit_vars[k, i] - (1 - lessonewaste[k]) * recruit_vars[k, i]
                    + overman_vars[k, i] + 0.5 * short_vars[k, i] >= requirement[k][i], f"Supply_Constraint_{k}_{i}")

# Maximum recruitment constraints
for k in range(K):
    for i in range(I):
        problem += (recruit_vars[k, i] <= recruit[k], f"Recruitment_Constraint_{k}_{i}")

# Solve the problem
problem.solve()

# Prepare the solution output format
solution = {
    "recruit": [[pulp.value(recruit_vars[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overman_vars[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k, i]) for i in range(I)] for k in range(K)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')