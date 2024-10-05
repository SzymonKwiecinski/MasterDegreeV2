import pulp

# Load data
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
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(requirement)
I = len(requirement[0])

# Create a problem instance
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overman_vars = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("ShortTime", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy_vars = pulp.LpVariable.dicts("Redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([
    recruit_vars[k, i] * 0 + 
    redundancy_vars[k, i] * costredundancy[k] + 
    overman_vars[k, i] * costoverman[k] + 
    short_vars[k, i] * costshort[k]
    for k in range(K) for i in range(I)
])

# Constraints
for k in range(K):
    # Initial strength considering more than one-year wastage
    current_strength = strength[k] * (1 - moreonewaste[k])
    for i in range(I):
        # Employees staying for more than one year
        if i > 0:
            current_strength = (
                (current_strength - redundancy_vars[k, i-1]) * (1 - moreonewaste[k])
            + recruit_vars[k, i-1] * (1 - lessonewaste[k])
            )

        # Total available workforce
        total_available = current_strength + recruit_vars[k, i]

        # Meeting requirement with short work and overmanning
        problem += (
            total_available + short_vars[k, i] * 0.5 + overman_vars[k, i]
            == requirement[k][i]
        )

        # Limits on recruitment, overmanning, and short time work
        problem += recruit_vars[k, i] <= recruit[k]
        problem += overman_vars[k, i] <= num_overman
        problem += short_vars[k, i] <= num_shortwork

# Solve the problem
problem.solve()

# Results
output = {
    "recruit": [[pulp.value(recruit_vars[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overman_vars[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k, i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')