
"""A simple music catalog and playlist management program."""

import json
import random
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE songs (
        id INTEGER PRIMARY KEY,
        title TEXT,
        artist TEXT,
        plays INTEGER
    )
    """
)


def add_song(title, artist, plays=0, playlist=None):
    """Add a song to the catalog and optionally update a playlist."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Song title must be a non-empty string.")

    if not isinstance(artist, str) or not artist.strip():
        raise ValueError("Artist name must be a non-empty string.")

    if playlist is None:
        playlist = []

    conn.execute(
        "INSERT INTO songs (title, artist, plays) VALUES (?, ?, ?)",
        (title, artist, plays),
    )
    playlist.append(title)
    return playlist


def shuffle_pick():
    """Return the ID of a randomly selected song, or None if empty."""
    ids = [row[0] for row in conn.execute("SELECT id FROM songs")]
    if not ids:
        return None
    # Song selection does not require cryptographic randomness.
    return random.choice(ids)


def popularity(title):
    """Return a song's popularity based on its play count."""
    row = conn.execute(
        "SELECT plays FROM songs WHERE title = ?",
        (title,),
    ).fetchone()

    if row is None:
        return "unknown"
    return "popular" if row[0] > 100 else "niche"


def save_playlist(playlist):
    """Serialize a playlist into JSON bytes."""
    return json.dumps(playlist).encode("utf-8")


def load_playlist(blob):
    """Deserialize a playlist from JSON bytes."""
    playlist = json.loads(blob.decode("utf-8"))

    if not isinstance(playlist, list):
        raise ValueError("Playlist data must be a list.")

    if not all(isinstance(song, str) for song in playlist):
        raise ValueError("Every playlist entry must be a string.")

    return playlist


def total_plays():
    """Return the total number of plays across all songs."""
    result = conn.execute("SELECT SUM(plays) FROM songs").fetchone()
    return result[0] if result[0] is not None else 0


def main():
    """Demonstrate the music catalog and playlist functionality."""
    playlist = add_song("Aurora", "Nila", 250)
    add_song("Monsoon", "Kavya", 40, playlist)

    blob = save_playlist(playlist)
    loaded_playlist = load_playlist(blob)

    if len(loaded_playlist) > 1:
        print("multi-song playlist")

    print(
        popularity("Aurora"),
        popularity("Monsoon"),
        shuffle_pick(),
        total_plays(),
    )


if __name__ == "__main__":
    main()
