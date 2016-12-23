# unearth

This project features a very basic implementation of web link extractor
using the Producer/Consumer approach, which takes an input file containing
list of urls to be fetched and returns a list of url it found on that page.


## How to use ?

1. Simply create a file which contains one url per line and place it inside
the data folder. Refer data/sample_input for details. Please ensure that the
input file is inside the data folder. The output file will also get written
inside the data folder.


2. Run the prgram as -
$ python main.py input_file=sample_input output_file=sample_output


The output file will be in csv format, containing the supplied url from input file
in each line, with the extracted urls following it. If there occured any error while
fetching any url/ parsing its content, those urls will not be present in this file.
If there are no urls following the supplied url, that would imply that no links were
extracted from that page.

'output_file' keyword is optional. if not supplied, the program will itself
create an output file having name as <inputfile>_output.csv

