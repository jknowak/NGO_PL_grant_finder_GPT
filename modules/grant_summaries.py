import os
import glob
import csv
import hashlib
import openai
import pandas as pd

# Function to summarize the Opis using OpenAI API
def summarize_opis(opis):
    # Call the OpenAI API to summarize the Opis
    # Replace 'YOUR_API_KEY' with your actual OpenAI API key
    openai.api_key = 'YOUR_API_KEY'
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=opis,
        max_tokens=100,
        temperature=0.5,
        n=1,
        stop=None,
        temperature=0.5
    )
    summary = response.choices[0].text.strip()
    return summary

def get_grants_summaries_dict():
    # read file and return dictionary
    
    grants_summaries_dict = {}

def regenerate_file(): -> None
    
    # Directory where the data files are located
    data_directory = './data/grants/'
    summaries_directory = './data/grants/summaries/'
    
    # Get a list of all files matching the pattern 'ngo_pl_id_*.txt'
    file_pattern = os.path.join(data_directory, 'ngo_pl_id_*.txt')
    files = glob.glob(file_pattern) #gets all files in the directory
    # get list of id's sorted
    ids = [int(file.split('_')[-1].split('.')[0]) for file in files]
    
    # Check if there are any new grants by comparing the list of files with a hash of the previous list
    previous_grants_hash = hashlib.md5(','.join(files).encode()).hexdigest()
    previous_grants_hash_file = '/path/to/previous_grants_hash.txt'
    
    if os.path.exists(previous_grants_hash_file):
        with open(previous_grants_hash_file, 'r') as f:
            previous_grants_hash_saved = f.read().strip()
        if previous_grants_hash == previous_grants_hash_saved:
            print("No new grants scraped. Exiting...")
            exit()
    
    # Process each file and summarize the Opis
    output_file = '/path/to/output.csv'
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Summary'])
        
        for file in files:
            with open(file, 'r') as f:
                opis = f.read()
            
            summary = summarize_opis(opis)
            writer.writerow([os.path.basename(file), summary])
    
    # Save the hash of the current list of grants
    with open(previous_grants_hash_file, 'w') as f:
        f.write(previous_grants_hash)
    
    print("Summary generation completed and saved to", output_file)