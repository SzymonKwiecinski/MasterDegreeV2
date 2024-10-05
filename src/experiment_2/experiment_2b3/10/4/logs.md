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

#### Data input from the JSON format
data = {
    'T': 7, 
    'Period': 4, 
    'Demand': [0, 5, 9, 15, 4, 7, 3]
}

#### Extracting data from the input
T = data['T']
period = data['Period']
demand = data['Demand']

#### Initialize the problem
problem = pulp.LpProblem("Nurse_Shift_Scheduling", pulp.LpMinimize)

#### Decision variables: start_j for each day j
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

#### Objective function: minimize total number of nurses
problem += pulp.lpSum(start), "Total_Nurses"

#### Constraints: demand for each day j
for j in range(T):
    problem += pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j], f"Demand_day_{j+1}"

#### Solve the problem
problem.solve()

#### Prepare output
result = {
    "start": [int(start[j].varValue) for j in range(T)],
    "total": int(pulp.value(problem.objective))
}

#### Print the result
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

