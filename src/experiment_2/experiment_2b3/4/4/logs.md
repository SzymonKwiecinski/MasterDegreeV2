# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO: 
- A hospital wants to make a weekly night shift (12pm-8am) schedule for its nurses. 
- The demand for nurses for the night shift on day \var{j} = 1,...,7 is an integer \var{d_j}. 
- Every nurse works \var{period} days in a row on the night shift, followed by (7 - \var{period}) days off.


INPUT FORMAT: 

{
    "period": period,
    "demand": [d_j for j in 1, ...,7]
}

OBJECTIVE: The goal is to find the minimal number of nurses the hospital needs to hire. 

OUTPUT INFO: 

- for each day \var{j} = 1,...,7, \var{start_j} which shows the number of nurses that start their period on day \var{j}.
- the total number of nurses hired.

OUTPUT FORMAT:

{
    "start": [start_j for j in 1, ...,7],
    "total": total
}


</DESCRIPTION>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parsing data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

#### Initialize problem
problem = pulp.LpProblem("Minimize_Nurses", pulp.LpMinimize)

#### Decision variables
start_nurses = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

#### Objective function: Minimize total number of nurses
total_nurses = pulp.lpSum(start_nurses)
problem += total_nurses

#### Constraints
for j in range(T):
    #### Sum of nurses covering day j
    nurses_covering_j = pulp.lpSum(start_nurses[(j - i) % T] for i in range(period))
    problem += (nurses_covering_j >= demand[j], f"demand_constraint_{j}")

#### Solve the problem
problem.solve()

#### Extract results
schedule = [int(start_nurses[j].varValue) for j in range(T)]
total_hired = int(pulp.value(total_nurses))

#### Print results
output = {
    "start": schedule,
    "total": total_hired
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

