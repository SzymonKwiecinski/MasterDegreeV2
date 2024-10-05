import pulp

# Load data
data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, 
                        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, 
                        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, 
                        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, 
                        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, 
                        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 
        'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Initialize problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Decision variables
translators = data["translators"]
translator_vars = {
    t["id"]: pulp.LpVariable(f"Translator_{t['id']}", cat='Binary')
    for t in translators
}

# Objective function
problem += pulp.lpSum(t["cost"] * translator_vars[t["id"]] for t in translators)

# Constraints to ensure all required languages are covered
required_languages = data['required_languages']
for lang in required_languages:
    problem += pulp.lpSum(translator_vars[t["id"]] for t in translators if lang in t["languages"]) >= 1

# Solve problem
problem.solve()

# Output results
selected_translators = [t["id"] for t in translators if pulp.value(translator_vars[t["id"]]) == 1]
total_cost = sum(t["cost"] for t in translators if pulp.value(translator_vars[t["id"]]) == 1)

output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')