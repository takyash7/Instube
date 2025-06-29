import streamlit as st
import yt_dlp
import instaloader
import os
import shutil

# Folders
if not os.path.exists("downloads"):
    os.makedirs("downloads")
if not os.path.exists("temp"):
    os.makedirs("temp")

st.set_page_config(page_title="Downloader", page_icon="📥")
st.title("📥 YouTube & Instagram Reels Downloader")

url = st.text_input("Paste YouTube or Instagram Reel URL 👇")

if st.button("Download"):
    if url:
        try:
            if "youtube.com" in url or "youtu.be" in url:
                if "shorts" in url or "youtu.be" in url:
                    video_id = url.split("/")[-1].split("?")[0]
                    url = f"https://www.youtube.com/watch?v={video_id}"
                if "watch?v=" in url:
                    url = url.split("&")[0].split("?si=")[0]

                ffmpeg_path = "C:/Users/BC/Desktop/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"

                status_placeholder = st.empty()
                progress_bar = st.progress(0)

                def progress_hook(d):
                    if d['status'] == 'downloading':
                        percent = d.get("_percent_str", "0.0%").strip()
                        speed = d.get("_speed_str", "0.0 KiB/s")
                        eta = d.get("eta", 0)
                        status_placeholder.info(f"📥 Downloading: {percent} at {speed} | ETA: {eta}s")
                        try:
                            progress = float(percent.replace('%', '').strip()) / 100.0
                            progress_bar.progress(min(progress, 1.0))
                        except:
                            pass
                    elif d['status'] == 'finished':
                        status_placeholder.success("✅ Download complete. Processing...")

                # Save to temporary folder first
                temp_folder = "temp"

                ydl_opts = {
                    'outtmpl': f'{temp_folder}/%(title)s.%(ext)s',
                    'format': 'bestvideo+bestaudio/best',
                    'ffmpeg_location': ffmpeg_path,
                    'merge_output_format': 'mp4',
                    'progress_hooks': [progress_hook],
                    'noplaylist': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'video')
                    filename = ydl.prepare_filename(info).replace(".webm", ".mp4").replace(".mkv", ".mp4")

                    # Move safely
                    final_path = os.path.join("downloads", os.path.basename(filename))
                    shutil.move(filename, final_path)

                    st.success(f"🎉 Downloaded: {title}")
                    st.info(f"📂 Saved to: downloads/{os.path.basename(filename)}")

            elif "instagram.com/reel" in url:
                shortcode = url.rstrip("/").split("/")[-1].split("?")[0]
                L = instaloader.Instaloader()
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target="downloads")
                st.success("✅ Instagram Reel downloaded!")

            else:
                st.warning("⚠️ Please enter a valid YouTube or Instagram Reel URL.")

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please paste a URL first.")
