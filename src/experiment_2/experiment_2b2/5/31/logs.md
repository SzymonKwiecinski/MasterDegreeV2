# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- A number of power stations are committed to meeting the following electricity load demands over a day.
- Period \var{t} of a day has demand \var{demand_{t}}.
- There are several types of generating unit available: the number of \var{k}-th type units is \var{num_{k}}.
- Type \var{k} generator has to work between a minimum level \var{minlevel_{k}} and a maximum level \var{maxlevel_{k}}. 
- There is an hourly cost of running each type \var{k} generator at minimum level \var{runcost_{k}}. 
- In addition, there is an extra hourly cost \var{extracost_{k}} for each megawatt at which a type \var{k} unit is operated above the minimum level. 
- Starting up a type \var{k} generator also involves a cost \var{startcost_{k}}.


INPUT FORMAT:

{
    "demand": [demand_{t} for t in 1,...,T],
    "num": [num_{k} for in 1,...,K],
    "minlevel": [minlevel_{k} for in 1,...,K],
    "maxlevel": [minlevel_{k} for in 1,...,K],
    "runcost": [runcost_{k} for in 1,...,K],
    "extracost": [extracost_{k} for in 1,...,K],
    "startcost": [startcost_{k} for in 1,...,K]
}


OBJECTIVE: Which generators should be working in which periods of the day to minimize total cost?

OUTPUT INFO:

- \var{numon} represents the number of generators of each type that are on in each period

OUTPUT FORMAT:

{
    "numon": [[numon_{k, t} for t in 1,...,T] for k in 1,...,K]
}
</DESCRIPTION>
<DATA>
{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

#### Constants
T = len(data['demand'])
K = len(data['num'])

#### Problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), cat='Binary')  #### 1 if generator k operates at time t
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')  #### Power above min level
z = pulp.LpVariable.dicts("z", ((k, t) for k in range(K) for t in range(T)), cat='Binary')  #### 1 if generator k is started at time t

#### Objective function: cost minimization
problem += pulp.lpSum([
    x[k, t] * data['runcost'][k] +
    y[k, t] * data['extracost'][k] +
    z[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
])

#### Constraints
for t in range(T):
    #### Demand constraint
    problem += pulp.lpSum([
        x[k, t] * data['minlevel'][k] + y[k, t]
        for k in range(K)
    ]) >= data['demand'][t]

    for k in range(K):
        #### Number of generators constraint
        problem += x[k, t] <= data['num'][k]

        #### Power output must be between min and max
        problem += y[k, t] <= x[k, t] * (data['maxlevel'][k] - data['minlevel'][k])

        #### Start-up constraint
        if t > 0:
            problem += z[k, t] >= x[k, t] - x[k, t - 1]
        else:
            problem += z[k, t] >= x[k, t]

#### Solve the problem
problem.solve()

#### Retrieve the results
numon = [[int(x[k, t].varValue) for t in range(T)] for k in range(K)]

#### Output
solution = {
    "numon": numon
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

