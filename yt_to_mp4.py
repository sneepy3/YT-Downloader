import pytube
import os
from moviepy.editor import VideoFileClip


# Festlegen von Download Pfad
dest_path = input("Download-Pfad (\"here\" für Programm-Pfad): ")

# bei here, current working directory
if dest_path.startswith("here"):
    dest_path = os.getcwd()

# Download-Pfad wird ausgegeben
print("Download-Pfad: " + dest_path + "\n")

# Anleitung
print("Links nacheinander eingeben! \nWenn der Dateiname nicht der Videoname sein soll, den gewünschen Dateinamen mit Leerzeichen getrennt nach dem Link angeben\n"+
      "Am Schluss \"end\" eingeben, dann erfolgt der Download")

# Liste der Video-LInks
videos = {}

def get_valid_filename(filename):
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

    b = valid_name.encode("latin-1", errors="ignore")
    valid_name = b.decode("latin-1")

    return valid_name

# Eingabe der YT-Links
while True:
    inputString = input("YT Link: ").strip()

    # Wenn der Download starten soll,
    if inputString == "end":
        break
    else:
        information = inputString.split(" ")

        # wenn ein Dateiname angegeben wurde,
        if len(information) > 1:
            videos[information[0]] = " ".join(information[1:])
        else:
            videos[inputString] = ""

# Audio der Videos wird nacheinander heruntergeladen
for video_link in videos:
    try:
        # Youtube Video object
        yt_video = pytube.YouTube(video_link)

        # Dateiname
        filename = get_valid_filename(videos[video_link])

        # Wenn kein Name angegeben wurde.
        if not filename:
            # wird der Videotitel genommen
            filename = get_valid_filename(yt_video.title)

        # Audiostreams
        video_streams = yt_video.streams.filter()

        # Audiospur download als mp4
        filepath = video_streams[0].download(dest_path, skip_existing=False, filename=filename)

        print(video_link + " gespeichert als " + filename + ".mp4")

    except Exception as e:
        print("Download von " + video_link + " fehlgeschlagen\n" + str(e))



