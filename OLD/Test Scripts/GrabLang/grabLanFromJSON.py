import json

# Opening JSON file
langFile = open('languages.json')
  
# returns JSON object as 
# a dictionary
langFiledata = json.load(langFile)

file1 = open("options.txt", "w")
# Iterating through the json
# list
for i in langFiledata:
    newline = f'<option value="{i}">{i}</option>'
    # Append-adds at last
    file1 = open("myfile.txt", "a")  # append mode
    file1.write(newline)

    # print(i)
    # print(langFiledata[i])
    # print("\n")
  
# Closing file
langFile.close()