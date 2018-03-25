import spotipy
import spotipy.util as util
import pandas as pd
import json

file = 'data/billboard_lyrics_2000-2015.csv'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

df = pd.read_csv(file)
lo = 0

while lo < 1562:
    quickview = df.iloc[lo:lo+50, 0:5]
    ids = []
    energy = []
    liveness = []
    tempo = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    time_signature = [] 
    danceability = [] 
    key = []
    duration_ms = []
    loudness = []
    valence = [] 
    
    if token:
        sp = spotipy.Spotify(auth=token)
        for index, row in quickview.iterrows():
            myQ = row['Song'],' ',row['Artist']
            results = sp.search(q=myQ, limit=1)
            if len(results['tracks']['items']) < 1:
                ids.append('NA')    
                continue
            for t in results['tracks']['items']:
                print t['id'], ' ', t['name']
                ids.append(t['id'])
    else:
        print "Can't get token for", username
    
    features = sp.audio_features(ids)
    for i in range(len(features)):
        json_string = json.dumps(features[i], indent=4)
        json_dict = json.loads(json_string)
        if json_dict is not None:
            energy.append(json_dict['energy'])
            liveness.append(json_dict['liveness'])
            tempo.append(json_dict['tempo'])
            speechiness.append(json_dict['speechiness'])
            acousticness.append(json_dict['acousticness'])
            instrumentalness.append(json_dict['instrumentalness'])
            time_signature.append(json_dict['time_signature'])
            danceability.append(json_dict['danceability'])
            key.append(json_dict['key'])
            duration_ms.append(json_dict['duration_ms'])
            loudness.append(json_dict['loudness'])
            valence.append(json_dict['valence'])
        else: 
            energy.append('NA')
            liveness.append('NA')
            tempo.append('NA')
            speechiness.append('NA')
            acousticness.append('NA')
            instrumentalness.append('NA')
            time_signature.append('NA')
            danceability.append('NA')
            key.append('NA')
            duration_ms.append('NA')
            loudness.append('NA')
            valence.append('NA')  
    
    quickview['ids'] = ids
    quickview['energy'] = energy
    quickview['liveness'] = liveness
    quickview['tempo'] = tempo
    quickview['speechiness'] = speechiness
    quickview['acousticness'] = acousticness
    quickview['instrumentalness'] = instrumentalness
    quickview['time_signature'] = time_signature
    quickview['danceability'] = danceability
    quickview['key'] = key
    quickview['duration_ms'] = duration_ms
    quickview['loudness'] = loudness
    quickview['valence'] = valence
    
    if lo == 0: 
        quickview.to_csv('data/output.csv')
    else: 
        quickview.to_csv('data/output.csv',mode='a')
    
    lo = lo + 50