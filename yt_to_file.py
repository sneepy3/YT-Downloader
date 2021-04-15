import pytube
import threading
import os
import time
from moviepy.editor import AudioFileClip, VideoFileClip
from youtube_video import Youtube_Video

# Downloadpfad
dest_path = ""

# Liste der zu herunterladenden Videos
videos = []

# Threads
threads = []


def instruction():
    global dest_path

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

# Eingabe der YT-Links
def start_link_input():
    while True:
        # Eingabe des Links
        inputString = input("YT Link: ").strip()

        # Wenn der Download starten soll,
        if inputString == "end":
            break
        elif inputString != "":
            informations = inputString.split(" ")
            
            file_format = "mp3"
            start_time = "0"
            end_time = "0"
            link = informations[0]
            filename = ""
			
            for i in range(len(informations)):
				# Wenn es sich um einen Parameter handelt
                if informations[i].startswith("-"):
                    # Parametername
                    param_name = informations[i][1]

                    # Parameter
                    param = informations[i+1]

                    # Dateiformat
                    if param_name == "f":
                        file_format = param

                    # Startzeit des Downloads in Min:Sek
                    elif param_name == "s":
                        start_time = param
                    
                    # Endzeit des Downloads
                    elif param_name == "e":
                        end_time = param

                    # Dateiname
                    elif param_name == "n":
                        filename = param

            # fügt video der Liste hinzu
            def add_video_to_list():
                # YoutubeVideo Objekt wird erstellt
                youtube_video = Youtube_Video(link=link, filename=filename, file_format=file_format, start_time=start_time, end_time=end_time)

                # Video wird zur Liste hinzugefügt
                videos.append(youtube_video)

            thread = threading.Thread(target=add_video_to_list)
            thread.start()
            threads.append(thread)


def dowload_videos():
    # Warten, bis alle Videos hinzugefügt wurden
    for thread in threads:
        try:
            thread.join()
        except:
            pass

    # Videos werden nacheinander heruntergeladen
    for video in videos:
        try:
            # wenn nur die Audio gespeichert werden soll,
            if video.file_format == "mp3":

                # Audiostreams
                audio_streams = video.pytube_video.streams.filter(only_audio=True)

                # Audiospur download als mp4
                filepath = audio_streams[0].download(os.getcwd(), skip_existing=False)

                # Konvertieren in mp3 und an gewünschtem Speicherort speichern
                audio = AudioFileClip(filepath).subclip(video.start_time, video.end_time)
                audio.write_audiofile(os.path.join(dest_path, video.filename + ".mp3"))

                audio.reader.__del__()

                # mp4 Datei wird gelöscht
                os.remove(filepath)

                print(video.pytube_video.title + " gespeichert als " + video.filename + ".mp3")

            # wenn das Video gespeichert werden soll
            elif video.file_format == "mp4":
                # Videostreams
                video_streams = video.pytube_video.streams.filter()
              
                # mp4 Download an gewünschten speicherort
                filepath = video_streams.get_highest_resolution().download(dest_path, skip_existing=False, filename=video.filename + "(old)")

                # Wenn nicht das ganze Video heruntergeladen werden soll,
                if video.start_time != 0 or video.end_time != video.pytube_video.length:
                    # gewünschter Videoausschnitt wird erstellt
                    videoclip = VideoFileClip(filepath).subclip(video.start_time, video.end_time)
                    
                    # Videoclip wird am gewünschten Speicherort gespeichert
                    videoclip.write_videofile(os.path.join(dest_path, video.filename + ".mp4"))
                    videoclip.reader.close()

                    # ursprüngliches komplettes Video wird gelöscht
                    os.remove(filepath)

                print(video.pytube_video.title + " gespeichert als " + video.filename + ".mp4")
        except Exception as e:
            print("Download von " + video.filename + " fehlgeschlagen\n" + str(e))


def main():
    while True:
        instruction()
        start_link_input()
        dowload_videos()

        videos.clear()

main()