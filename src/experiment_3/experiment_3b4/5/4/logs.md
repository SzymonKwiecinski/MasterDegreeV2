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
To formulate this problem as a Mixed Integer Linear Programming (MILP) model, we aim to determine the optimal schedule for nurses to cover the night shifts while minimizing the total number of nurses hired. 

Here is the MILP formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{MILP Formulation for Nurse Scheduling Problem}

\textbf{Objective:}
Minimize the total number of nurses hired.

\[
\text{Minimize } Z = \sum_{j=1}^{7} \text{start}_j
\]

\textbf{Constraints:}

1. Ensure that the demand on each day \( j \) is met:

For each day \( j \in \{1,...,7\} \), the total number of nurses covering the night shift should be greater than or equal to the demand \( d_j \).

\[
\sum_{i=0}^{\text{period}-1} \text{start}_{(j-i-1) \mod 7 + 1} \geq d_j, \quad \forall j = 1, \ldots, 7
\]

Where \((j-i-1) \mod 7 + 1\) ensures a cyclic consideration of days leading up to day \( j \).

2. Non-negativity constraints:

\[
\text{start}_j \geq 0 \quad \text{and integer}, \quad \forall j = 1, \ldots, 7
\]

\textbf{Variables:}

- \(\text{start}_j\): The number of nurses starting their period on day \( j \).

\textbf{Parameters:}

- \(d_j\): Demand for nurses on day \( j \).
- \(\text{period}\): Number of consecutive days each nurse works.

\end{document}
```

This LaTeX code defines the objective function as minimizing the total number of nurses hired, while the constraints ensure that the demand for nurses each day is met. The modulo operation in the constraints helps manage the cyclic nature of the scheduling over the 7-day week period and considers the period days for which a nurse works consecutively.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{MILP Formulation for Nurse Scheduling Problem}

\textbf{Objective:}
Minimize the total number of nurses hired.

\[
\text{Minimize } Z = \sum_{j=1}^{7} \text{start}_j
\]

\textbf{Constraints:}

1. Ensure that the demand on each day \( j \) is met:

For each day \( j \in \{1,...,7\} \), the total number of nurses covering the night shift should be greater than or equal to the demand \( d_j \).

\[
\sum_{i=0}^{\text{period}-1} \text{start}_{(j-i-1) \mod 7 + 1} \geq d_j, \quad \forall j = 1, \ldots, 7
\]

Where \((j-i-1) \mod 7 + 1\) ensures a cyclic consideration of days leading up to day \( j \).

2. Non-negativity constraints:

\[
\text{start}_j \geq 0 \quad \text{and integer}, \quad \forall j = 1, \ldots, 7
\]

\textbf{Variables:}

- \(\text{start}_j\): The number of nurses starting their period on day \( j \).

\textbf{Parameters:}

- \(d_j\): Demand for nurses on day \( j \).
- \(\text{period}\): Number of consecutive days each nurse works.

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

#### Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Variables: Number of nurses starting on each day (integer and non-negative)
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')

#### Objective: Minimize the total number of nurses hired
problem += pulp.lpSum([start[j] for j in range(1, T + 1)])

#### Constraints: Ensure the demand on each day is met
for j in range(1, T + 1):
    problem += pulp.lpSum([start[(j-i-1) % T + 1] for i in range(period)]) >= demand[j-1], f"Demand_Day_{j}"

#### Solve
problem.solve()

#### Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

