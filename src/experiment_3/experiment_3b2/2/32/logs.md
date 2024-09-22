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
To formulate the given problem as a Linear Programming (LP) problem, we will define the variables, objective function, and constraints based on the provided information.

**Variables:**
- Let \( x_k \) be the decision variable representing the production quantity of product \( k \), where \( k = 1, \ldots, K \).

**Objective Function:**
- We aim to maximize the total profit, given by the sum of the profits from all products:
  \[
  \text{Maximize } Z = \sum_{k=1}^{K} (\text{profit}_k \times x_k)
  \]

**Constraints:**
- For each production stage \( s \), the total time required to produce the products must not exceed the available time:
  \[
  \sum_{k=1}^{K} (\text{produce\_time}_{k,s} \times x_k) \leq \text{time}_s, \quad \forall s = 1, \ldots, S
  \]

- Additionally, the production quantity for each product should be non-negative:
  \[
  x_k \geq 0, \quad \forall k = 1, \ldots, K
  \]

Below is the corresponding LaTeX code encapsulating this LP formulation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Maximizing Profit}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_k \) : production quantity of product \( k \), for \( k = 1, \ldots, K \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
Z = \sum_{k=1}^{K} \left( \text{profit}_{k} \times x_k \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Time constraints for each stage \( s \):
    \[
    \sum_{k=1}^{K} \left( \text{produce\_time}_{k,s} \times x_k \right) \leq \text{time}_{s}, \quad \forall s = 1, \ldots, S
    \]
    \item Non-negativity constraints:
    \[
    x_k \geq 0, \quad \forall k = 1, \ldots, K
    \]
\end{itemize}

\end{document}
```

This LaTeX document defines the mathematical model that represents the described problem, optimizing production quantities while considering the constraints on available processing time.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Maximizing Profit}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_k \) : production quantity of product \( k \), for \( k = 1, \ldots, K \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
Z = \sum_{k=1}^{K} \left( \text{profit}_{k} \times x_k \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Time constraints for each stage \( s \):
    \[
    \sum_{k=1}^{K} \left( \text{produce\_time}_{k,s} \times x_k \right) \leq \text{time}_{s}, \quad \forall s = 1, \ldots, S
    \]
    \item Non-negativity constraints:
    \[
    x_k \geq 0, \quad \forall k = 1, \ldots, K
    \]
\end{itemize}

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

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("production_quantity", range(data['NumProducts']), lowBound=0)  #### x_k >= 0

#### Objective Function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumProducts'])), "Total_Profit"

#### Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * x[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][s], f"Time_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

