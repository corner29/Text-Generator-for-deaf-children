import requests
import sys

def text(url, title):
    data, error = process(url)
    
    if data:
        filename = title + '.txt'
        with open(filename, 'w') as f:
            f.write(data['text'])
        print('Transcript saved')
    elif error:
        print("Error!!!", error)

def process(url):
    transcribe_id = converting(url)
    while True:
        data = is_complete(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']            

def converting(audio_url):
    transcript_request = {
        'audio_url': audio_url
    }
    transcript_response = requests.post('https://api.assemblyai.com/v2/transcript', json=transcript_request, headers={'authorization': 'Enter your API key here'})
    return transcript_response.json()['id']

        
def is_complete(transcript_id):
    polling_endpoint = 'https://api.assemblyai.com/v2/transcript' + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers={'authorization': 'Enter your API key here'})
    return polling_response.json()

def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(5_242_880)
                if not data:
                    break
                yield data

    upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers={'authorization': 'Enter your API key here'}, data=read_file(filename))
    return upload_response.json()['upload_url']

filename = sys.argv[1]
audio_url = upload(filename)
text(audio_url,'text')