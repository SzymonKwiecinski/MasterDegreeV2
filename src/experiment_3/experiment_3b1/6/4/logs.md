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

\section*{Mathematical Model for Nursing Shift Scheduling}

\subsection*{Parameters}
\begin{itemize}
    \item $period$: Number of consecutive days a nurse works the night shift.
    \item $d_j$: Demand for nurses on day $j$ for $j = 1, \ldots, 7$.
    \item $N$: Total number of nurses hired.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $start_j$: Number of nurses starting their shift on day $j$ for $j = 1, \ldots, 7$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of nurses hired:

\[
\text{Minimize } N = \sum_{j=1}^{7} start_j
\]

\subsection*{Constraints}
For each day $j$, the demand must be satisfied by the nurses starting their shifts that day and the ones from the previous $period - 1$ days:

\[
\sum_{i=0}^{\min(period-1, j-1)} start_{j-i} \geq d_j \quad \forall j \in \{1, 2, \ldots, 7\}
\]

This ensures that the number of nurses available on each day meets the required demand.

\subsection*{Output}
The model will output:
\begin{itemize}
    \item $start_j$ for each day $j = 1, \ldots, 7$.
    \item The total number of nurses hired $N$.
\end{itemize}

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

\section*{Mathematical Model for Nursing Shift Scheduling}

\subsection*{Parameters}
\begin{itemize}
    \item $period$: Number of consecutive days a nurse works the night shift.
    \item $d_j$: Demand for nurses on day $j$ for $j = 1, \ldots, 7$.
    \item $N$: Total number of nurses hired.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $start_j$: Number of nurses starting their shift on day $j$ for $j = 1, \ldots, 7$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of nurses hired:

\[
\text{Minimize } N = \sum_{j=1}^{7} start_j
\]

\subsection*{Constraints}
For each day $j$, the demand must be satisfied by the nurses starting their shifts that day and the ones from the previous $period - 1$ days:

\[
\sum_{i=0}^{\min(period-1, j-1)} start_{j-i} \geq d_j \quad \forall j \in \{1, 2, \ldots, 7\}
\]

This ensures that the number of nurses available on each day meets the required demand.

\subsection*{Output}
The model will output:
\begin{itemize}
    \item $start_j$ for each day $j = 1, \ldots, 7$.
    \item The total number of nurses hired $N$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input Data
data_json = '''{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}'''
data = json.loads(data_json.replace("'", "\""))

#### Parameters
T = data['T']  #### Number of days
period = data['Period']  #### Number of consecutive days for night shift
demand = data['Demand']  #### Demand for nurses for each day

#### Create the linear programming problem
problem = pulp.LpProblem("NursingShiftScheduling", pulp.LpMinimize)

#### Decision Variables
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')

#### Objective Function
problem += pulp.lpSum(start[j] for j in range(1, T + 1)), "TotalNursesHired"

#### Constraints
for j in range(1, T + 1):
    problem += (
        pulp.lpSum(start[max(1, j - k)] for k in range(0, min(period, j))) >= demand[j - 1],
        f"Demand_Satisfaction_Day_{j}"
    )

#### Solve the problem
problem.solve()

#### Output the results
for j in range(1, T + 1):
    print(f'Start_{j}: {start[j].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

