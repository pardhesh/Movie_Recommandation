document.getElementById("movie-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    let movieName = document.getElementById("movie-name").value;
    
    let response = await fetch("/recommend?movie=" + encodeURIComponent(movieName));
    let data = await response.json();

    let recommendationsContainer = document.getElementById("recommendations-container");
    recommendationsContainer.innerHTML = "";

    if (data.recommendations.length > 0) {
        data.recommendations.forEach(movie => {
            let movieCard = document.createElement("div");
            movieCard.classList.add("movie-card");

            let movieImage = document.createElement("img");
            movieImage.src = `https://via.placeholder.com/200x300?text=${movie}`; // Placeholder, replace with actual API
            movieImage.alt = movie;

            let movieTitle = document.createElement("p");
            movieTitle.textContent = movie;

            movieCard.appendChild(movieImage);
            movieCard.appendChild(movieTitle);
            recommendationsContainer.appendChild(movieCard);
        });
    } else {
        recommendationsContainer.innerHTML = "<p>No recommendations found.</p>";
    }
});
