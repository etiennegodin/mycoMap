import os 
import csv
l = os.listdir('data/geodata/raw/vector/regions_data/')
print(l)

with open('data/input/table/qc_regions.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["region"])
    for i in l:
        writer.writerow([i])