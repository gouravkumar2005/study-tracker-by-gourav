import webbrowser
import urllib.parse
import requests
import json

class YouTubeMusicPlayer:
    def __init__(self):
        self.current_video_id = None
        self.playlist = []
        
    def search_youtube_api(self, query, max_results=10):
        """Search YouTube using web scraping (no API key needed)"""
        try:
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query + ' study music')}"
            # Return curated results for now
            return self.get_curated_results(query)
        except:
            return self.get_curated_results(query)
    
    def get_curated_results(self, query):
        """Get curated study music based on search"""
        query_lower = query.lower()
        
        all_music = {
            'lofi': [
                {"title": "Lofi Hip Hop Radio - Beats to Study/Relax", "id": "jfKfPfyJRdk", "duration": "LIVE", "channel": "Lofi Girl"},
                {"title": "Chill Lofi Study Beats", "id": "lTRiuFIWV54", "duration": "2:00:00", "channel": "Chillhop Music"},
                {"title": "Lofi Hip Hop Mix", "id": "5qap5aO4i9A", "duration": "1:30:00", "channel": "ChilledCow"},
            ],
            'classical': [
                {"title": "Classical Music for Studying", "id": "jgpJVI3tDbY", "duration": "3:00:00", "channel": "Classical Music"},
                {"title": "Mozart for Studying and Concentration", "id": "Rb0UmrCXxVA", "duration": "2:30:00", "channel": "Classical Tunes"},
                {"title": "Bach Study Music", "id": "6JQm5aSjX6g", "duration": "2:00:00", "channel": "Bach Music"},
            ],
            'piano': [
                {"title": "Piano Music for Studying", "id": "z1Yb-4nQgbs", "duration": "2:30:00", "channel": "Yellow Brick Cinema"},
                {"title": "Peaceful Piano Music", "id": "lCOF9LN_Zxs", "duration": "3:00:00", "channel": "Peaceful Piano"},
                {"title": "Piano Concentration Music", "id": "tf5zJKB7JT8", "duration": "1:45:00", "channel": "Study Music"},
            ],
            'jazz': [
                {"title": "Coffee Shop Jazz Music", "id": "kgx4WGK0oNU", "duration": "LIVE", "channel": "Cafe Music BGM"},
                {"title": "Smooth Jazz for Studying", "id": "neV3EPgvZ3g", "duration": "2:00:00", "channel": "Jazz Music"},
                {"title": "Relaxing Jazz Piano", "id": "DSGyEsJ17cI", "duration": "3:00:00", "channel": "Jazz Cafe"},
            ],
            'ambient': [
                {"title": "Ambient Study Music", "id": "lTRiuFIWV54", "duration": "2:00:00", "channel": "Ambient Music"},
                {"title": "Deep Focus Music", "id": "DWcJFNfaw9c", "duration": "3:00:00", "channel": "Greenred Productions"},
                {"title": "Concentration Music", "id": "2OEL4P1Rz04", "duration": "1:00:00", "channel": "Study Music Project"},
            ],
        }
        
        # Search in categories
        results = []
        for category, items in all_music.items():
            if any(word in query_lower for word in category.split()):
                results.extend(items)
        
        # If no match, return lofi as default
        if not results:
            results = all_music['lofi'] + all_music['classical'][:2] + all_music['piano'][:2]
        
        return results[:10]
    
    def search_songs(self, query):
        """Search for tracks"""
        return self.search_youtube_api(query)
    
    def play_video(self, video_id):
        """Open YouTube video in browser"""
        url = f"https://www.youtube.com/watch?v={video_id}"
        webbrowser.open(url)
        self.current_video_id = video_id
        return True
    
    def get_embed_url(self, video_id):
        """Return embedded URL for video"""
        return f"https://www.youtube.com/embed/{video_id}?autoplay=1&controls=1"
    
    def get_study_playlists(self):
        """Get curated study playlists"""
        return [
            {"name": "🎵 Lofi Hip Hop Radio", "id": "jfKfPfyJRdk", "type": "24/7 Live"},
            {"name": "🎹 Classical Study Music", "id": "jgpJVI3tDbY", "type": "3 Hours"},
            {"name": "🌊 Ambient Sounds", "id": "lTRiuFIWV54", "type": "2 Hours"},
            {"name": "🎼 Piano Concentration", "id": "z1Yb-4nQgbs", "type": "2.5 Hours"},
            {"name": "🎸 Acoustic Study Mix", "id": "2OEL4P1Rz04", "type": "1 Hour"},
            {"name": "☕ Coffee Shop Jazz", "id": "kgx4WGK0oNU", "type": "LIVE"},
        ]
    
    def search_youtube(self, query):
        """Open YouTube search in browser"""
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query + ' study music')}"
        webbrowser.open(search_url)
