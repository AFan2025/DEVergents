document.addEventListener('DOMContentLoaded', function () {
    var optionBox = document.querySelector('.option-box');
    var label = document.getElementById('option-label');
    var resultsList = document.getElementById('results-list');
    var themePairs = [
        ['Day', 'Night'],
        ['Chill', 'Party'],
        ['Sad', 'Happy'],
        ['Car', 'Run'],
        ['Fire', 'Ice'],
        ['Mountain', 'Beach'],
        ['Cat', 'Dog'],
        ['Coffee', 'Tea'],
        ['Sun', 'Moon'],
        ['Morning', 'Evening']
    ];
    var currentIndex = 0;

    var hammer = new Hammer(optionBox);

    hammer.get('swipe').set({ direction: Hammer.DIRECTION_ALL });

    function updateLabels() {
        if (currentIndex < themePairs.length) {
            document.getElementById('option1').textContent = themePairs[currentIndex][0];
            document.getElementById('option2').textContent = themePairs[currentIndex][1];
            label.textContent = '';
        } else {
            label.innerHTML = '<a href="#search" class="text-white" style="font-size: 2.5rem;">Pick New Song</a>';
            document.getElementById('option1').textContent = '';
            document.getElementById('option2').textContent = '';
            document.getElementById('both').style.display = 'none';
            document.getElementById('neither').style.display = 'none';
        }
    }

    function addResult(chosen1, chosen2, bothChosen, neitherChosen) {
        var li = document.createElement('li');
        if (bothChosen) {
            li.innerHTML = `<span class="chosen">${chosen1}</span> vs. <span class="chosen">${chosen2}</span>`;
        } else if (neitherChosen) {
            li.innerHTML = `<span class="not-chosen">${chosen1}</span> vs. <span class="not-chosen">${chosen2}</span>`;
        } else {
            li.innerHTML = `<span class="chosen">${chosen1}</span> vs. <span class="not-chosen">${chosen2}</span>`;
        }
        resultsList.appendChild(li);
    }

    hammer.on('swipeleft', function () {
        if (currentIndex < themePairs.length) {
            var chosen = themePairs[currentIndex][0];
            var notChosen = themePairs[currentIndex][1];
            addResult(chosen, notChosen, false, false);
            currentIndex++;
            updateLabels();
        }
    });

    hammer.on('swiperight', function () {
        if (currentIndex < themePairs.length) {
            var chosen = themePairs[currentIndex][1];
            var notChosen = themePairs[currentIndex][0];
            addResult(chosen, notChosen, false, false);
            currentIndex++;
            updateLabels();
        }
    });

    hammer.on('swipeup', function () {
        if (currentIndex < themePairs.length) {
            var chosen1 = themePairs[currentIndex][0];
            var chosen2 = themePairs[currentIndex][1];
            addResult(chosen1, chosen2, true, false);
            currentIndex++;
            updateLabels();
        }
    });

    hammer.on('swipedown', function () {
        if (currentIndex < themePairs.length) {
            var notChosen1 = themePairs[currentIndex][0];
            var notChosen2 = themePairs[currentIndex][1];
            addResult(notChosen1, notChosen2, false, true);
            currentIndex++;
            updateLabels();
        }
    });

    updateLabels();
});

var currentSong = null;

var songs = [
    { title: 'Firework', artist: 'Katy Perry', cover: 'KatyPerry.jpeg' },
    { title: 'Teenage Dream', artist: 'Katy Perry', cover: 'KatyPerry.jpeg' },
    { title: 'Classify Rocks', artist: 'Olivia and Margaux', cover: 'album.jpg' }
];

function showSuggestions() {
    var searchInput = document.getElementById('search-input').value.toLowerCase();
    var suggestions = document.getElementById('suggestions');
    suggestions.innerHTML = '';

    if (searchInput === '') {
        suggestions.style.display = 'none';
        return;
    }

    var foundSongs = [];

    songs.forEach(song => {
        if (song.title.toLowerCase().includes(searchInput) || song.artist.toLowerCase().includes(searchInput)) {
            foundSongs.push(song);
        }
    });

    if (foundSongs.length > 0) {
        foundSongs.forEach(song => {
            var suggestion = document.createElement('a');
            suggestion.className = 'list-group-item list-group-item-action';
            suggestion.textContent = `${song.title} by ${song.artist}`;
            suggestion.onclick = function() {
                document.getElementById('search-input').value = song.title;
                searchMusic();
                suggestions.innerHTML = '';
                suggestions.style.display = 'none';
            };
            suggestions.appendChild(suggestion);
        });
        suggestions.style.display = 'block';
    } else {
        suggestions.style.display = 'none';
    }
}

