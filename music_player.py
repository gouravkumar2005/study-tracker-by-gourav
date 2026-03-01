try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    SPOTIFY_AVAILABLE = True
except ImportError:
    SPOTIFY_AVAILABLE = False

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

import webbrowser

class StudyMusicPlayer:
    def __init__(self):
        self.spotify = None
        self.spotify_enabled = False
        self.current_track = None
        self.playlist = []
        
        # Spotify credentials (user needs to set these)
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = "http://localhost:8888/callback"
        
    def connect_spotify(self, client_id, client_secret):
        """Connect to Spotify"""
        if not SPOTIFY_AVAILABLE:
            return False, "Spotify library not installed. Run: pip install spotipy"
        
        try:
            self.client_id = client_id
            self.client_secret = client_secret
            
            scope = "user-read-playback-state,user-modify-playback-state,playlist-read-private"
            self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=self.redirect_uri,
                scope=scope
            ))
            
            # Test connection
            self.spotify.current_user()
            self.spotify_enabled = True
            return True, "Connected to Spotify successfully!"
        except Exception as e:
            return False, f"Failed to connect: {str(e)}"
    
    def search_tracks(self, query, limit=10):
        """Search for tracks on Spotify"""
        if not self.spotify_enabled:
            return []
        
        try:
            results = self.spotify.search(q=query, type='track', limit=limit)
            tracks = []
            for item in results['tracks']['items']:
                tracks.append({
                    'name': item['name'],
                    'artist': item['artists'][0]['name'],
                    'uri': item['uri'],
                    'id': item['id']
                })
            return tracks
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def play_track(self, track_uri):
        """Play a track on Spotify"""
        if not self.spotify_enabled:
            return False, "Spotify not connected"
        
        try:
            devices = self.spotify.devices()
            if not devices['devices']:
                return False, "No active Spotify device found. Please open Spotify app."
            
            self.spotify.start_playback(uris=[track_uri])
            self.current_track = track_uri
            return True, "Playing track"
        except Exception as e:
            return False, f"Playback error: {str(e)}"
    
    def pause(self):
        """Pause playback"""
        if not self.spotify_enabled:
            return False
        try:
            self.spotify.pause_playback()
            return True
        except:
            return False
    
    def resume(self):
        """Resume playback"""
        if not self.spotify_enabled:
            return False
        try:
            self.spotify.start_playback()
            return True
        except:
            return False
    
    def next_track(self):
        """Skip to next track"""
        if not self.spotify_enabled:
            return False
        try:
            self.spotify.next_track()
            return True
        except:
            return False
    
    def previous_track(self):
        """Go to previous track"""
        if not self.spotify_enabled:
            return False
        try:
            self.spotify.previous_track()
            return True
        except:
            return False
    
    def get_playlists(self):
        """Get user's playlists"""
        if not self.spotify_enabled:
            return []
        
        try:
            playlists = self.spotify.current_user_playlists(limit=20)
            result = []
            for item in playlists['items']:
                result.append({
                    'name': item['name'],
                    'id': item['id'],
                    'tracks': item['tracks']['total']
                })
            return result
        except:
            return []
    
    def play_playlist(self, playlist_id):
        """Play a playlist"""
        if not self.spotify_enabled:
            return False, "Spotify not connected"
        
        try:
            devices = self.spotify.devices()
            if not devices['devices']:
                return False, "No active Spotify device found"
            
            self.spotify.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
            return True, "Playing playlist"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def open_spotify_web(self):
        """Open Spotify web player"""
        webbrowser.open("https://open.spotify.com")
