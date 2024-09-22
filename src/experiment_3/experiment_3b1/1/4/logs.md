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

\title{MILP Model for Night Shift Nurse Scheduling}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

\subsection*{Parameters}
\begin{itemize}
    \item Let $N$ be the total number of nurses hired.
    \item Let $d_j$ be the demand for nurses on day $j$, for $j = 1, \ldots, 7$.
    \item Let $period$ be the number of consecutive days a nurse works the night shift.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let $start_j$ be the number of nurses that start their shift on day $j$, for $j = 1, \ldots, 7$.
\end{itemize}

\subsection*{Objective Function}
The goal is to minimize the total number of nurses hired:

\[
\text{Minimize } N = \sum_{j=1}^{7} start_j
\]

\subsection*{Constraints}
For each day $j$, the total number of nurses working the night shift must meet the demand:

\[
\sum_{i=0}^{period - 1} start_{(j - i + 7) \mod 7} \geq d_j, \quad \forall j = 1, \ldots, 7
\]

Where $start_{(j - i + 7) \mod 7}$ represents the number of nurses starting their shift on the day that satisfies the period of work.

We also have the non-negativity constraint:

\[
start_j \geq 0 \quad \forall j = 1, \ldots, 7
\]

\subsection*{Output}
The output will be as follows:

\begin{verbatim}
{
    "start": [start_1, start_2, start_3, start_4, start_5, start_6, start_7],
    "total": N
}
\end{verbatim}

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

\title{MILP Model for Night Shift Nurse Scheduling}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

\subsection*{Parameters}
\begin{itemize}
    \item Let $N$ be the total number of nurses hired.
    \item Let $d_j$ be the demand for nurses on day $j$, for $j = 1, \ldots, 7$.
    \item Let $period$ be the number of consecutive days a nurse works the night shift.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let $start_j$ be the number of nurses that start their shift on day $j$, for $j = 1, \ldots, 7$.
\end{itemize}

\subsection*{Objective Function}
The goal is to minimize the total number of nurses hired:

\[
\text{Minimize } N = \sum_{j=1}^{7} start_j
\]

\subsection*{Constraints}
For each day $j$, the total number of nurses working the night shift must meet the demand:

\[
\sum_{i=0}^{period - 1} start_{(j - i + 7) \mod 7} \geq d_j, \quad \forall j = 1, \ldots, 7
\]

Where $start_{(j - i + 7) \mod 7}$ represents the number of nurses starting their shift on the day that satisfies the period of work.

We also have the non-negativity constraint:

\[
start_j \geq 0 \quad \forall j = 1, \ldots, 7
\]

\subsection*{Output}
The output will be as follows:

\begin{verbatim}
{
    "start": [start_1, start_2, start_3, start_4, start_5, start_6, start_7],
    "total": N
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

#### Define the problem
problem = pulp.LpProblem("NurseScheduling", pulp.LpMinimize)

#### Decision variables: start_j for each day j
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

#### Objective function: Minimize the total number of nurses hired
problem += pulp.lpSum(start), "TotalNursesHired"

#### Constraints to meet demand for each day
for j in range(T):
    problem += (pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j], f'DemandConstraint_{j}')

#### Solve the problem
problem.solve()

#### Prepare output
output = {
    "start": [start[j].varValue for j in range(T)],
    "total": pulp.value(problem.objective)
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Print the output
print(json.dumps(output))
```

