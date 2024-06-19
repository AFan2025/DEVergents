let currentSongIndex = 0;
let classifiedSongs = [];

const songs = [
    { title: 'Song 1', artist: 'Artist 1', adjective: 'happy' },
    { title: 'Song 2', artist: 'Artist 2', adjective: 'sad' },
    // Add more songs here
];

function loadSong() {
    if (currentSongIndex >= songs.length) {
        document.getElementById('song-card').style.display = 'none';
        document.getElementById('suggestions').style.display = 'block';
        return;
    }

    const song = songs[currentSongIndex];
    document.getElementById('song-title').textContent = song.title;
    document.getElementById('song-artist').textContent = song.artist;
    document.getElementById('song-adjective').textContent = `Is this song ${song.adjective}?`;
}

function swipeLeft() {
    classifiedSongs.push({ ...songs[currentSongIndex], classified: false });
    currentSongIndex++;
    loadSong();
}

function swipeRight() {
    classifiedSongs.push({ ...songs[currentSongIndex], classified: true });
    currentSongIndex++;
    loadSong();
}

function suggestSongs() {
    const adjective = document.getElementById('adjective-input').value;
    const suggestions = classifiedSongs.filter(song => song.classified && song.adjective === adjective);
    const suggestedSongsDiv = document.getElementById('suggested-songs');
    suggestedSongsDiv.innerHTML = '';

    if (suggestions.length === 0) {
        suggestedSongsDiv.textContent = 'No suggestions available.';
        return;
    }

    suggestions.forEach(song => {
        const songElement = document.createElement('div');
        songElement.textContent = `${song.title} by ${song.artist}`;
        suggestedSongsDiv.appendChild(songElement);
    });
}

window.onload = loadSong;
