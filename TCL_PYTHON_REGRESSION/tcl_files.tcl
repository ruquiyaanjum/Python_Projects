#TCL CODE FOR READING A MULTIPLE FILES FROM LOCAL DIRECTORY
# Define the folder containing CSV files
set folder_path "/home/data"

# Get a list of all CSV files in the folder
set csv_files [glob -nocomplain "${folder_path}/*.csv"]

# Iterate over each CSV file
foreach file_name $csv_files {
    # Open the CSV file for reading
    set file [open $file_name "r"]
    puts "Contents of $file_name:"
    
    # Read and process each line of the file
    while {[gets $file line] != -1} {
        # Split the line into fields
        set fields [split $line ","]
        
        # Print each field
        foreach field $fields {
            puts $field
        }
    }
    
    puts "" ;# Print an empty line to separate files
    
    # Close the file
    close $file
}


