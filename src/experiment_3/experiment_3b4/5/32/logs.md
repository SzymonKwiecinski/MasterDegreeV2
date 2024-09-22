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
To solve this linear programming problem, we need to maximize the profit from the production of various products, subject to constraints on the available production time at each stage. Here's how we can formulate the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

Let:
\begin{itemize}
    \item \( K \) be the number of products,
    \item \( S \) be the number of stages,
    \item \( \text{produce\_time}_{k,s} \) be the time required to produce one unit of product \( k \) at stage \( s \),
    \item \( \text{time}_{s} \) be the available working hours at stage \( s \),
    \item \( \text{profit}_{k} \) be the profit for product \( k \),
    \item \( \text{quantity}_{k} \) be the quantity of product \( k \) to be produced.
\end{itemize}

The objective is to maximize the total profit:
\[
\text{Maximize } \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

Subject to the constraints:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \times \text{quantity}_{k} \leq \text{time}_{s} \quad \forall s \in \{1, 2, \ldots, S\}
\]

And the non-negativity constraints:
\[
\text{quantity}_{k} \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]

\end{document}
```

The above model seeks to determine the optimal production quantities \(\text{quantity}_{k}\) for each product \(k\) such that the available time at each stage is not exceeded, and the total profit is maximized.

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

Let:
\begin{itemize}
    \item \( K \) be the number of products,
    \item \( S \) be the number of stages,
    \item \( \text{produce\_time}_{k,s} \) be the time required to produce one unit of product \( k \) at stage \( s \),
    \item \( \text{time}_{s} \) be the available working hours at stage \( s \),
    \item \( \text{profit}_{k} \) be the profit for product \( k \),
    \item \( \text{quantity}_{k} \) be the quantity of product \( k \) to be produced.
\end{itemize}

The objective is to maximize the total profit:
\[
\text{Maximize } \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

Subject to the constraints:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \times \text{quantity}_{k} \leq \text{time}_{s} \quad \forall s \in \{1, 2, \ldots, S\}
\]

And the non-negativity constraints:
\[
\text{quantity}_{k} \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]

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

#### Number of products and machines
K = data['NumProducts']
S = data['NumMachines']

#### Unpack data
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
quantity_vars = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(profit[k] * quantity_vars[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * quantity_vars[k] for k in range(K)) <= available_time[s], f"Stage_{s}_Time_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

