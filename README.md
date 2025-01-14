# mycoMap

# Goals

## 1. (New) Find actors that exlains mushroom species diveristy 

Download multiple species of same group (sapotrophic, mycrorrhizal)
X Independant variable remain same as previous
Y Dependant variable is number of species found ( instead of count) 

### Create map of species diversity index of forest 

## 2. Predict likelihood of finding species base on factors 

Count of occurences for given factors
Logistic regression with multiple inputs 
Maybe create data points without occurence 

### Create map of specific specie likelyhood 

# Main ideas to improve scripts 

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
  