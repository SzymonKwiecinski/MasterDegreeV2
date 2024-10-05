import pulp

# Data
data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']},
                        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']},
                        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']},
                        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']},
                        {'id': 5, 'cost': 9000,  'languages': ['FR', 'GE', 'RU', 'SP']},
                        {'id': 6, 'cost': 7000,  'languages': ['GE', 'SP', 'PO']}],
        'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

translators = data["translators"]
required_languages = data["required_languages"]

# Problem
problem = pulp.LpProblem("Translators_Selection", pulp.LpMinimize)

# Variables
translator_vars = pulp.LpVariable.dicts("Translator", (translator['id'] for translator in translators), cat='Binary')

# Objective
problem += pulp.lpSum(translator['cost'] * translator_vars[translator['id']] for translator in translators)

# Constraints
for language in required_languages:
    problem += pulp.lpSum(translator_vars[translator['id']] for translator in translators if language in translator['languages']) >= 1

# Solve
problem.solve()

# Output
selected_translators = [translator['id'] for translator in translators if translator_vars[translator['id']].varValue == 1]
total_cost = sum(translator['cost'] for translator in translators if translator_vars[translator['id']].varValue == 1)

output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')