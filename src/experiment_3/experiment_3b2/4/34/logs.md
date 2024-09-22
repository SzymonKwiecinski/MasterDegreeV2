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
To model this Linear Programming problem, we will define the objective function and constraints based on the provided inputs. The goal is to minimize the cost of purchasing foods while meeting the nutritional requirements.

Here's the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Diet Problem}

\subsection*{Sets and Indices}
\begin{itemize}
    \item $k = 1, \ldots, K$: Index for foods available at the market.
    \item $m = 1, \ldots, M$: Index for nutritional ingredients.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{price}_{k}$: Price per unit of food $k$.
    \item $\text{demand}_{m}$: Minimum required units of nutrient $m$ per day.
    \item $\text{nutri}_{k,m}$: Units of nutrient $m$ contained in one unit of food $k$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $\text{quantity}_{k}$: Quantity of food $k$ to purchase.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of purchasing foods:
\[
\min \sum_{k=1}^{K} \text{price}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Nutritional requirements:
    \[
    \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_{k} \geq \text{demand}_{m}, \quad \forall m = 1, \ldots, M
    \]
    \item Non-negativity:
    \[
    \text{quantity}_{k} \geq 0, \quad \forall k = 1, \ldots, K
    \]
\end{itemize}

\end{document}
```

This LaTeX code defines a Linear Programming model for the problem described. The objective is to minimize the total price of foods while satisfying the nutritional demands for each nutrient. The constraints ensure that the nutritional requirements are met, and the non-negativity constraints ensure that the quantities of food purchased are non-negative.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Diet Problem}

\subsection*{Sets and Indices}
\begin{itemize}
    \item $k = 1, \ldots, K$: Index for foods available at the market.
    \item $m = 1, \ldots, M$: Index for nutritional ingredients.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{price}_{k}$: Price per unit of food $k$.
    \item $\text{demand}_{m}$: Minimum required units of nutrient $m$ per day.
    \item $\text{nutri}_{k,m}$: Units of nutrient $m$ contained in one unit of food $k$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $\text{quantity}_{k}$: Quantity of food $k$ to purchase.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of purchasing foods:
\[
\min \sum_{k=1}^{K} \text{price}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Nutritional requirements:
    \[
    \sum_{k=1}^{K} \text{nutri}_{k,m} \cdot \text{quantity}_{k} \geq \text{demand}_{m}, \quad \forall m = 1, \ldots, M
    \]
    \item Non-negativity:
    \[
    \text{quantity}_{k} \geq 0, \quad \forall k = 1, \ldots, K
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data input
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

#### Indices
K = len(data['price'])  #### Number of foods
M = len(data['demand'])  #### Number of nutritional ingredients

#### Create the problem
problem = pulp.LpProblem("Diet_Problem", pulp.LpMinimize)

#### Decision Variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K)), "Total_Cost"

#### Nutritional Constraints
for m in range(M):
    problem += (
        pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m],
        f"Nutritional_Requirement_{m}"
    )

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

