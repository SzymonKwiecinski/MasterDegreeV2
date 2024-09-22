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

\section*{Mathematical Model for Nurse Scheduling}

\subsection*{Parameters}
\begin{itemize}
    \item \( d_j \): Demand for nurses on day \( j \) where \( j = 1, \ldots, 7 \).
    \item \( \text{period} \): Number of consecutive days a nurse works.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_j \): Number of nurses that start their shift on day \( j \) where \( j = 1, \ldots, 7 \).
    \item \( N \): Total number of nurses hired.
\end{itemize}

\subsection*{Objective}
\[
\text{Minimize } N = \sum_{j=1}^{7} x_j
\]

\subsection*{Constraints}
The demand for nurses must be satisfied for each day \( j \):
\[
\sum_{k=1}^{7} x_{(j-k+1) \text{ mod } 7 + 1} \geq d_j \quad \text{for } j = 1, \ldots, 7
\]

Where \( x_{(j-k+1) \text{ mod } 7 + 1} \) accounts for the \( \text{period} \) of consecutive shifts.

\subsection*{Non-negativity Constraints}
\[
x_j \geq 0 \quad \text{for } j = 1, \ldots, 7
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

\section*{Mathematical Model for Nurse Scheduling}

\subsection*{Parameters}
\begin{itemize}
    \item \( d_j \): Demand for nurses on day \( j \) where \( j = 1, \ldots, 7 \).
    \item \( \text{period} \): Number of consecutive days a nurse works.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_j \): Number of nurses that start their shift on day \( j \) where \( j = 1, \ldots, 7 \).
    \item \( N \): Total number of nurses hired.
\end{itemize}

\subsection*{Objective}
\[
\text{Minimize } N = \sum_{j=1}^{7} x_j
\]

\subsection*{Constraints}
The demand for nurses must be satisfied for each day \( j \):
\[
\sum_{k=1}^{7} x_{(j-k+1) \text{ mod } 7 + 1} \geq d_j \quad \text{for } j = 1, \ldots, 7
\]

Where \( x_{(j-k+1) \text{ mod } 7 + 1} \) accounts for the \( \text{period} \) of consecutive shifts.

\subsection*{Non-negativity Constraints}
\[
x_j \geq 0 \quad \text{for } j = 1, \ldots, 7
\]

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
Demand = data['Demand']

#### Create a linear programming problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0, cat='Integer')

#### Objective function: Minimize total number of nurses hired
problem += pulp.lpSum(x[j] for j in range(1, T + 1)), "Total_Nurses_Hired"

#### Constraints to meet demand for each day
for j in range(1, T + 1):
    problem += (
        pulp.lpSum(x[(j - k) % T + 1] for k in range(Period)) >= Demand[j - 1],
        f"Demand_Constraint_Day_{j}"
    )

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

