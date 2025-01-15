# mycoMap

# Goals

# Main flaws current

## ****Can't predict count with linear regression
### Would instead need to predict probaility / likelyhood based on counts
### Not counts based on type of soil like now ****** 


## 1. (New) Find actors that explains mushroom species diveristy 

## ****** First explore if plausbile to get mutiple occurence on same geo_point???? *********
Find 20 species with most observations 

Download multiple species of same group (sapotrophic, mycrorrhizal)
X Independant variable remain same as previous

### Make meta dataframe from individual species df
Merge on geoc_maj
#### Ideally would find some geo_point with multiple species occurences on it ??  
Otherwise could merge from similar env_factors, ex all geo points with cl_haut = 1 etc 

Store species found (key)
Store count of each species (value)
### Can calculate diversity index and shannon inex on meta dataframe 
On this data point, basedo n number of speices found = diversity index 
On this datat point based on proability of each species , calculate shannon index
Both could become Y depenant variable 

Y Dependant variable is number of species found ( instead of count)  ?

### Create map of species diversity index of forest 

## 2. Predict likelihood of finding species base on factors 



Count of occurences for given factors
Logistic regression with multiple inputs 
https://www.youtube.com/watch?v=vN5cNN2-HWE&ab_channel=StatQuestwithJoshStarmer
Maybe create data points without occurence 

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
  