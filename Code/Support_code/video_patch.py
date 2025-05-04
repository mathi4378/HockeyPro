from moviepy.editor import VideoFileClip, concatenate_videoclips

# Lade deine Videodateien
clip1 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\A1.mp4")
clip2 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\A3.mp4")
clip3 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\A5.mp4")
clip4 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\A7.mp4")
clip5 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\A9.mp4")

clip6 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\C1.mp4")
clip7 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\C3.mp4")
clip8= VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\C5.mp4")
clip9 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\C7.mp4")
clip10 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\C9.mp4")

clip11 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\E1.mp4")
clip12 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\E3.mp4")
clip13 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\E5.mp4")
clip14 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\E7.mp4")
clip15 = VideoFileClip("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment 2\\E9.mp4")

# Füge sie zusammen
final_clip = concatenate_videoclips([clip1, clip2, clip3,clip4,clip5,clip6,clip7,clip8,clip9,clip10,clip11,clip12,clip13,clip14,clip15])

# Speichere das Ergebnis
final_clip.write_videofile("Experiment_1.mp4", codec="libx264", audio_codec="aac")
