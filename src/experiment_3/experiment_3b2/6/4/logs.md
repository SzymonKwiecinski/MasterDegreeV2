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
To formulate the given problem as a Mixed Integer Linear Programming (MILP) model, we need to define decision variables, constraints, and the objective function. Below is the formulation in LaTeX.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MILP Formulation for Nurse Scheduling Problem}

\subsection*{Indices}
\begin{itemize}
    \item $j \in \{1, 2, \ldots, 7\}$: Day of the week
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $d_j$: Demand for nurses on day $j$ during the night shift
    \item \text{period}: Number of consecutive days a nurse works followed by $(7 - \text{period})$ days off
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_j$: Number of nurses who start their shift period on day $j$, $x_j \in \mathbb{Z}_{\geq 0}$ for $j = 1, 2, \ldots, 7$
    \item $N$: Total number of nurses hired
\end{itemize}

\subsection*{Objective}
Minimize the total number of nurses hired:
\[
\min N
\]

\subsection*{Constraints}
\begin{itemize}
    \item Link the total number of nurses with the starting schedule:
    \[
    N = \sum_{j=1}^{7} x_j
    \]
    \item Meet the demand on each day:
    \[
    \sum_{k=0}^{\text{period} - 1} x_{(j-k-1) \mod 7 + 1} \geq d_j, \quad \text{for } j = 1, 2, \ldots, 7
    \]
    The expression $(j-k-1) \mod 7 + 1$ is used to handle cyclic indexing for days.
\end{itemize}

\subsection*{Explanation}
Each nurse works for a continuous period of "period" days and is off for the remaining days of the week. The constraint ensures that for each day, the cumulative number of nurses who start within the last "period" days meets the demand for that day. The objective function seeks to minimize the total number of nurses hired, which corresponds to minimizing the sum of nurses starting their period on each day.

\end{document}
```

This formulation incorporates all necessary constraints and the objective to solve the problem optimally. The decision variables and constraints are set up to ensure the demand is met and the total number of nurses is minimized.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MILP Formulation for Nurse Scheduling Problem}

\subsection*{Indices}
\begin{itemize}
    \item $j \in \{1, 2, \ldots, 7\}$: Day of the week
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $d_j$: Demand for nurses on day $j$ during the night shift
    \item \text{period}: Number of consecutive days a nurse works followed by $(7 - \text{period})$ days off
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_j$: Number of nurses who start their shift period on day $j$, $x_j \in \mathbb{Z}_{\geq 0}$ for $j = 1, 2, \ldots, 7$
    \item $N$: Total number of nurses hired
\end{itemize}

\subsection*{Objective}
Minimize the total number of nurses hired:
\[
\min N
\]

\subsection*{Constraints}
\begin{itemize}
    \item Link the total number of nurses with the starting schedule:
    \[
    N = \sum_{j=1}^{7} x_j
    \]
    \item Meet the demand on each day:
    \[
    \sum_{k=0}^{\text{period} - 1} x_{(j-k-1) \mod 7 + 1} \geq d_j, \quad \text{for } j = 1, 2, \ldots, 7
    \]
    The expression $(j-k-1) \mod 7 + 1$ is used to handle cyclic indexing for days.
\end{itemize}

\subsection*{Explanation}
Each nurse works for a continuous period of "period" days and is off for the remaining days of the week. The constraint ensures that for each day, the cumulative number of nurses who start within the last "period" days meets the demand for that day. The objective function seeks to minimize the total number of nurses hired, which corresponds to minimizing the sum of nurses starting their period on each day.

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
Period = data['Period']
Demand = data['Demand']

#### Initialize the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0, cat='Integer')  #### Number of nurses starting on each day
N = pulp.LpVariable("N", lowBound=0, cat='Integer')  #### Total number of nurses hired

#### Objective Function
problem += N, "Total_Nurses_Hired"

#### Constraints
#### Total number of nurses is the sum of nurses starting on each day
problem += N == pulp.lpSum(x[j] for j in range(1, T + 1)), "Total_Nurses"

#### Demand constraints for each day
for j in range(1, T + 1):
    problem += pulp.lpSum(x[(j - k - 1) % T + 1] for k in range(Period)) >= Demand[j - 1], f"Demand_Constraint_{j}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

