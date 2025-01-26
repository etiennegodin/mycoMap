# mycoMap

# **Goals**

# Main flaws current


convert vector forest composition in raster to sample
faster ? 
## Filter goedata 

### Spatial Filtering

Reduce over-sampling by thinning the dataset spatially. This involves removing closely clustered records to ensure a more uniform spatial coverage.
For example, set a minimum distance threshold between occurrences (e.g., 1 km apart) and retain only one record per grid cell or area.


### Biais layer

close to city
national park 



Examples of Hypotheses to Test
Fungi species richness increases with tree stand diversity index.
Fungi species X is more likely to occur on soils of type A than type B.
Higher tree height classes are associated with lower fungi diversity.
Slope class has a significant impact on fungi community composition.
Tree density class predicts the presence of specific fungi species.




Species-Habitat Associations

Which abiotic factors are most strongly associated with the presence of specific fungi species?
Are certain fungi species more common in specific soil types, slope classes, or areas with particular tree stand diversity?
Biodiversity Patterns

How does fungi species richness (number of species) vary with tree stand diversity or Shannon index?
Is there a correlation between fungi diversity and tree stand diversity?
Environmental Gradients

How do environmental gradients (e.g., slope, tree height, soil type) influence fungi distribution and abundance?
Are there threshold effects where certain conditions favor or inhibit fungi occurrences?
Co-occurrence Patterns

Do certain fungi species co-occur in the same areas, and what abiotic conditions favor these co-occurrences?
Are there signs of niche partitioning among species?
Predictive Modeling

Can you predict the occurrence of specific fungi species based on abiotic variables?




















### Create map of specific specie likelyhood 

# Main ideas to improve scripts 

## 1. Calculate metrics of occurence to create sub-groups of study 

### Webscrap mycoquebec 
Get infos like 
ecology
Periodes fructification

### find species 
find species with most occurence, create list ( exploaratory in this script)

### download data ( first portion of this main.py)
make iterable if fed list of species from exploratory phase

### get data run only when confirmation of gbif , could make fancy trigger, like query email of gbif account 
include geo data anylissis in get_data script
iterable too

## Data enhancement, filter, modify 
account for fact thta occurens are human and flaws (only in cities or near centers)
entropy concept ???

## analysis only - could include iterating over acquired species (by group) 
list of all dirs in gbifQueries an iterate over to do stats and find multiple ocrelation 
could help define most influencal factors fro groups of mushroom instaed of juste one specifc

## anaylyse timeseries, based on occurence date 

yearly always same months
i.e. plus chance en juin 
#### shift accorss years ?
example juin -> juillet 

### if null hypothesis rejected 

proceed to do map visual 
from linear fit, 
  