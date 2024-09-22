import pulp

data = {'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}

requirements = data['requirement']
initial_strength = data['strength']
lessone_wastage = data['lessonewaste']
moreone_wastage = data['moreonewaste']
recruit_limit = data['recruit']
cost_redundancy = data['costredundancy']
num_overman = data['num_overman']
cost_overman = data['costoverman']
num_shortwork = data['num_shortwork']
cost_short = data['costshort']

K = len(requirements)  # number of manpower categories
I = len(requirements[0])  # number of years

problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short_work = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("Redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective: Minimize redundancy cost
problem += pulp.lpSum(redundancy[k, i] * cost_redundancy[k] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            # Initial year manpower balance
            manpower_after_wastage = initial_strength[k] * (1 - moreone_wastage[k])
        else:
            # Manpower balance after wastage
            manpower_after_wastage = (
                recruit[k, i-1] * (1 - lessone_wastage[k]) +
                (initial_strength[k] - recruit[k, i-1]) * (1 - moreone_wastage[k])
            )

        # Manpower balance equation
        problem += (
            manpower_after_wastage + recruit[k, i] + short_work[k, i] / 2 +
            overmanning[k, i] - redundancy[k, i] == requirements[k][i]
        )

        # Recruitment limit
        problem += recruit[k, i] <= recruit_limit[k]

        # Short-time working limit
        problem += short_work[k, i] <= num_shortwork

        # Overmanning limit
        problem += overmanning[k, i] <= num_overman

# Solve problem
problem.solve()

# Prepare output
output = {
    "recruit": [[pulp.value(recruit[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_work[k, i]) for i in range(I)] for k in range(K)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')