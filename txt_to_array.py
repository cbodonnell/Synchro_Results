import csv

#Imports a tab-delimited .txt file and converts it to a 2D array
#Removes blank lines and excess whitespace
def txt_to_array(path):
    with open(path) as f:
        reader = csv.reader(f, delimiter="\t")
        noBlanks = [line for line in list(reader) if len(line)>0]
        clean = [[item.strip() for item in line] for line in noBlanks]
    return clean
