import csv
import json
import os
import hashlib
import requests

SHEET_ID ='1b5H3bp_9-YVjTYQNjLeokXJewrcPfgUo_MYvYXtaUno'

SHEET_NAME = 'Sheet1'

url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'


rows = []

def download_csv():
    print("Downloading data...")
    response = requests.get(url)
    
    with open('data.csv', 'w') as file:
        file.write(response.content.decode('utf-8'))
    print('Done')
    
    generate_json()
    

def generate_json():
    
    if not os.path.exists('jsons'):
        os.mkdir('jsons')

    with open("data.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        current_team = ''
        
    
        for line,row in enumerate(csv_reader):
            row = row[:8]
            team, sn, filename, name, description, gender, attributes, _ = row
            
            if line== 0:
              
                print(f'HEADERS:  {", ".join([x for i,x in enumerate(row) if i<8])}')
                print()
                print('Starting CHIP-007 json creation...')
                row.append('Hash')
                rows.append(row)
                
            else:
                if team:
                    current_team = team
                    
                item = {
                            "format": "CHIP-0007",
                            "name": name,
                            "description": description,
                            "minting_tool": current_team,
                            "sensitive_content": False,
                            "series_number": sn,
                            "series_total": 526,
                            "attributes": [
                                {
                                    "trait_type": "gender",
                                    "value": gender,
                                },
                                
                            ],
                            "collection": {
                                "name": "Zuri NFT Tickets for Free Lunch",
                                "id": "b774f676-c1d5-422e-beed-00ef5510c64d",
                                "attributes": [
                                    {
                                        "type": "description",
                                        "value": "Rewards for accomplishments during HNGi9.",
                                    }
                                ],
                            },
                        }
                attr = [x.split(':') for x in attributes.split(';') if x]
                
                for att in attr:
                    item['attributes'].append({'trait_type': att[0].strip(), 'value':att[1].strip()})
                
                with open(f'jsons/{filename}.json', 'w') as jf:
                    data = json.dumps(item, indent=4)
                    data_hash = hashlib.sha256(data.encode()).hexdigest()
                    row.append(data_hash)
                    rows.append(row)
                    jf.write(data)
                            
    print('Done')
    generate_output()
                    

                        

def generate_output():
    print('Generating output...')
    if not os.path.exists('output'):
        os.mkdir('output')
        
    
    with open('output/data.output.csv', 'w') as write_file:
          cw = csv.writer(write_file)
          cw.writerows(rows)
    print('Done')
                


if __name__=='__main__':
    download_csv()
   