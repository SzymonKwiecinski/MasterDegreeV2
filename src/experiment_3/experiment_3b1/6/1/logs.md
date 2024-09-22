# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A firm produces \var{M} different goods using \var{N} different raw materials.
- The firm has \var{available_{i}} of raw material \var{i} available.
- Good \var{j} requires \var{req_{i,j}} units of material \var{i} per unit produced.
- Good \var{j} results in a revenue of \var{price_j} per unit produced.


INPUT FORMAT: 

{
    "available": [available_{i} for i in 1, ..., N]
    "requirements": [[req_{i,j} for i in 1, ..., N] for j in 1, ..., M],
    "prices": [price_{j} for j in 1, ..., M]
}

OBJECTIVE: How much of each good should the firm produce in order to maximize its total revenue?

OUTPUT INFO:

- the amount of each good produced \var{amount_{j}}.

OUTPUT FORMAT:

{
    "amount": [amount_{j} for j in 1, ..., M]
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Maximizing Revenue}
\author{}
\date{}
\maketitle

\section*{Problem Description}

A firm produces \( M \) different goods using \( N \) different raw materials. The firm has \( \text{available}_i \) of raw material \( i \) available. Good \( j \) requires \( \text{req}_{i,j} \) units of material \( i \) per unit produced. Good \( j \) results in a revenue of \( \text{price}_j \) per unit produced.

\section*{Input Format}

Let:
\begin{itemize}
    \item \( \text{available} = [\text{available}_1, \text{available}_2, \ldots, \text{available}_N] \)
    \item \( \text{requirements} = \left[ \left[ \text{req}_{1,j}, \text{req}_{2,j}, \ldots, \text{req}_{N,j} \right] \text{ for } j = 1, \ldots, M \right] \)
    \item \( \text{prices} = [\text{price}_1, \text{price}_2, \ldots, \text{price}_M] \)
\end{itemize}

\section*{Objective}

Maximize the total revenue, which can be mathematically formulated as follows:

\[
\text{Maximize } Z = \sum_{j=1}^{M} \text{price}_j \cdot \text{amount}_j
\]

\section*{Subject to}

The constraints based on the availability of raw materials can be expressed as:

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i \quad \forall i = 1, 2, \ldots, N
\]

\section*{Non-negativity Constraint}

Additionally, the production amounts must be non-negative:

\[
\text{amount}_j \geq 0 \quad \forall j = 1, 2, \ldots, M
\]

\section*{Output Format}

The solution to the optimization problem will yield the amount of each good to produce:

\[
\text{Output} = \{ \text{amount} : [\text{amount}_1, \text{amount}_2, \ldots, \text{amount}_M] \}
\]

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

\title{Linear Programming Model for Maximizing Revenue}
\author{}
\date{}
\maketitle

\section*{Problem Description}

A firm produces \( M \) different goods using \( N \) different raw materials. The firm has \( \text{available}_i \) of raw material \( i \) available. Good \( j \) requires \( \text{req}_{i,j} \) units of material \( i \) per unit produced. Good \( j \) results in a revenue of \( \text{price}_j \) per unit produced.

\section*{Input Format}

Let:
\begin{itemize}
    \item \( \text{available} = [\text{available}_1, \text{available}_2, \ldots, \text{available}_N] \)
    \item \( \text{requirements} = \left[ \left[ \text{req}_{1,j}, \text{req}_{2,j}, \ldots, \text{req}_{N,j} \right] \text{ for } j = 1, \ldots, M \right] \)
    \item \( \text{prices} = [\text{price}_1, \text{price}_2, \ldots, \text{price}_M] \)
\end{itemize}

\section*{Objective}

Maximize the total revenue, which can be mathematically formulated as follows:

\[
\text{Maximize } Z = \sum_{j=1}^{M} \text{price}_j \cdot \text{amount}_j
\]

\section*{Subject to}

The constraints based on the availability of raw materials can be expressed as:

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i \quad \forall i = 1, 2, \ldots, N
\]

\section*{Non-negativity Constraint}

Additionally, the production amounts must be non-negative:

\[
\text{amount}_j \geq 0 \quad \forall j = 1, 2, \ldots, M
\]

\section*{Output Format}

The solution to the optimization problem will yield the amount of each good to produce:

\[
\text{Output} = \{ \text{amount} : [\text{amount}_1, \text{amount}_2, \ldots, \text{amount}_M] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = json.loads('{"M": 4, "N": 5, "Available": [10, 20, 15, 35, 25], "Requirements": [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], "Prices": [7, 10, 5, 9]}')

M = data['M']  #### Number of goods
N = data['N']  #### Number of raw materials
available = data['Available']  #### Available amounts of raw materials
requirements = data['Requirements']  #### Requirements of each good
prices = data['Prices']  #### Prices of each good

#### Create the problem variable
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

#### Decision variables for the amount of each good to produce
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

#### Objective function
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M)), "Total_Revenue"

#### Constraints based on available raw materials
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i], f"Material_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Print the results
amounts_output = [amounts[j].varValue for j in range(M)]
print(f'Output: {{"amount": {amounts_output}}}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

