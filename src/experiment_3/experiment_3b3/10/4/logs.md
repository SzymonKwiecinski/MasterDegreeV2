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

\section*{Mixed Integer Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item Let $p$ be the period (number of consecutive days a nurse works).
    \item Let $d_j$ be the demand for nurses on day $j$, for $j = 1, \ldots, 7$.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item Let $x_j$ be the number of nurses that start their shift on day $j$, for $j = 1, \ldots, 7$.
    \item Let $N$ be the total number of nurses hired.
\end{itemize}

\subsection*{Objective}
Minimize the total number of nurses hired:
\[
\text{Minimize } N = \sum_{j=1}^{7} x_j
\]

\subsection*{Constraints}
The number of nurses available on each day must meet the demand:
\[
\sum_{j=k}^{k+p-1} x_j \geq d_k \quad \text{for } k = 1, \ldots, 7
\]
where the indices are taken modulo 7 (i.e., day 8 is treated as day 1).

\subsection*{Non-negativity and Integer Constraints}
\[
x_j \geq 0 \quad \text{and integer for } j = 1, \ldots, 7
\]
\[
N \geq 0 \quad \text{and integer}
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

\section*{Mixed Integer Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item Let $p$ be the period (number of consecutive days a nurse works).
    \item Let $d_j$ be the demand for nurses on day $j$, for $j = 1, \ldots, 7$.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item Let $x_j$ be the number of nurses that start their shift on day $j$, for $j = 1, \ldots, 7$.
    \item Let $N$ be the total number of nurses hired.
\end{itemize}

\subsection*{Objective}
Minimize the total number of nurses hired:
\[
\text{Minimize } N = \sum_{j=1}^{7} x_j
\]

\subsection*{Constraints}
The number of nurses available on each day must meet the demand:
\[
\sum_{j=k}^{k+p-1} x_j \geq d_k \quad \text{for } k = 1, \ldots, 7
\]
where the indices are taken modulo 7 (i.e., day 8 is treated as day 1).

\subsection*{Non-negativity and Integer Constraints}
\[
x_j \geq 0 \quad \text{and integer for } j = 1, \ldots, 7
\]
\[
N \geq 0 \quad \text{and integer}
\]

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extraction
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
p = data['Period']
demand = data['Demand']

#### Problem definition
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Variables
x = {j: pulp.LpVariable(f"x_{j}", lowBound=0, cat='Integer') for j in range(T)}
N = pulp.LpVariable("N", lowBound=0, cat='Integer')

#### Objective function
problem += pulp.lpSum(x[j] for j in range(T)), "Minimize Total Nurses"

#### Constraints
for k in range(T):
    problem += pulp.lpSum(x[(j % T)] for j in range(k, k + p)) >= demand[k], f"Demand_Constraint_day_{k+1}"

#### Solve the problem
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


