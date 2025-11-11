import tkinter as tk
from tkinter import messagebox, filedialog
from threading import Thread
import yt_dlp
import os


class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        root.title("4K YouTube Downloader")
        root.geometry("500x350")
        root.resizable(False, False)

        # Title
        tk.Label(root, text="4K YouTube Downloader", font=("Arial", 16, "bold")).pack(
            pady=10
        )

        # URL input
        self.url_label = tk.Label(root, text="Enter YouTube URL:")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        # Quality selection
        self.quality_var = tk.StringVar(value="best")
        self.quality_label = tk.Label(root, text="Select Quality:")
        self.quality_label.pack(pady=5)
        self.quality_menu = tk.OptionMenu(
            root,
            self.quality_var,
            "2160p",
            "1440p",
            "1080p",
            "720p",
            "480p",
            "360p",
            "best",
        )
        self.quality_menu.pack(pady=5)

        # Download folder
        tk.Button(root, text="Choose Download Folder", command=self.choose_folder).pack(
            pady=5
        )
        self.path_label = tk.Label(root, text="No folder selected", fg="gray")
        self.path_label.pack()

        # Download button
        self.download_button = tk.Button(
            root,
            text="Download",
            command=self.start_download_thread,
            bg="green",
            fg="white",
        )
        self.download_button.pack(pady=10)

        # Progress label
        self.progress_label = tk.Label(root, text="", fg="blue")
        self.progress_label.pack()

        self.download_path = ""

    def choose_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.download_path = path
            self.path_label.config(text=path, fg="black")

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        if not self.download_path:
            messagebox.showerror("Error", "Please select a download folder")
            return

        # Disable button immediately and clear URL
        self.download_button.config(state="disabled")
        self.url_entry.delete(0, tk.END)

        Thread(target=self.download_video, args=(url,)).start()

    def download_video(self, url):
        quality = self.quality_var.get()

        def progress_hook(d):
            if d["status"] == "downloading":
                downloaded = d.get("downloaded_bytes", 0)
                total = d.get("total_bytes") or d.get("total_bytes_estimate")
                speed = d.get("speed", 0)

                downloaded_mb = downloaded / (1024 * 1024)
                speed_mb = speed / (1024 * 1024) if speed else 0

                if total:
                    pct = round(downloaded / total * 100, 1)
                    size_gb = round(total / (1024**3), 2)
                    self.progress_label.config(
                        text=f"{pct}% of {size_gb} GB at {speed_mb:.2f} MB/s"
                    )
                else:
                    self.progress_label.config(
                        text=f"{downloaded_mb:.2f} MB downloaded at {speed_mb:.2f} MB/s"
                    )
            elif d["status"] == "finished":
                self.progress_label.config(text="Download completed!")

        ydl_opts = {
            "format": (
                f"bestvideo[height<={quality.replace('p','')}]+bestaudio/best"
                if quality != "best"
                else "best"
            ),
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(self.download_path, "%(title)s.%(ext)s"),
            "ffmpeg_location": r"C:\ffmpeg\bin",
            "ffprobe_location": r"C:\ffmpeg\bin",
            "progress_hooks": [progress_hook],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "Download Finished!")
        except Exception as e:
            self.progress_label.config(text="Error during download.")
            messagebox.showerror("Error", str(e))
        finally:
            # Enable button after download finishes
            self.download_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
