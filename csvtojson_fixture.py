import sys
import getopt
import csv
from os.path import dirname
import simplejson

try:
    script, input_file_name, model_name = sys.argv
except ValueError:
    print "\nRun via:\n\n%s input_file_name model_name" % sys.argv[0]
    print "\ne.g. %s airport.csv app_airport.Airport" % sys.argv[0]
    print "\nNote: input_file_name should be a path relative to where this script is."
    sys.exit()

in_file = dirname(__file__) + input_file_name
out_file = dirname(__file__) + input_file_name + ".json"

print "Converting %s from CSV to JSON as %s" % (in_file, out_file)

f = open(in_file, 'r' )
fo = open(out_file, 'w')

reader = csv.reader( f )

header_row = []
entries = []
for row in reader:
    if not header_row:
        header_row = row
        continue
        
    pk = row[0]
    model = model_name
    fields = {}
    for i in range(len(row)-1):
        active_field = row[i+1]
        if active_field.isdigit():
            try:
                new_number = int(active_field)
            except ValueError:
                new_number = float(active_field)
            fields[header_row[i+1]] = new_number
        else:
            fields[header_row[i+1]] = active_field.strip()
        
    row_dict = {}
    row_dict["pk"] = int(pk)
    row_dict["model"] = model_name
    
    row_dict["fields"] = fields
    entries.append(row_dict)

fo.write("%s" % simplejson.dumps(entries, indent=4))
f.close()
fo.close()
