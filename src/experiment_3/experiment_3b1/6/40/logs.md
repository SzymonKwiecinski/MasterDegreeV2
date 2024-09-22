# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A foundry receives a specific order for \var{n_steel_quant} tons of steel. 
- This steel must meet the following characteristics: it must contain at least \var{mn_percent} percentage of manganese (Mn) while its percentage of silicon (SI) must be between \var{si_min} and \var{si_max}.
- To cast this steel, the foundry has limited quantities of several types of minerals.
- The contents expressed in percentage per mineral \var{k} are \var{contsi_{k}} for Si and \var{contmn_{k}} for Mn.
- The process for producing steel is such that direct addition of Mn is possible.
- This Manganese is available at a price of \var{mang_price} million euros per ton. 
- As for the minerals, it costs \var{cost_{k}} million euros per thousand tons for mineral \var{k}.
- The foundry plans to sell the steel produced at \var{sell_price} million euros per ton.
- The cost of smelting a ton of mineral is \var{melt_price} million euros.

INPUT FORMAT:

{
	"n_steel_quant": n_steel_quant,
	"mn_percent": mn_percent,
	"si_min": si_min,
	"si_max": si_max,
	"contsi": [contsi_{k} for k in 1,...,K]
	"contmn": [contmn_{k} for k in 1,...,K]
	"mang_price": mang_price,
	"cost": [cost_{k} for k in 1,...,K]
	"sell_price": sell_price,
	"melt_price": melt_price
}

OBJECTIVE: How should the manufacture manage the steel to maximize profit?

OUTPUT INFO:

- \var{amount} represents the amount of each mineral melted
- \var{num_mang} represents the amount of Manganese directly added

OUTPUT FORMAT:

{
	"amount": [amount_{k} for k in 1,...,K]
	"num_mang": [num_mang]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Inputs:}
\begin{itemize}
    \item \( n_{\text{steel\_quant}} \): tons of steel required
    \item \( mn_{\text{percent}} \): minimum percentage of manganese in the steel
    \item \( si_{\text{min}} \): minimum percentage of silicon in the steel
    \item \( si_{\text{max}} \): maximum percentage of silicon in the steel
    \item \( \text{contsi}_k \): percentage of silicon in mineral \( k \)
    \item \( \text{contmn}_k \): percentage of manganese in mineral \( k \)
    \item \( mang_{\text{price}} \): price of manganese (in million euros per ton)
    \item \( \text{cost}_k \): cost of mineral \( k \) (in million euros per thousand tons)
    \item \( sell_{\text{price}} \): selling price of steel (in million euros per ton)
    \item \( melt_{\text{price}} \): melting cost of a ton of mineral (in million euros)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( \text{amount}_k \): amount of mineral \( k \) melted (in tons)
    \item \( num_{\text{mang}} \): amount of manganese added directly (in tons)
\end{itemize}

\textbf{Objective Function:}
Maximize profit:
\[
\text{Profit} = n_{\text{steel\_quant}} \times sell_{\text{price}} - \sum_{k=1}^{K} \left( \frac{\text{cost}_k}{1000} \times \text{amount}_k + melt_{\text{price}} \times \text{amount}_k \right) - mang_{\text{price}} \times num_{\text{mang}}
\]

\textbf{Constraints:}
1. Manganese content constraint:
\[
\sum_{k=1}^{K} \left( \frac{\text{amount}_k \times \text{contmn}_k}{100} \right) + num_{\text{mang}} \geq \frac{mn_{\text{percent}}}{100} \times n_{\text{steel\_quant}}
\]

2. Silicon content constraints:
\[
si_{\text{min}} \leq \frac{\sum_{k=1}^{K} \left( \frac{\text{amount}_k \times \text{contsi}_k}{100} \right)}{n_{\text{steel\_quant}}} \leq si_{\text{max}}
\]

