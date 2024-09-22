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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{MILP Model for Nurse Scheduling}
\author{}
\date{}
\maketitle

\section*{Problem Definition}
Let \( n \) be the total number of nurses needed, and let \( \text{period} \) be the number of days each nurse works consecutively. Let \( d_j \) be the demand for nurses on day \( j \) for \( j = 1, \ldots, 7 \).

\section*{Variables}
Define the decision variables:
\begin{itemize}
    \item \( x_j \): the number of nurses that start their shift on day \( j \) for \( j = 1, \ldots, 7 \).
    \item \( n \): the total number of nurses hired.
\end{itemize}

\section*{Objective Function}
The goal is to minimize the total number of nurses hired:
\[
\text{Minimize } n = \sum_{j=1}^{7} x_j
\]

\section*{Constraints}
Each nurse works for \( \text{period} \) days and has \( 7 - \text{period} \) days off. We need to ensure that the demand for nurses is met on each day \( j \):

For each day \( j \):
\[
\sum_{k=0}^{\text{period}-1} x_{(j-k) \mod 7} \geq d_j \quad \text{for } j = 1, \ldots, 7
\]

Where \( x_{(j-k) \mod 7} \) represents the nurses starting their shift on day \( (j-k) \). The calculation ensures that the demand \( d_j \) is met by the nurses who started on the previous \( \text{period} \) days.

\section*{Final Model}
The full Mixed Integer Linear Programming (MILP) formulation is as follows:

\begin{align*}
\text{Minimize } & \quad n = \sum_{j=1}^{7} x_j \\
\text{subject to } & \quad \sum_{k=0}^{\text{period}-1} x_{(j-k) \mod 7} \geq d_j, & \quad j = 1, \ldots, 7 \\
& \quad x_j \geq 0 \quad \text{and integer for } j = 1, \ldots, 7
\end{align*}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{MILP Model for Nurse Scheduling}
\author{}
\date{}
\maketitle

\section*{Problem Definition}
Let \( n \) be the total number of nurses needed, and let \( \text{period} \) be the number of days each nurse works consecutively. Let \( d_j \) be the demand for nurses on day \( j \) for \( j = 1, \ldots, 7 \).

\section*{Variables}
Define the decision variables:
\begin{itemize}
    \item \( x_j \): the number of nurses that start their shift on day \( j \) for \( j = 1, \ldots, 7 \).
    \item \( n \): the total number of nurses hired.
\end{itemize}

\section*{Objective Function}
The goal is to minimize the total number of nurses hired:
\[
\text{Minimize } n = \sum_{j=1}^{7} x_j
\]

\section*{Constraints}
Each nurse works for \( \text{period} \) days and has \( 7 - \text{period} \) days off. We need to ensure that the demand for nurses is met on each day \( j \):

For each day \( j \):
\[
\sum_{k=0}^{\text{period}-1} x_{(j-k) \mod 7} \geq d_j \quad \text{for } j = 1, \ldots, 7
\]

Where \( x_{(j-k) \mod 7} \) represents the nurses starting their shift on day \( (j-k) \). The calculation ensures that the demand \( d_j \) is met by the nurses who started on the previous \( \text{period} \) days.

\section*{Final Model}
The full Mixed Integer Linear Programming (MILP) formulation is as follows:

\begin{align*}
\text{Minimize } & \quad n = \sum_{j=1}^{7} x_j \\
\text{subject to } & \quad \sum_{k=0}^{\text{period}-1} x_{(j-k) \mod 7} \geq d_j, & \quad j = 1, \ldots, 7 \\
& \quad x_j \geq 0 \quad \text{and integer for } j = 1, \ldots, 7
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON
data_json = '{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}'
data = json.loads(data_json)

#### Parameters
T = data['T']  #### Total days (7)
Period = data['Period']  #### Working period (4)
Demand = data['Demand']  #### Demand for each day

#### Define the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Integer') for j in range(1, T + 1)]

#### Objective Function
problem += pulp.lpSum(x[j - 1] for j in range(1, T + 1)), "Total_Nurses_Hired"

#### Constraints to meet demand
for j in range(T):
    problem += (pulp.lpSum(x[(j - k) % T] for k in range(Period)) >= Demand[j]), f"Demand_Constraint_{j + 1}"

#### Solve the problem
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

