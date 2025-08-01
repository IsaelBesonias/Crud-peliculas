document.getElementById("movie-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const title = document.getElementById("title").value;
  const director = document.getElementById("director").value;
  const year = document.getElementById("year").value;

  const movie = {
    title,
    director,
    year
  };

  addMovieToList(movie);
  this.reset(); 
});

function addMovieToList(movie) {
  const list = document.getElementById("movie-list");
  const item = document.createElement("li");

  item.textContent = `${movie.title} - ${movie.director} (${movie.year})`;

  list.appendChild(item);
}
