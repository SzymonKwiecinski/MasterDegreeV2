import pulp

# Define the data parameters
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

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

K = len(requirement)  # Number of manpower categories
I = len(requirement[0])  # Number of years

# Define the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function: Minimize total costs
problem += (
    pulp.lpSum(cost_short[k] * short[k, i] for k in range(K) for i in range(I)) +
    pulp.lpSum(cost_overman[k] * overmanning[k, i] for k in range(K) for i in range(I)) +
    pulp.lpSum(cost_redundancy[k] * redundancy[k, i] for k in range(K) for i in range(I))
)

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower balance equation
        if i == 0:
            manpower_balance = strength[k] - redundancy[k, i] + recruit[k, i] * (1 - lessonewaste[k])
        else:
            manpower_balance = (strength[k] if i == 0 else manpower_balance) * (1 - moreonewaste[k]) \
                               - redundancy[k, i] + recruit[k, i] * (1 - lessonewaste[k])

        # Requirement constraint
        problem += manpower_balance >= requirement[k][i] - short[k, i] * 0.5 - overmanning[k, i]

        # Recruitment limits
        problem += recruit[k, i] <= recruit_limit[k]

        # Short-time working limits
        problem += short[k, i] <= num_shortwork

        # Overmanning limits
        problem += overmanning[k, i] <= num_overman

# Solve the problem
problem.solve()

# Output Results
output = {
    "recruit": [[pulp.value(recruit[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k, i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')