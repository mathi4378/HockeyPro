from moviepy.editor import VideoFileClip

# Pfade für Eingabe und Ausgabe
input_path = "E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\Experiment2.mp4"
output_path = "E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\Experiment2.mov"

# Video laden und als .mp4 speichern
video_clip = VideoFileClip(input_path)
video_clip.write_videofile(output_path, codec="libx264")
video_clip.close()

output_path