function searchMusic() {
    var searchInput = document.getElementById('search-input').value.toLowerCase();
    var results = document.getElementById('results');
    var foundSongs = [];

    if (searchInput === '') {
        results.innerHTML = 'Please enter a song or artist.';
        document.getElementById('song-details').classList.add('d-none');
        return;
    }

    songs.forEach(song => {
        if (song.title.toLowerCase() === searchInput || song.artist.toLowerCase() === searchInput) {
            foundSongs.push(song);
        } else if (song.artist.toLowerCase().includes(searchInput)) {
            foundSongs.push(song);
        }
    });

    if (foundSongs.length > 0) {
        if (foundSongs.length === 1) {
            displaySongDetails(foundSongs[0].title, foundSongs[0].artist, foundSongs[0].cover);
        } else {
            results.innerHTML = '<h3>Choose a song:</h3>';
            foundSongs.forEach(song => {
                var button = document.createElement('button');
                button.className = 'btn btn-link';
                button.textContent = song.title;
                button.onclick = function() {
                    displaySongDetails(song.title, song.artist, song.cover);
                };
                results.appendChild(button);
            });
            document.getElementById('song-details').classList.add('d-none');
        }
    } else {
        results.innerHTML = 'No results found.';
        document.getElementById('song-details').classList.add('d-none');
    }
}

function generateRandomSong() {
    var randomSong = songs[Math.floor(Math.random() * songs.length)];
    displaySongDetails(randomSong.title, randomSong.artist, randomSong.cover);
}

function displaySongDetails(title, artist, cover) {
    var albumCover = document.getElementById('album-cover');
    var songTitle = document.getElementById('song-title');
    var artistName = document.getElementById('artist-name');

    albumCover.src = cover;
    songTitle.textContent = title;
    artistName.textContent = artist;

    document.getElementById('song-details').classList.remove('d-none');
    document.getElementById('results').innerHTML = ''; // Clear previous results

    currentSong = title; // Store current song title

    // Update option box background image
    var optionBox = document.getElementById('option-box');
    optionBox.style.backgroundImage = `url(${cover})`;
    optionBox.onclick = function() {
        updateRankRateSection();
    };

    // Set label colors based on the background image
    setLabelColorsBasedOnBackground(cover);
}

function updateRankRateSection() {
    if (currentSong) {
        document.getElementById('rank-rate-title').textContent = `Rank/Rate: ${currentSong}`;
        document.getElementById('song-title-display').textContent = currentSong;

        // Reset the rank-rate section if necessary
        var resultsList = document.getElementById('results-list');
        resultsList.innerHTML = ''; // Clear the previous results
        // Reset options if needed
        currentIndex = 0;
        updateLabels();

        // Set label colors based on the background image
        setLabelColorsBasedOnBackground(document.getElementById('album-cover').src);

        // Ensure the background image is correctly set
        var optionBox = document.getElementById('option-box');
        optionBox.style.backgroundImage = `url(${document.getElementById('album-cover').src})`;
    }
}

function setLabelColorsBasedOnBackground(imageSrc) {
    var img = new Image();
    img.src = imageSrc;

    img.onload = function() {
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        canvas.width = img.width;
        canvas.height = img.height;
        context.drawImage(img, 0, 0, img.width, img.height);

        // Get the image data
        var imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        var data = imageData.data;

        // Analyze the colors in the image
        var colorSum = 0;
        var r, g, b, avg;

        for (var x = 0, len = data.length; x < len; x += 4) {
            r = data[x];
            g = data[x + 1];
            b = data[x + 2];
            avg = Math.floor((r + g + b) / 3);
            colorSum += avg;
        }

        var brightness = Math.floor(colorSum / (img.width * img.height));

        // Set label color based on the average brightness
        var labelColor = brightness > 128 ? 'black' : 'white';
        var labels = document.querySelectorAll('.option-box .label');
        labels.forEach(function(label) {
            label.style.color = labelColor;
        });
    };
}