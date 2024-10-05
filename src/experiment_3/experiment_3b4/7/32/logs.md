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
To construct a Linear Programming (LP) model for the given problem, we define variables and constraints based on the description. Below is the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_k \) be the production quantity of product \( k \), for \( k = 1, \ldots, K \).
\end{itemize}

\textbf{Objective Function:}
Maximize the total profit, given by:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\textbf{Subject to the following constraints:}

1. Stage time constraints:
   For each stage \( s = 1, \ldots, S \), ensure the total production time does not exceed the available time:
   \[
   \sum_{k=1}^{K} \text{produce\_time}_{k, s} \cdot x_k \leq \text{time}_s
   \]

2. Non-negativity constraints:
   \[
   x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
   \]

\textbf{Input Parameters:}
\begin{itemize}
    \item \(\text{produce\_time}_{k, s}\) represents the necessary time in hours to produce one unit of product \( k \) at stage \( s \).
    \item \(\text{time}_s\) denotes the available working hours for stage \( s \).
    \item \(\text{profit}_k\) is the unitary profit for product \( k \).
\end{itemize}

\end{document}
```

This LaTeX code represents the mathematical model for the problem where we are maximizing the profit by determining the production quantities of different products while respecting production time constraints at each stage. The constraints ensure that the production does not exceed available hours at each stage. The decision variables \( x_k \) are the quantities of each product to be produced.

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

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_k \) be the production quantity of product \( k \), for \( k = 1, \ldots, K \).
\end{itemize}

\textbf{Objective Function:}
Maximize the total profit, given by:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\textbf{Subject to the following constraints:}

1. Stage time constraints:
   For each stage \( s = 1, \ldots, S \), ensure the total production time does not exceed the available time:
   \[
   \sum_{k=1}^{K} \text{produce\_time}_{k, s} \cdot x_k \leq \text{time}_s
   \]

2. Non-negativity constraints:
   \[
   x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
   \]

\textbf{Input Parameters:}
\begin{itemize}
    \item \(\text{produce\_time}_{k, s}\) represents the necessary time in hours to produce one unit of product \( k \) at stage \( s \).
    \item \(\text{time}_s\) denotes the available working hours for stage \( s \).
    \item \(\text{profit}_k\) is the unitary profit for product \( k \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') 
     for k in range(data['NumProducts'])]

#### Objective Function
problem += pulp.lpSum(data['Profit'][k] * x[k] 
                      for k in range(data['NumProducts']))

#### Constraints
#### Stage time constraints
for s in range(data['NumMachines']):
    problem += (pulp.lpSum(data['ProduceTime'][k][s] * x[k] 
                           for k in range(data['NumProducts'])) <= data['AvailableTime'][s])

#### Solve the problem
problem.solve()

#### Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

