import customtkinter as ctk
from pytube import YouTube


def stream_window_init():
    # Prevent invalid URL
    try:
        global yt_object
        global streams
        global streams_to_text

        yt_object = YouTube(url_input.get())
        streams = yt_object.streams.filter(type="video")
        streams_to_text = []

    except:
        url_input.delete(0, "end")
        return

    # Remove URL widgets
    url_window.place_forget()

    # Configure stream widgets
    stream_selector.set("Pick a Stream")
    stream_title.configure(text=yt_object.title)

    # Display as a formatted string
    for stream in streams:
        txt = "Resolution: {0}, FPS: {1}, Size: {2}mb"
        streams_to_text.insert(
            -1,
            txt.format(
                stream.resolution, stream.fps, round(stream.filesize / 1000000, 2)
            ),
        )
    stream_selector.configure(values=streams_to_text)
    stream_window.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)


def download_window_init():
    # Prevent null stream
    if stream_selector.get() == "Pick a Stream":
        return

    # Remove stream widgets
    stream_window.place_forget()

    # Insert download widgets
    download_window.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)


def download_video():
    # Find correct stream
    for i, stream in enumerate(streams_to_text):
        if stream == stream_selector.get():
            # Download the correct stream with file name chosen by user
            streams[i].download(filename=download_input.get() + ".mp4")
            break
    # End program
    window.destroy()


# Initialize window with styling
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
window = ctk.CTk()
window.title("YouTube Video Downloader")
window.geometry("480x288")

# URL widget setup
url_window = ctk.CTkFrame(master=window)
url_window.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

url_input = ctk.CTkEntry(master=url_window, placeholder_text="Enter a URL...")
url_input.pack(pady=16, padx=16)

url_button = ctk.CTkButton(master=url_window, text="Next", command=stream_window_init)
url_button.pack(pady=16, padx=16)

# Stream widget setup
stream_window = ctk.CTkFrame(master=window)

stream_title = ctk.CTkLabel(master=stream_window, text="placeholder", wraplength=150)
stream_title.pack(pady=16, padx=16)

stream_selector = ctk.CTkOptionMenu(master=stream_window)
stream_selector.pack(pady=16, padx=16)

stream_button = ctk.CTkButton(
    master=stream_window, text="Done", command=download_window_init
)
stream_button.pack(pady=16, padx=16)

# Download widget setup
download_window = ctk.CTkFrame(master=window)

download_input = ctk.CTkEntry(
    master=download_window, placeholder_text="Enter a File Name..."
)
download_input.pack(pady=16, padx=16)

download_button = ctk.CTkButton(
    master=download_window, text="Download", command=download_video
)
download_button.pack(pady=16, padx=16)


# Begin
window.mainloop()
