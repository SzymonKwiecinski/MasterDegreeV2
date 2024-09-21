import pulp
import json

# Data provided
data = {
    'translators': [
        {'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']},
        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']},
        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']},
        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']},
        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']},
        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}
    ],
    'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']
}

# Extracting data
translators = data['translators']
required_languages = data['required_languages']

# Number of translators
N = len(translators)
# Number of required languages
M = len(required_languages)

# Creating the linear programming problem
problem = pulp.LpProblem("Translator_Hiring_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum(translators[i]['cost'] * x[i] for i in range(N)), "Total_Hiring_Cost"

# Constraints
for j in required_languages:
    problem += pulp.lpSum(x[i] for i in range(N) if j in translators[i]['languages']) >= 1, f"Language_{j}_Coverage"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')