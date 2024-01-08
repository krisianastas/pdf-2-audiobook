import requests, json, time, pypdf

good_response = bool
pdf_text = ""
local_pdf_name = input("Please type the name of your PDF file: ")
try:
  with open (local_pdf_name + ".pdf", "rb") as f:
    pdf = pypdf.PdfReader(f)
    numOfPages = len(pdf.pages)
    for i in range(numOfPages):
      page = pdf.pages[i]
      pdf_text += page.extract_text()
except:
  print("This file does not exist.")
  exit()

apikey = "YOUR API KEY" 
filename = local_pdf_name + ".wav"

headers = {'content-type': "application/json", 'x-rapidapi-host': "large-text-to-speech.p.rapidapi.com", 'x-rapidapi-key': apikey}
response = requests.request("POST", "https://large-text-to-speech.p.rapidapi.com/tts", data=json.dumps({"text": pdf_text}), headers=headers)
try:
  id = json.loads(response.text)['id']
  eta = json.loads(response.text)['eta']
  print(f'Waiting {eta} seconds for the job to finish...')
  time.sleep(eta)
  good_response = True
except:
   print("Error connecting to the server.")
   good_response = False

if good_response:
  response = requests.request("GET", "https://large-text-to-speech.p.rapidapi.com/tts", headers=headers, params={'id': id})
  while "url" not in json.loads(response.text):
      response = requests.request("GET", "https://large-text-to-speech.p.rapidapi.com/tts", headers=headers, params={'id': id})
      print(f'Waiting 5 more seconds...')
      time.sleep(5)
else:
   exit()

url = json.loads(response.text)['url']
response = requests.request("GET", url)
with open(filename, 'wb') as f:
    f.write(response.content)
print(f'File saved to {filename} ! \nOr download here: {url}')