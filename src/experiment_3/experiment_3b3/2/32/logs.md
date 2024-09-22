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

\title{Linear Programming Model for Product Production}
\author{}
\date{}
\maketitle

\section*{Problem Definition}

We are tasked with determining the optimal quantities of products to produce in order to maximize profit while satisfying production constraints across different stages.

\section*{Parameters}

Let:
\begin{itemize}
    \item \( K \): Number of products
    \item \( S \): Number of stages
    \item \( \text{produce\_time}_{k,s} \): Time required to produce 1 unit of product \( k \) at stage \( s \) (in hours)
    \item \( \text{time}_{s} \): Total available time for stage \( s \) (in hours)
    \item \( \text{profit}_{k} \): Profit per unit of product \( k \)
    \item \( x_{k} \): Quantity of product \( k \) to be produced
\end{itemize}

\section*{Objective Function}

We aim to maximize the total profit given by:

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_{k}
\]

\section*{Constraints}

For each stage \( s \) (where \( s = 1, 2, \ldots, S \)), we have the following constraints based on the available time:

\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_{k} \leq \text{time}_{s}, \quad \forall s = 1, 2, \ldots, S
\]

Additionally, we include non-negativity constraints:

\[
x_{k} \geq 0, \quad \forall k = 1, 2, \ldots, K
\]

\section*{Complete Model}

Putting it all together, the linear programming model can be stated as follows:

\begin{align*}
\text{Maximize} & \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_{k} \\
\text{subject to} & \quad \sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_{k} \leq \text{time}_{s}, \quad \forall s = 1, 2, \ldots, S \\
& \quad x_{k} \geq 0, \quad \forall k = 1, 2, \ldots, K
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

\title{Linear Programming Model for Product Production}
\author{}
\date{}
\maketitle

\section*{Problem Definition}

We are tasked with determining the optimal quantities of products to produce in order to maximize profit while satisfying production constraints across different stages.

\section*{Parameters}

Let:
\begin{itemize}
    \item \( K \): Number of products
    \item \( S \): Number of stages
    \item \( \text{produce\_time}_{k,s} \): Time required to produce 1 unit of product \( k \) at stage \( s \) (in hours)
    \item \( \text{time}_{s} \): Total available time for stage \( s \) (in hours)
    \item \( \text{profit}_{k} \): Profit per unit of product \( k \)
    \item \( x_{k} \): Quantity of product \( k \) to be produced
\end{itemize}

\section*{Objective Function}

We aim to maximize the total profit given by:

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_{k}
\]

\section*{Constraints}

For each stage \( s \) (where \( s = 1, 2, \ldots, S \)), we have the following constraints based on the available time:

\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_{k} \leq \text{time}_{s}, \quad \forall s = 1, 2, \ldots, S
\]

Additionally, we include non-negativity constraints:

\[
x_{k} \geq 0, \quad \forall k = 1, 2, \ldots, K
\]

\section*{Complete Model}

Putting it all together, the linear programming model can be stated as follows:

\begin{align*}
\text{Maximize} & \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_{k} \\
\text{subject to} & \quad \sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_{k} \leq \text{time}_{s}, \quad \forall s = 1, 2, \ldots, S \\
& \quad x_{k} \geq 0, \quad \forall k = 1, 2, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x_vars = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

#### Objective function
problem += pulp.lpSum(data['Profit'][k] * x_vars[k] for k in range(data['NumProducts']))

#### Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * x_vars[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][s]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

