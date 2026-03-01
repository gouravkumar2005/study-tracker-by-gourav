import os
import platform

class WebsiteBlocker:
    def __init__(self):
        self.hosts_path = self._get_hosts_path()
        self.redirect_ip = "127.0.0.1"
        self.blocked_sites = []
        
    def _get_hosts_path(self):
        if platform.system() == "Windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        else:
            return "/etc/hosts"
    
    def block_websites(self, websites):
        """Block list of websites"""
        try:
            with open(self.hosts_path, 'r+') as file:
                content = file.read()
                file.seek(0, 2)  # Move to end
                
                if "# Study Tracker Blocks" not in content:
                    file.write("\n# Study Tracker Blocks\n")
                
                for website in websites:
                    if website not in content:
                        file.write(f"{self.redirect_ip} {website}\n")
                        file.write(f"{self.redirect_ip} www.{website}\n")
                        self.blocked_sites.append(website)
            
            self._flush_dns()
            return True
        except PermissionError:
            return False
    
    def unblock_websites(self):
        """Unblock all websites"""
        try:
            with open(self.hosts_path, 'r') as file:
                lines = file.readlines()
            
            with open(self.hosts_path, 'w') as file:
                skip = False
                for line in lines:
                    if "# Study Tracker Blocks" in line:
                        skip = True
                    elif skip and line.strip() == "":
                        skip = False
                    
                    if not skip:
                        file.write(line)
            
            self._flush_dns()
            return True
        except PermissionError:
            return False
    
    def _flush_dns(self):
        """Flush DNS cache"""
        if platform.system() == "Windows":
            os.system("ipconfig /flushdns > nul 2>&1")
        else:
            os.system("sudo systemd-resolve --flush-caches > /dev/null 2>&1")
    
    def get_default_blocked_sites(self):
        """Get default list of distracting websites"""
        return [
            "facebook.com", "instagram.com", "twitter.com", "tiktok.com",
            "youtube.com", "netflix.com", "reddit.com", "snapchat.com",
            "twitch.tv", "discord.com", "whatsapp.com", "telegram.org"
        ]