3. Non-negativity constraints:
\[
\text{amount}_k \geq 0, \quad num_{\text{mang}} \geq 0 \quad \forall k
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

\section*{Linear Programming Model}

\textbf{Inputs:}
\begin{itemize}
    \item \( n_{\text{steel\_quant}} \): tons of steel required
    \item \( mn_{\text{percent}} \): minimum percentage of manganese in the steel
    \item \( si_{\text{min}} \): minimum percentage of silicon in the steel
    \item \( si_{\text{max}} \): maximum percentage of silicon in the steel
    \item \( \text{contsi}_k \): percentage of silicon in mineral \( k \)
    \item \( \text{contmn}_k \): percentage of manganese in mineral \( k \)
    \item \( mang_{\text{price}} \): price of manganese (in million euros per ton)
    \item \( \text{cost}_k \): cost of mineral \( k \) (in million euros per thousand tons)
    \item \( sell_{\text{price}} \): selling price of steel (in million euros per ton)
    \item \( melt_{\text{price}} \): melting cost of a ton of mineral (in million euros)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( \text{amount}_k \): amount of mineral \( k \) melted (in tons)
    \item \( num_{\text{mang}} \): amount of manganese added directly (in tons)
\end{itemize}

\textbf{Objective Function:}
Maximize profit:
\[
\text{Profit} = n_{\text{steel\_quant}} \times sell_{\text{price}} - \sum_{k=1}^{K} \left( \frac{\text{cost}_k}{1000} \times \text{amount}_k + melt_{\text{price}} \times \text{amount}_k \right) - mang_{\text{price}} \times num_{\text{mang}}
\]

\textbf{Constraints:}
1. Manganese content constraint:
\[
\sum_{k=1}^{K} \left( \frac{\text{amount}_k \times \text{contmn}_k}{100} \right) + num_{\text{mang}} \geq \frac{mn_{\text{percent}}}{100} \times n_{\text{steel\_quant}}
\]

2. Silicon content constraints:
\[
si_{\text{min}} \leq \frac{\sum_{k=1}^{K} \left( \frac{\text{amount}_k \times \text{contsi}_k}{100} \right)}{n_{\text{steel\_quant}}} \leq si_{\text{max}}
\]

3. Non-negativity constraints:
\[
\text{amount}_k \geq 0, \quad num_{\text{mang}} \geq 0 \quad \forall k
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'n_steel_quant': 1000, 
    'mn_percent': 0.45, 
    'si_min': 3.25, 
    'si_max': 5.0, 
    'contsi': [4.0, 1.0, 0.6], 
    'contmn': [0.45, 0.5, 0.4], 
    'mang_price': 8.0, 
    'cost': [21, 25, 15], 
    'sell_price': 0.45, 
    'melt_price': 0.005
}

#### Extracting values from the data for convenience
n_steel_quant = data['n_steel_quant']
mn_percent = data['mn_percent']
si_min = data['si_min']
si_max = data['si_max']
contsi = data['contsi']
contmn = data['contmn']
mang_price = data['mang_price']
cost = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']

#### Number of minerals
K = len(contsi)

#### Create the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

#### Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  #### amount_k
num_mang = pulp.LpVariable("num_mang", lowBound=0)  #### num_mang

#### Objective function
profit = n_steel_quant * sell_price - pulp.lpSum((cost[k] / 1000) * amount[k] + melt_price * amount[k] for k in range(K)) - mang_price * num_mang
problem += profit, "Total_Profit"

#### Constraints
#### Manganese content constraint
problem += pulp.lpSum((amount[k] * contmn[k] / 100) for k in range(K)) + num_mang >= (mn_percent / 100) * n_steel_quant, "Manganese_Content"

#### Silicon content constraints
problem += (pulp.lpSum((amount[k] * contsi[k] / 100) for k in range(K)) / n_steel_quant) >= si_min, "Silicon_Min_Content"
problem += (pulp.lpSum((amount[k] * contsi[k] / 100) for k in range(K)) / n_steel_quant) <= si_max, "Silicon_Max_Content"

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

