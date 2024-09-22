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
To solve this linear programming (LP) problem, we need to maximize the total profit while satisfying production constraints at each stage. The problem can be formulated as follows:

Let's define:
- \( K \): Number of products.
- \( S \): Number of stages.

Given:
- \( \text{produce\_time}_{k,s} \): Time required to produce one unit of product \( k \) at stage \( s \).
- \( \text{time}_{s} \): Available working time at stage \( s \).
- \( \text{profit}_{k} \): Profit from one unit of product \( k \).

Decision Variable:
- \( \text{quantity}_{k} \): Number of units to produce for product \( k \).

Objective Function:
\[ \text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k} \]

Subject to Constraints:
1. Stage constraints to ensure that the production time does not exceed the available time at each stage:
   \[
   \sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot \text{quantity}_{k} \leq \text{time}_{s} \quad \text{for each } s = 1, \ldots, S
   \]
2. Non-negativity constraints:
   \[
   \text{quantity}_{k} \geq 0 \quad \text{for each } k = 1, \ldots, K
   \]

Now, here is the formulation of this LP problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( K \): Set of products, indexed by \( k \).
    \item \( S \): Set of production stages, indexed by \( s \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \(\text{produce\_time}_{k,s}\): Time to produce one unit of product \( k \) at stage \( s \).
    \item \(\text{time}_{s}\): Available working time at stage \( s \).
    \item \(\text{profit}_{k}\): Profit for one unit of product \( k \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \(\text{quantity}_{k}\): Number of units to produce for product \( k \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Production time constraints at each stage:
    \[
    \sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot \text{quantity}_{k} \leq \text{time}_{s} \quad \forall s \in S
    \]
    \item Non-negativity constraints:
    \[
    \text{quantity}_{k} \geq 0 \quad \forall k \in K
    \]
\end{itemize}

\end{document}
```

This LaTeX code describes the LP problem which maximizes the total profit subject to constraints on the production stages and the non-negativity of the decision variables. Adjust the sets \( K \) and \( S \) according to the specific problem data when implementing the solution.

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

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( K \): Set of products, indexed by \( k \).
    \item \( S \): Set of production stages, indexed by \( s \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \(\text{produce\_time}_{k,s}\): Time to produce one unit of product \( k \) at stage \( s \).
    \item \(\text{time}_{s}\): Available working time at stage \( s \).
    \item \(\text{profit}_{k}\): Profit for one unit of product \( k \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \(\text{quantity}_{k}\): Number of units to produce for product \( k \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Production time constraints at each stage:
    \[
    \sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot \text{quantity}_{k} \leq \text{time}_{s} \quad \forall s \in S
    \]
    \item Non-negativity constraints:
    \[
    \text{quantity}_{k} \geq 0 \quad \forall k \in K
    \]
\end{itemize}

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

#### Sets
K = range(data['NumProducts'])
S = range(data['NumMachines'])

#### Parameters
produce_time = data['ProduceTime']
time = data['AvailableTime']
profit = data['Profit']

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
quantity = pulp.LpVariable.dicts("Quantity", K, lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in K), "Total Profit"

#### Constraints
for s in S:
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in K) <= time[s], f"Time_Constraint_Stage_{s}"

#### Solve
problem.solve()

#### Output the objective
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

