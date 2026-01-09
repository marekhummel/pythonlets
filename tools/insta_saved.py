from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect

import instaloader as il


def import_session(loader):
    """Sample code from instaloader docs"""
    # Find firefox cookies
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    cookiefile = glob(expanduser(default_cookiefile))[0]

    # Connect and find insta session
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )

    # Set session
    loader.context._session.cookies.update(cookie_data)
    username = loader.test_login()
    if not username:
        raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
    loader.context.username = username
    loader.save_session_to_file()

    return username


# Create instance
loader = il.Instaloader(  # type: ignore
    download_video_thumbnails=False,
    save_metadata=False,
    filename_pattern="{date_utc}",
    post_metadata_txt_pattern="",
    max_connection_attempts=1,
)

# Import session from firefox login
user = import_session(loader)

# Update path and download
loader.dirname_pattern = "_out/instagram/"
loader.download_saved_posts()  # post_filter=lambda item: item.date_utc > datetime(2022, 12, 3))
