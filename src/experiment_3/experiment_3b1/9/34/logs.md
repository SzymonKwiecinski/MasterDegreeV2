# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We assume that there are available at the market different foods and that the food \var{k} sells at a price \var{price_{k}} per unit. 
- In addition there are several basic nutritional ingredients and, to achieve a balanced diet, each individual must receive at least \var{demand_{m}} units of nutrient \var{m} per day. 
- Finally, we assume that each unit of food \var{k} contains \var{nutri_{k, m}} units of nutrition \var{m}

INPUT FORMAT:

{
	"price": [price_{k} for k in 1,...,K],
	"demand": [demand_{m} for m in 1,...,M],
	"nutrition": [[nutri_{k, m} for m in 1,...,M] for k in 1,...,K]
}


OBJECTIVE: We want to minimize the total prices of the foods to purchase.

OUTPUT INFO:

- \var{quantity} represents the quantity of each food to purchase

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

\title{Linear Programming Model for Nutritional Optimization}
\author{}
\date{}
\maketitle

\section*{Problem Description}
We aim to minimize the total cost of purchasing food while satisfying nutritional demands.

\subsection*{Inputs}
Let:
\begin{itemize}
    \item $K$ = number of different food types
    \item $M$ = number of nutritional ingredients
    \item $\text{price}_k$ = price per unit of food $k$ for $k = 1, \ldots, K$
    \item $\text{demand}_m$ = minimum required units of nutrient $m$ for $m = 1, \ldots, M$
    \item $\text{nutri}_{k,m}$ = units of nutrient $m$ contained in food $k$
\end{itemize}

\subsection*{Decision Variables}
Define $x_k$ as the quantity of food $k$ to purchase for $k = 1, \ldots, K$.

\subsection*{Objective Function}
The objective is to minimize the total cost:
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\subsection*{Constraints}
To ensure that each nutrient demand is met, we have the following constraints:
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M
\]

Additionally, we include non-negativity constraints on the decision variables:
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\subsection*{Output}
\begin{itemize}
    \item The solution will provide the quantities of each food to purchase, represented as:
    \[
    \text{quantity} = [x_1, x_2, \ldots, x_K]
    \]
\end{itemize}

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

\title{Linear Programming Model for Nutritional Optimization}
\author{}
\date{}
\maketitle

\section*{Problem Description}
We aim to minimize the total cost of purchasing food while satisfying nutritional demands.

\subsection*{Inputs}
Let:
\begin{itemize}
    \item $K$ = number of different food types
    \item $M$ = number of nutritional ingredients
    \item $\text{price}_k$ = price per unit of food $k$ for $k = 1, \ldots, K$
    \item $\text{demand}_m$ = minimum required units of nutrient $m$ for $m = 1, \ldots, M$
    \item $\text{nutri}_{k,m}$ = units of nutrient $m$ contained in food $k$
\end{itemize}

\subsection*{Decision Variables}
Define $x_k$ as the quantity of food $k$ to purchase for $k = 1, \ldots, K$.

\subsection*{Objective Function}
The objective is to minimize the total cost:
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\subsection*{Constraints}
To ensure that each nutrient demand is met, we have the following constraints:
\[
\sum_{k=1}^{K} \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M
\]

Additionally, we include non-negativity constraints on the decision variables:
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\subsection*{Output}
\begin{itemize}
    \item The solution will provide the quantities of each food to purchase, represented as:
    \[
    \text{quantity} = [x_1, x_2, \ldots, x_K]
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

#### Extracting the data
K = len(data['price'])  #### Number of food types
M = len(data['demand'])  #### Number of nutritional ingredients
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

#### Creating the LP problem
problem = pulp.LpProblem("Nutritional_Optimization", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("food_quantity", range(K), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints for nutritional demands
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demands[m], f"Nutrient_Constraint_{m+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

