import os
import json


def combine_json_files(input_directory, output_file):
    # Initialize an empty list to store all combined data
    combined_data = []

    # Loop through each file in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            filepath = os.path.join(input_directory, filename)
            with open(filepath, "r") as file:
                data = json.load(file)
                combined_data.append(data)

    # Save the combined data into a single JSON file
    with open(output_file, "w") as output_file:
        json.dump(combined_data, output_file, indent=4)

    print(f"Combined data saved to {output_file}")


# Define the input directory and output file
input_directory = "JSON_FILES"
output_file = "combined_data.json"

# Call the function to combine JSON files
combine_json_files(input_directory, output_file)
