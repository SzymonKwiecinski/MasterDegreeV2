import pulp
import json

data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, 
                        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, 
                        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, 
                        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, 
                        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, 
                        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 
        'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Create the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Create decision variables
translators = data['translators']
required_languages = data['required_languages']

x = pulp.LpVariable.dicts("translators", [translator['id'] for translator in translators], cat='Binary')

# Objective function
problem += pulp.lpSum(translator['cost'] * x[translator['id']] for translator in translators)

# Constraints
for language in required_languages:
    problem += pulp.lpSum(x[translator['id']] for translator in translators if language in translator['languages']) >= 1

# Solve the problem
problem.solve()

# Get selected translators and total cost
selected_translators = [translator['id'] for translator in translators if x[translator['id']].value() == 1]
total_cost = pulp.value(problem.objective)

# Output the result
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')