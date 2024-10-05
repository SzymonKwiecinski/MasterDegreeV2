# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We suppose that some products can be produced, each of them passing through several stages.
- Necessary time to produce 1 unit of product \var{k} is \var{produce_time_{k, s}} hours for stage \var{s}.
- Availability in working hours is \var{time_{s}} for stage \var{s}. 
- The unitary profits for product \var{k} is \var{profit_{k}}.

INPUT FORMAT:

{
	"produce_time": [[produce_time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"available_time": [time_{s} for s in 1,...,S],
	"profit": [profit_{k} for k in 1,...,K]
}


OBJECTIVE: Determine the quantities to be produced such that all the production constraints are satisfied and the profit is maximized.

OUTPUT INFO:

- \var{quantity} represents the production quantity for each product

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Indices:}
\begin{itemize}
    \item $k$: Index for products ($k = 1, \ldots, K$)
    \item $s$: Index for stages ($s = 1, \ldots, S$)
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $produce\_time_{k, s}$: Time required to produce one unit of product $k$ at stage $s$ (hours)
    \item $time_{s}$: Available working hours at stage $s$
    \item $profit_{k}$: Unit profit for product $k$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $quantity_{k}$: Quantity of product $k$ to produce
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
\text{Maximize } Z = \sum_{k=1}^{K} profit_{k} \cdot quantity_{k}
\end{equation}

\textbf{Constraints:}
\begin{equation}
\sum_{k=1}^{K} produce\_time_{k, s} \cdot quantity_{k} \leq time_{s}, \quad \forall s = 1, \ldots, S
\end{equation}

\textbf{Non-negativity Constraints:}
\begin{equation}
quantity_{k} \geq 0, \quad \forall k = 1, \ldots, K
\end{equation}

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

\section*{Linear Programming Model}

\textbf{Indices:}
\begin{itemize}
    \item $k$: Index for products ($k = 1, \ldots, K$)
    \item $s$: Index for stages ($s = 1, \ldots, S$)
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $produce\_time_{k, s}$: Time required to produce one unit of product $k$ at stage $s$ (hours)
    \item $time_{s}$: Available working hours at stage $s$
    \item $profit_{k}$: Unit profit for product $k$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $quantity_{k}$: Quantity of product $k$ to produce
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
\text{Maximize } Z = \sum_{k=1}^{K} profit_{k} \cdot quantity_{k}
\end{equation}

\textbf{Constraints:}
\begin{equation}
\sum_{k=1}^{K} produce\_time_{k, s} \cdot quantity_{k} \leq time_{s}, \quad \forall s = 1, \ldots, S
\end{equation}

\textbf{Non-negativity Constraints:}
\begin{equation}
quantity_{k} \geq 0, \quad \forall k = 1, \ldots, K
\end{equation}

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Create decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

#### Objective function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in range(data['NumProducts']))

#### Constraints for each stage (machine)
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * quantity[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][s]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


