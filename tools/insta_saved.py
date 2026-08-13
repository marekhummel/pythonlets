from getpass import getpass
from glob import glob
from os import environ
from sqlite3 import OperationalError, connect
from types import MethodType

import instaloader as il


def login(loader):
    username = input("Instagram username: ").strip()
    password = getpass("Instagram password: ")
    loader.login(username, password)
    return username


def import_session(loader):
    """Optional Firefox cookie import."""

    windows_user = environ.get("USERNAME") or environ.get("USER")
    if not windows_user:
        raise SystemExit("Set FIREFOX_COOKIEFILE or ensure USERNAME/USER is available.")
    default_cookiefile = (
        f"/mnt/c/Users/{windows_user}/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite"
    )
    cookiefile = glob(default_cookiefile)[0]

    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        try:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
            )
        except OperationalError:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
            )
        loader.context._session.cookies.update(cookie_data)
    finally:
        conn.close()

    username = loader.test_login()
    if not username:
        raise SystemExit("Firefox cookies do not contain a valid Instagram login.")
    loader.context.username = username
    return username


def use_authenticated_media_requests(loader):
    """Download media with the logged-in session instead of Instaloader's anonymous one."""

    def get_raw_authenticated(context, url, _attempt=1):
        resp = context._session.get(
            url,
            stream=True,
            headers={"Referer": "https://www.instagram.com/"},
        )
        if resp.status_code == 200:
            resp.raw.decode_content = True
            return resp
        if resp.status_code == 403:
            raise il.QueryReturnedForbiddenException(context._response_error(resp))
        if resp.status_code == 404:
            raise il.QueryReturnedNotFoundException(context._response_error(resp))
        raise il.ConnectionException(context._response_error(resp))

    loader.context.get_raw = MethodType(get_raw_authenticated, loader.context)


loader = il.Instaloader(  # type: ignore
    download_video_thumbnails=False,
    save_metadata=False,
    filename_pattern="{date_utc}",
    post_metadata_txt_pattern="",
    max_connection_attempts=1,
    dirname_pattern="_out/instagram/",
    resume_prefix=None,
)

# user = login(loader)
user = import_session(loader)
use_authenticated_media_requests(loader)

print(f"Authenticated as {loader.test_login()}.")
loader.download_saved_posts()
