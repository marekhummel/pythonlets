import argparse

from downloader import download_playlist, download_video


if __name__ == '__main__':
    # sys.argv.append('-p')
    # sys.argv.append('PLhlJzNE93TpbeOEXwji2SWu62wMmifFJI')
    # sys.argv.append('-i')
    # sys.argv.append(r'Integrieren|Koordinatensysteme')
    # sys.argv.append('-o')
    # sys.argv.append(r'.')

    parser = argparse.ArgumentParser(description='YouTube Downloader')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--playlist', type=str)
    group.add_argument('-v', '--video', type=str)
    parser.add_argument('-i', '--ignore', type=str, default='(?!)')
    parser.add_argument('-o', '--output', type=str)

    args = parser.parse_args()

    if args.video:
        uri = f'https://www.youtube.com/watch?v={args.video}'
        target = args.output if args.output else './out/'
        download_video(uri, target)
        print('File downloaded.')
    elif args.playlist:
        uri = f'https://www.youtube.com/playlist?list={args.playlist}'
        target = args.output if args.output else f'./out/{args.playlist}'
        download_playlist(uri, target, args.ignore)
        print('\r\nFile(s) downloaded.\r\nDone.')
