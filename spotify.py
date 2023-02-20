from spotipy import Spotify
import requests
import json


class InvalidSearchError(Exception):
    pass


def get_artist_uri(spotify: Spotify, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: album name
    :return: Spotify uri of the desired artist
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='artist')
    if not results['artists']['items']:
        raise InvalidSearchError(f'No artist named "{original}"')
    artist_uri = results['artists']['items'][0]['uri']
    print(results['artists']['items'][0]['name'])
    return artist_uri


def get_track_uri(spotify: Spotify, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: track name
    :return: Spotify uri of the desired track
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='track')
    if not results['tracks']['items']:
        raise InvalidSearchError(f'No track named "{original}"')
    track_uri = results['tracks']['items'][0]['uri']
    return track_uri


def play_artist(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, context_uri=uri)
    
    
def add_to_queue(spotify=None, device_id=None, uri=None):
    spotify.add_to_queue(device_id=None, uri=uri)


def play_track(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, uris=[uri])


def repeat(spotify=None, device_id=None, state=None):
    spotify.repeat(device_id=device_id, state=state)
  
  
def shuffle(spotify=None, state=None, device_id=None):
    spotify.shuffle(state=state, device_id=device_id)
    

def pause_playback(spotify=None, device_id=None):
    spotify.pause_playback(device_id=device_id)


def next_track(spotify=None, device_id=None):
    spotify.next_track(device_id=device_id)
    
    
def previous_track(spotify=None, device_id=None):
    spotify.previous_track(device_id=device_id)
    
    
def resume(spotify=None, device_id=None, access_token=None):
    SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()
    
    # print(json.dumps(response.json(), indent=2))

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    progress_ms = json_resp['progress_ms']
    uri = json_resp['item']['uri']

    current_track_info = {
        "id": track_id,
        "track_name": track_name,
        "progress_ms": progress_ms,
        "uri": uri,
    }
    spotify.start_playback(device_id=device_id, position_ms=progress_ms, uris=[uri])


def volume(spotify=None, volume_percent=None, device_id=None):
    spotify.volume(volume_percent=volume_percent, device_id=device_id)