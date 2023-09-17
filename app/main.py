import time
import cv2
import transformers
import torch
import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import math

load_dotenv()

scope = "user-library-read,playlist-read-collaborative,\
user-read-playback-state,user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

device_id = "aebd3ba2eda9d51d3f907d45e6e50ebe994b9253"
soundtrack_playlist_url = "0OvyXIAjpkaryB8xvhBTiY"
test_track_url = "6tpWeI6ijAmAHZJSVQu8Kn"

## UTILITY FUNCTIONS

# get all tracks in target playlist
def getPlaylist(playlistId):
    playlists = sp.playlist(playlistId)
    tracklist = playlists['tracks']['items']
    return tracklist

# get list of ids for a target playlist
def getPlaylistTrackIds(playlistId):
    tracklist = getPlaylist(playlistId)
    tracklistId = list(map(lambda t: t['track']['id'], tracklist))
    return tracklistId

# get all audio features for array of tracks
def getAudioFeatures(tracks):
    return sp.audio_features(tracks)

# get just the emotion for a single track
def getEmotion(track):
    features = getAudioFeatures([track])
    return (features[0]['valence'], features[0]['energy'])

def getTrackToEmotions(playlistId):
    tracklistIds = getPlaylistTrackIds(playlistId)
    mapping = {}
    for track in tracklistIds:
        mapping[track] = getEmotion(track)

    return mapping

def getUriFromTrackId(trackId):
    return sp.track(trackId)['uri']

print(sp.devices())
# print(getEmotion(test_track_url))
# print(getPlaylist(soundtrack_playlist_url))
# print(getPlaylistTrackIds(soundtrack_playlist_url))
# sp.start_playback(device_id)

# SONG PLAYING ALGOS

print(getTrackToEmotions(soundtrack_playlist_url))

def emotion_cat2dim(category: str) -> tuple[float, float]:
    if category == "amusement":
        valence, arousal = 0.55, 0.1
    elif category == "anger":
        valence, arousal = -0.4, 0.8
    elif category == "awe":
        valence, arousal = 0.3, 0.9
    elif category == "contentment":
        valence, arousal = 0.9, -0.3
    elif category == "disgust":
        valence, arousal = -0.7, 0.5
    elif category == "excitement":
        valence, arousal = 0.7, 0.7
    elif category == "fear":
        valence, arousal = -0.1, 0.7
    elif category == "sadness":
        valence, arousal = -0.8, -0.7
    return (valence, arousal)

image_processor = transformers.ViTImageProcessor.from_pretrained("google/vit-large-patch16-224")
model = transformers.ViTForImageClassification.from_pretrained("./model/")

idx2cat = [
    "amusement",
    "anger",
    "awe",
    "contentment",
    "disgust",
    "excitement",
    "fear",
    "sadness",
]

# Initialize the video capture
cap = cv2.VideoCapture(0)  # 0 refers to the default camera

# currently playing song id
currentSong = ""

with torch.no_grad():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('Video Stream', frame)

        # Break the loop if 'q' is pressed
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        if int(time.time()) % 5 == 0:
            cat_idx = model(**image_processor(frame, return_tensors="pt")).logits
            probs = torch.nn.functional.softmax(cat_idx)[0, :8]
            emotion = np.array([0, 0], dtype=np.float32)
            for idx, cat in enumerate(idx2cat):
                print(f"{cat}: {probs[idx]}")
                emotion += np.array(emotion_cat2dim(cat))*probs[idx].item()
            print()
            emotion_vector = (emotion[0], emotion[1])
            minId = ""
            minDist = 5
            for id, emo in getTrackToEmotions(soundtrack_playlist_url).items():
                if math.dist(emotion_vector, emo) < minDist:
                    minId = id
                    minDist = math.dist(emotion_vector, emo)

            if currentSong == minId:
                pass
            else:
                currentSong = minId

                sp.start_playback(device_id, uris=[getUriFromTrackId(minId)])
            

# Release the capture
cap.release()
cv2.destroyAllWindows()
