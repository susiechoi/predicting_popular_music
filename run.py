import spotipy
import spotipy.util as util
import pandas as pd

file = 'data/billboard_lyrics_1964-2015.csv'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

df = pd.read_csv(file).iloc[0:10,0:5]

ids = []

if token:
    sp = spotipy.Spotify(auth=token)
    for index, row in df.iterrows():
        myQ = row['Song'],' ',row['Artist']
        results = sp.search(q=myQ, limit=1)
        for t in results['tracks']['items']:
            print t['id'], ' ', t['name']
            ids.append(t['id'])
else:
    print "Can't get token for", username
    
df['ids'] = ids
print sp.audio_features(tracks=ids)

# df.to_csv('data/output.csv',mode = 'a')