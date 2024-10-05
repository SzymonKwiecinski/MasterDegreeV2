# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To create a mathematical model for this problem, we need to establish a Mixed-Integer Linear Programming (MILP) model. The goal is to minimize the number of nurses needed while meeting the demand for each night shift.

Let's define our variables and constraints:

- Variables:
  - Let \( \text{start}_j \) be the number of nurses starting their period on day \( j \), where \( j = 1, \ldots, 7 \).
  - Let \( \text{total} \) be the total number of nurses hired.

- Parameters:
  - \( \text{period} \) is the number of consecutive days each nurse works.
  - \( d_j \) is the demand for nurses on day \( j \).

- Objective:
  - Minimize the total number of nurses hired.

- Constraints:
  - Ensure that the demand for each day \( j \) is satisfied by considering the cyclic nature of the schedule. A nurse starting on day \( j \) will work on days \( j, j+1, \ldots, j+\text{period}-1 \mod 7 \).

Now, let's write this in a mathematical format using LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{MILP Model for Nurse Scheduling:}

\begin{align*}
\min \quad & \text{total} = \sum_{j=1}^{7} \text{start}_j \\
\text{s.t.} \quad & \sum_{k=0}^{\text{period}-1} \text{start}_{(j-k-1) \mod 7 + 1} \geq d_j, \quad j = 1, \ldots, 7 \\
& \text{start}_j \geq 0, \quad \text{integer}, \quad j = 1, \ldots, 7 \\
\end{align*}

\end{document}
```

Explanation:
- The objective function minimizes the total number of nurses, which is the sum of nurses starting their period each day.
- The first constraint ensures that the sum of nurses working on any day \( j \) (who started their work period within the last \text{period} days) meets or exceeds the demand \( d_j \).
- The constraint \((j-k-1) \mod 7 + 1\) handles the cyclic nature of the week where the schedule wraps around after day 7.
- The variables \(\text{start}_j\) are required to be non-negative integers, as we cannot hire fractional nurses or negative numbers of nurses.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{MILP Model for Nurse Scheduling:}

\begin{align*}
\min \quad & \text{total} = \sum_{j=1}^{7} \text{start}_j \\
\text{s.t.} \quad & \sum_{k=0}^{\text{period}-1} \text{start}_{(j-k-1) \mod 7 + 1} \geq d_j, \quad j = 1, \ldots, 7 \\
& \text{start}_j \geq 0, \quad \text{integer}, \quad j = 1, \ldots, 7 \\
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data_json = '''{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}'''
data = json.loads(data_json.replace("'", '"'))

#### Define model
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Define variables
start = pulp.LpVariable.dicts("start", range(1, data['T'] + 1), lowBound=0, cat='Integer')

#### Objective function
problem += pulp.lpSum(start[j] for j in range(1, data['T'] + 1)), "Total_Starts"

#### Constraints
for j in range(1, data['T'] + 1):
    problem += pulp.lpSum(start[(j - k - 1) % data['T'] + 1] for k in range(data['Period'])) >= data['Demand'][j - 1], f"Demand_Constraint_{j}"

#### Solve the problem
problem.solve()

#### Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

