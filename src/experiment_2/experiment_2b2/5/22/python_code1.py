import pulp

# Data
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
recruit_capacity = data['recruit']
cost_redundancy = data['costredundancy']
num_overman = data['num_overman']
cost_overman = data['costoverman']
num_shortwork = data['num_shortwork']
cost_short = data['costshort']

K = len(strength)
I = len(requirement[0])

# Problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, cat='Integer')
redundancy_vars = pulp.LpVariable.dicts("Redundancy", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(redundancy_vars[k][i] * cost_redundancy[k] for k in range(K) for i in range(I))

# Constraints
manpower_vars = [[pulp.LpVariable(f"Manpower_{k}_{i}", lowBound=0, cat='Continuous') for i in range(I)] for k in range(K)]

for k in range(K):
    for i in range(I):
        if i == 0:
            manpower_start = strength[k]
        else:
            manpower_start = (1 - moreonewaste[k]) * (manpower_vars[k][i - 1] + recruit_vars[k][i - 1] * (1 - lessonewaste[k]))

        manpower = manpower_start + recruit_vars[k][i] - redundancy_vars[k][i] + overmanning_vars[k][i] - short_vars[k][i] * 0.5
        problem += manpower_vars[k][i] == manpower

        # Meet manpower requirement
        problem += manpower_vars[k][i] >= requirement[k][i]

        # Maximum recruit constraint
        problem += recruit_vars[k][i] <= recruit_capacity[k]

        # Maximum short-time working constraint
        problem += short_vars[k][i] <= num_shortwork

        # Overmanning constraint
        problem += overmanning_vars[k][i] <= num_overman

problem.solve()

# Results
recruit_solution = [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)]
overmanning_solution = [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)]
short_solution = [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]

output = {
    "recruit": recruit_solution,
    "overmanning": overmanning_solution,
    "short": short_solution
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')