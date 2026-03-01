try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
import threading

class VoiceCommandSystem:
    def __init__(self):
        if not VOICE_AVAILABLE:
            self.enabled = False
            return
        
        self.enabled = True
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.listening = False
        self.commands = {
            'start session': 'start_session',
            'stop session': 'stop_session',
            'take break': 'take_break',
            'show progress': 'show_progress',
            'show analytics': 'show_analytics',
            'show rewards': 'show_rewards'
        }
    
    def speak(self, text):
        """Text to speech"""
        if not self.enabled:
            return
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice commands"""
        if not self.enabled:
            return None
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio).lower()
                return command
        except:
            return None
    
    def process_command(self, command):
        """Process voice command"""
        for key, action in self.commands.items():
            if key in command:
                return action
        return None
    
    def start_listening(self, callback):
        """Start listening in background"""
        def listen_loop():
            self.listening = True
            while self.listening:
                command = self.listen()
                if command:
                    action = self.process_command(command)
                    if action and callback:
                        callback(action)
        
        thread = threading.Thread(target=listen_loop, daemon=True)
        thread.start()
    
    def stop_listening(self):
        """Stop listening"""
        self.listening = False
