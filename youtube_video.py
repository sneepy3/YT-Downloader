import pytube

class Youtube_Video:
    def __init__(self, link, filename, file_format="mp3", start_time="0", end_time="0"):
        # Videolink
        self.pytube_video = pytube.YouTube(link)
        
        # Dateiname
        self.filename = self.get_valid_filename(filename)

        if filename == "":
            self.filename = self.get_valid_filename(self.pytube_video.title)

        # Dateiformat
        self.file_format = file_format
        
        # Startzeit des Downloads
        self.start_time = self.get_videotime_in_seconds(start_time)
        
        # Endzeit des Downloads
        self.end_time = self.get_videotime_in_seconds(end_time)

        if self.end_time == 0:
            self.end_time = self.pytube_video.length

    # gibt Sekundenzeit von einem timestring im format min:sec zurück
    def get_videotime_in_seconds(self, timestring):
        times = timestring.split(":")

        if len(times) <= 1:
            return 0

        # Minute
        minutes = int(times[0])

        # Sekunde
        seconds = int(times[1])

        # Sekundenzeit
        return minutes*60 + seconds

    def get_valid_filename(self, filename):
        # ungültige Zeichen werden entfernt
        valid_name = filename.replace("*", "")\
            .replace("\"", "")\
            .replace("/", "")\
            .replace("\\", "")\
            .replace(":", "")\
            .replace(">", "")\
            .replace("<", "")\
            .replace("?", "")\
            .replace("*", "")\
            .replace("|", "")

        # nicht Latin-1 zeichen werden entfernt
        b = valid_name.encode("latin-1", errors="ignore")
        valid_name = b.decode("latin-1")

        return valid_name