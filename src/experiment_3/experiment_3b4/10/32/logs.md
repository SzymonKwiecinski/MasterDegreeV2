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
To solve this problem, we need to formulate a Linear Programming (LP) model that maximizes the profit while satisfying the constraints on production time at each stage. Here's the mathematical model for the given problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Given:}
\begin{itemize}
    \item Let $K$ denote the number of different products.
    \item Let $S$ denote the number of production stages.
    \item Let $produce\_time_{k, s}$ be the time required to produce one unit of product $k$ at stage $s$.
    \item Let $time_{s}$ be the available production time at stage $s$.
    \item Let $profit_{k}$ be the profit for producing one unit of product $k$.
\end{itemize}

\subsection*{Decision Variables:}
\begin{itemize}
    \item Let $quantity_{k}$ be the number of units to produce for product $k$, where $k = 1, \ldots, K$.
\end{itemize}

\subsection*{Objective Function:}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_{k} \times quantity_{k}
\]

\subsection*{Constraints:}
1. For each stage $s = 1, \ldots, S$, the total production time used must not exceed the available time:
\[
\sum_{k=1}^{K} produce\_time_{k, s} \times quantity_{k} \leq time_{s}
\]

2. Non-negativity constraint:
\[
quantity_{k} \geq 0 \quad \text{for all } k = 1, \ldots, K
\]

\end{document}
```

This model captures both the objective of maximizing profits and the constraints on production time availability for each production stage. Each product \(k\) has a profit \(profit_k\), and the decision variable \(quantity_k\) represents the amount of product \(k\) to produce. The LP constraints ensure that the sum of production times for each stage does not exceed the available time.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Given:}
\begin{itemize}
    \item Let $K$ denote the number of different products.
    \item Let $S$ denote the number of production stages.
    \item Let $produce\_time_{k, s}$ be the time required to produce one unit of product $k$ at stage $s$.
    \item Let $time_{s}$ be the available production time at stage $s$.
    \item Let $profit_{k}$ be the profit for producing one unit of product $k$.
\end{itemize}

\subsection*{Decision Variables:}
\begin{itemize}
    \item Let $quantity_{k}$ be the number of units to produce for product $k$, where $k = 1, \ldots, K$.
\end{itemize}

\subsection*{Objective Function:}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_{k} \times quantity_{k}
\]

\subsection*{Constraints:}
1. For each stage $s = 1, \ldots, S$, the total production time used must not exceed the available time:
\[
\sum_{k=1}^{K} produce\_time_{k, s} \times quantity_{k} \leq time_{s}
\]

2. Non-negativity constraint:
\[
quantity_{k} \geq 0 \quad \text{for all } k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extracting and defining the data from the JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

K = data['NumProducts']  #### Number of products
S = data['NumMachines']  #### Number of stages

produce_time = data['ProduceTime']  #### Time required to produce one unit of product at each stage
time_available = data['AvailableTime']  #### Available production time at each stage
profit = data['Profit']  #### Profit for producing one unit of each product

#### Creating a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Defining decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Defining the objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

#### Defining constraints for each production stage
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= time_available[s], f"Time_Constraint_Stage_{s}"

#### Solving the problem
problem.solve()

#### Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

