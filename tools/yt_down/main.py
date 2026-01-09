import argparse
import sys

from downloader import download_playlist, download_video

if __name__ == "__main__":
    # sys.argv.append("-v")
    # sys.argv.append("1sM89qLmd9Y")
    sys.argv.append("-p")
    sys.argv.append("PLChB_B712tZg2clVHoZjEsikOS4BeVryE")
    # sys.argv.append('-i')
    # sys.argv.append(r'Integrieren|Koordinatensysteme')
    sys.argv.append("-o")
    sys.argv.append(r"./_out/yt/")
    sys.argv.append("-a")

    parser = argparse.ArgumentParser(description="YouTube Downloader")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--playlist", type=str)
    group.add_argument("-v", "--video", type=str)
    parser.add_argument("-i", "--ignore", type=str, default="(?!)")
    parser.add_argument("-o", "--output", type=str)
    parser.add_argument("-a", "--audio-only", action="store_true")

    args = parser.parse_args()
    print(args)

    if args.video:
        uri = f"https://www.youtube.com/watch?v={args.video}"
        target = args.output if args.output else "./_out/yt"
        download_video(uri, target, args.audio_only)
        print("File downloaded.")
    elif args.playlist:
        uri = f"https://www.youtube.com/playlist?list={args.playlist}"
        target = args.output if args.output else f"./_out/yt/{args.playlist}"
        download_playlist(uri, target, args.audio_only, args.ignore)
        print("\r\nFile(s) downloaded.\r\nDone.")
