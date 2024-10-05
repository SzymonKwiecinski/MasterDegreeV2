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
To model this linear programming problem in LaTeX, we need to define decision variables, an objective function, and a set of constraints based on the provided problem information.

Let's assume you have:
- \( K \) products
- \( S \) stages

The decision variables \( x_k \) represent the quantity of product \( k \) to be produced.

The objective function is to maximize the total profit, which can be expressed as:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\]

The constraints ensure that the total production time for each stage does not exceed the available working hours. This can be represented by:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k, s} \times x_k \leq \text{time}_{s} \quad \text{for each stage } s = 1, \ldots, S
\]

Additionally, the decision variables must be non-negative:
\[
x_k \geq 0 \quad \text{for each product } k = 1, \ldots, K
\]

Here is the corresponding LaTeX code for this linear programming model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}
\[
x_k \quad \text{for } k = 1, \ldots, K
\]

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\]

\textbf{Constraints:}
\[
\sum_{k=1}^{K} \text{produce\_time}_{k, s} \times x_k \leq \text{time}_{s} \quad \text{for each stage } s = 1, \ldots, S
\]

\textbf{Non-negativity Constraints:}
\[
x_k \geq 0 \quad \text{for each product } k = 1, \ldots, K
\]

\end{document}
```

This LaTeX code formulates a general linear programming model to solve the given problem, considering the production constraints and maximizing the total profit from the products.

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
\[
x_k \quad \text{for } k = 1, \ldots, K
\]

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\]

\textbf{Constraints:}
\[
\sum_{k=1}^{K} \text{produce\_time}_{k, s} \times x_k \leq \text{time}_{s} \quad \text{for each stage } s = 1, \ldots, S
\]

\textbf{Non-negativity Constraints:}
\[
x_k \geq 0 \quad \text{for each product } k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"NumProducts": 2, "NumMachines": 2, "ProduceTime": [[1, 3], [2, 1]], "AvailableTime": [200, 100], "Profit": [20, 10]}')

#### Extract data from JSON
K = data['NumProducts']
S = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += (pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s]), f"Time_Constraint_stage_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

