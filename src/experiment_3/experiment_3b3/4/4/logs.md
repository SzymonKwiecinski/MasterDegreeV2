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

\section*{Mathematical Model for Nurse Scheduling Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $period$: The number of consecutive days a nurse works the night shift.
    \item $d_j$: The demand for nurses on night shift for day $j$, where $j = 1, \ldots, 7$.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $start_j$: The number of nurses that start their shift on day $j$, where $j = 1, \ldots, 7$.
    \item $total$: The total number of nurses hired.
\end{itemize}

\subsection*{Objective}
Minimize the total number of nurses hired:
\[
\text{Minimize } total = \sum_{j=1}^{7} start_j
\]

\subsection*{Constraints}
The demand for nurses on each day must be satisfied, which can be expressed as:
\[
\sum_{i=0}^{period-1} start_{(j-i) \mod 7} \geq d_j, \quad \forall j = 1, \ldots, 7
\]
where $start_{(j-i) \mod 7}$ is the number of nurses starting on day $j-i$.

\subsection*{Non-negativity Constraints}
All variables must be non-negative integers:
\[
start_j \geq 0 \quad \forall j = 1, \ldots, 7
\]
\[
total \geq 0
\]

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

\section*{Mathematical Model for Nurse Scheduling Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $period$: The number of consecutive days a nurse works the night shift.
    \item $d_j$: The demand for nurses on night shift for day $j$, where $j = 1, \ldots, 7$.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $start_j$: The number of nurses that start their shift on day $j$, where $j = 1, \ldots, 7$.
    \item $total$: The total number of nurses hired.
\end{itemize}

\subsection*{Objective}
Minimize the total number of nurses hired:
\[
\text{Minimize } total = \sum_{j=1}^{7} start_j
\]

\subsection*{Constraints}
The demand for nurses on each day must be satisfied, which can be expressed as:
\[
\sum_{i=0}^{period-1} start_{(j-i) \mod 7} \geq d_j, \quad \forall j = 1, \ldots, 7
\]
where $start_{(j-i) \mod 7}$ is the number of nurses starting on day $j-i$.

\subsection*{Non-negativity Constraints}
All variables must be non-negative integers:
\[
start_j \geq 0 \quad \forall j = 1, \ldots, 7
\]
\[
total \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Read data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

#### Problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

#### Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')
total = pulp.LpVariable("total", lowBound=0, cat='Integer')

#### Objective
problem += total

#### Constraints
problem += total == pulp.lpSum([start[j] for j in range(T)])

for j in range(T):
    problem += pulp.lpSum([start[(j-i) % T] for i in range(period)]) >= demand[j]

#### Solve
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

