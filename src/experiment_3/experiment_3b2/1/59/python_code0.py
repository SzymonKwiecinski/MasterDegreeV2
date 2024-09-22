import pulp
import json

# Data provided in JSON format
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

# Problem definition
problem = pulp.LpProblem("Translator_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", [t['id'] for t in translators], cat='Binary')

# Objective function
problem += pulp.lpSum(t['cost'] * x[t['id']] for t in translators)

# Constraints for covering required languages
for lang in required_languages:
    problem += (
        pulp.lpSum(x[t['id']] for t in translators if lang in t['languages']) >= 1,
        f"Coverage_{lang}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')