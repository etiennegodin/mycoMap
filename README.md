# mycoMap

# goals

### 1.






maybe un peu de machine learning pour tweak le strength des parametres dimportance pour final value 
necessite targte training 
tensorflow??


The primary abiotic variables that impact mushroom production are temperature, humidity, light,


https://www.sciencedirect.com/science/article/pii/S0378112722004455

The interaction between precipitation and temperature modulated mushroom production.
•
Mushroom production was enhanced by mushrooms species richness.
•
Ectomycorrhizal species richness was mainly affected by stand characteristics.
•
Species richness of saprotrophic mushrooms was affected by pH of the soil.

Ambient temperature, soil humidity, and especially precipitation in the summer and autumn seem to be the most important factors explaining differences in mushroom production

Among other environmental characteristics, nitrogen concentration, pH, type of soil, slope, and elevation are listed as main predictors of mushroom production

The type of soil also matters, as fewer mushrooms are observed in soils with decreasing proportion of sand

Among basic tree stand characteristics, stand age, stand basal area, and canopy cover are most commonly reported to have the greatest impact on mushroom production. Mushroom yield is higher in younger stands, due to the faster growth rate of young trees


Tree identity and tree species richness influence the fungal biomass and species composition of fungi.



They also revealed that tree composition can explain a large proportion of variation in the species composition of fungal communities, even greater than soil properties

________________
Statistics

This is the simplest form, where we have one thing we’re trying to predict and one thing we think might influence it. For example, We are perform a predictive analysis where are trying to predict someone’s weight based on their height.

Multiple Linear Regression: Here, things get a bit more complex. We’re still predicting one thing, but now we’re considering multiple factors that might influence it. For instance, we might predict a person’s weight based on their height, age, and maybe even their diet habits.


____________________________________________________

Data Preparation:

Encoding Categorical Variables: Convert categorical variables into numerical formats suitable for modeling. For nominal variables (without intrinsic order), use one-hot encoding. For ordinal variables (with a clear order), assign integer values corresponding to their order. 
Handling Continuous Variables: Ensure continuous variables are scaled appropriately, especially if the modeling technique is sensitive to variable scales. Standardization or normalization can be applied as needed. 

Exploratory Data Analysis (EDA):

Visualization: Create plots to understand relationships between variables and the target occurrence variable. This helps in identifying patterns and potential interactions.
Correlation Analysis: Assess correlations between predictors and the target variable to identify significant relationships.
Model Selection:

Species Distribution Models (SDMs): These models are commonly used to predict species occurrence based on environmental variables. They can handle various data types and are suitable for presence-absence or presence-only data. 

Generalized Linear Models (GLMs): GLMs, such as logistic regression, can model the probability of species occurrence. They can incorporate different types of predictor variables and are interpretable.
Machine Learning Algorithms: Techniques like Random Forests or Gradient Boosting Machines can capture complex relationships and interactions between variables. They handle mixed data types effectively but may require larger datasets.
Model Training and Evaluation:

Training: Fit the chosen model to your dataset, ensuring that the data is appropriately split into training and testing sets to evaluate performance.
Evaluation Metrics: Use metrics such as Area Under the Receiver Operating Characteristic Curve (AUC-ROC) for classification models to assess predictive performance.
Prediction and Interpretation:


Predicting Occurrence Probability: Use the trained model to predict the likelihood of species occurrence for new data points.
Interpreting Results: Analyze model coefficients or feature importances to understand the influence of each variable on species occurrence.
Software and Tools:

R and Python: Both programming languages offer packages for species distribution modeling and handling mixed data types. In R, packages like dismo and caret are useful. In Python, libraries such as scikit-learn and statsmodels can be employed.
Combining Multiple Data Sources:

Integrating data from various sources can enhance model performance. Approaches like Integrated Species Distribution Models (ISDMs) allow for the combination of different data types to improve predictions. 

By following these steps, you can effectively interpret and predict species occurrence likelihood using a dataset with ordinal, categorical, and continuous variables. It's essential to consider the ecological context and ensure that the chosen modeling approach aligns with the characteristics of your data and research objectives.


_____________________________________________________________________________________
_____________________________________________________________________________________
_____________________________________________________________________________________


Generalized Linear Models (GLMs) are a versatile extension of traditional linear regression models, designed to handle various types of response variables and relationships between predictors and the response. In the context of species distribution modeling, GLMs are particularly useful for predicting the probability of species occurrence based on environmental and spatial variables.

Key Features of GLMs:

Flexibility in Response Variables: GLMs can model response variables that are not normally distributed, such as binary (presence/absence), count (number of occurrences), or continuous data. This flexibility makes them suitable for ecological data, which often involve diverse types of response variables.

Incorporation of Various Predictor Variables: GLMs can include different types of predictor variables—continuous (e.g., temperature), categorical (e.g., habitat type), and ordinal (e.g., soil quality grades). This capability allows for a comprehensive analysis of factors influencing species occurrence.

Interpretability: The coefficients estimated in GLMs provide insights into the relationship between predictor variables and the response variable. For instance, in a logistic regression model, the coefficients indicate how changes in predictor variables affect the log-odds of species presence, aiding in ecological interpretation and decision-making.

Example: Modeling Species Occurrence with Logistic Regression

Suppose we aim to model the probability of a particular plant species' presence based on environmental variables such as elevation, soil type, and annual precipitation.

Data Preparation:

Response Variable: Binary indicator of species presence (1) or absence (0).
Predictor Variables:
Elevation: Continuous variable representing altitude.
Soil Type: Categorical variable indicating soil classification.
Annual Precipitation: Continuous variable measuring yearly rainfall.
Model Specification:

We use logistic regression, a type of GLM suitable for binary response variables, to model the probability of species presence.

The model can be expressed as:

Interpretation:

Coefficients: The sign and magnitude of the coefficients indicate the direction and strength of the relationship between predictors and the probability of species presence.

Odds Ratios: Exponentiating the coefficients provides odds ratios, which quantify how a one-unit change in a predictor affects the odds of species presence.Advantages of Using GLMs in Species Distribution Modeling:

Handling Non-linear Relationships: By applying appropriate link functions (e.g., logit for binary data), GLMs can model non-linear relationships between predictors and the response variable.

Accommodating Different Data Distributions: GLMs are not restricted to normal distributions and can handle various types of data distributions, making them suitable for ecological data that often deviate from normality.

Modeling Interactions: GLMs can include interaction terms to explore how the combined effect of predictors influences species occurrence.

Applications in Ecology:

GLMs are widely used in species distribution modeling to:

Predict Species Presence: Estimate the likelihood of species occurrence in unsurveyed areas based on environmental predictors.

Identify Key Environmental Factors: Determine which environmental variables significantly influence species distribution.

Inform Conservation Strategies: Guide habitat management and conservation planning by understanding species-environment relationships.

For a practical implementation of GLMs in species distribution modeling, the R programming language offers packages such as fuzzySim, which facilitates modeling species presence-absence records and computing occurrence probabilities. 
FUZZYSIM

In summary, Generalized Linear Models, including logistic regression, provide a robust framework for modeling species occurrence probabilities. Their ability to incorporate diverse predictor variables and offer interpretable results makes them valuable tools in ecological modeling and conservation planning.