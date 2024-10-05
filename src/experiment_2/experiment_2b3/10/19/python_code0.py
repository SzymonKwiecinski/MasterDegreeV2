import pulp

# Data
data = {'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}

buy_price = data["buy_price"]
sell_price = data["sell_price"]
is_vegetable = data["is_vegetable"]
max_veg = data["max_vegetable_refining_per_month"]
max_non_veg = data["max_non_vegetable_refining_per_month"]
storage_size = data["storage_size"]
storage_cost = data["storage_cost"]
min_hardness = data["min_hardness"]
max_hardness = data["max_hardness"]
hardness = data["hardness"]
init_amount = data["init_amount"]
min_usage = data["min_usage"]
dependencies = data["dependencies"]

I = len(buy_price[0])  # Number of oils
M = len(buy_price)     # Number of months

indexes = [(i, m) for i in range(I) for m in range(M)]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
buy = pulp.LpVariable.dicts("Buy", indexes, 0)
refine = pulp.LpVariable.dicts("Refine", indexes, 0)
storage = pulp.LpVariable.dicts("Storage", indexes, 0, storage_size)
use = pulp.LpVariable.dicts("Use", [(i, m) for i in range(I) for m in range(1, M+1)], 0, 1, cat='Binary')

# Objective
profit = pulp.lpSum(
    [(sell_price - buy_price[m][i]) * refine[i, m] - storage_cost * storage[i, m] for i in range(I) for m in range(M)]
)
problem += profit

# Constraints
for m in range(M):
    problem += (
        pulp.lpSum(storage[i, m] for i in range(I)) <= storage_size,
        f"Storage_Capacity_Month_{m}"
    )
    problem += (
        pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_veg,
        f"Max_Vegetable_Refining_Month_{m}"
    )
    problem += (
        pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_veg,
        f"Max_NonVegetable_Refining_Month_{m}"
    )
    problem += (
        pulp.lpSum(use[i, m+1] for i in range(I)) <= 3,
        f"Max_3_Oils_Use_Month_{m}"
    )
    
    for i in range(I):
        if m == 0:
            problem += (
                storage[i, m] == init_amount + buy[i, m] - refine[i, m],
                f"Initial_Storage_Constraint_Oil_{i}"
            )
        else:
            problem += (
                storage[i, m] == storage[i, m-1] + buy[i, m] - refine[i, m],
                f"Storage_Constraint_Oil_{i}_Month_{m}"
            )
        
        problem += (
            refine[i, m] >= min_usage * use[i, m+1],
            f"Min_Usage_If_Used_Oil_{i}_Month_{m}"
        )
        
        for j, dep in enumerate(dependencies[i]):
            if dep == 1:
                problem += (
                    use[i, m+1] <= use[j, m+1],
                    f"Dependency_Oil_{i}_on_Oil_{j}_Month_{m}"
                )

problem += pulp.lpSum(
    hardness[i] * refine[i, m] for i in range(I) for m in range(M)
) >= min_hardness * pulp.lpSum(refine[i, m] for i in range(I) for m in range(M)), "Min_Hardness"

problem += pulp.lpSum(
    hardness[i] * refine[i, m] for i in range(I) for m in range(M)
) <= max_hardness * pulp.lpSum(refine[i, m] for i in range(I) for m in range(M)), "Max_Hardness"

for i in range(I):
    problem += (
        storage[i, M-1] == init_amount,
        f"Final_Storage_{i}"
    )

# Solve
problem.solve()

# Extract solutions
buy_solution = [[pulp.value(buy[i, m]) for i in range(I)] for m in range(M)]
refine_solution = [[pulp.value(refine[i, m]) for i in range(I)] for m in range(M)]
storage_solution = [[pulp.value(storage[i, m]) for i in range(I)] for m in range(M)]

output = {
    "buy": buy_solution,
    "refine": refine_solution,
    "storage": storage_solution
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')