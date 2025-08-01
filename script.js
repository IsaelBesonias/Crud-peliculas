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

  item.innerHTML = `
    <strong>${movie.title}</strong> - ${movie.director} (${movie.year})
    <button class="delete-button">Eliminar</button>
  `;

  // Agregar evento al botón de eliminar
  item.querySelector(".delete-button").addEventListener("click", function () {
    list.removeChild(item);
  });

  list.appendChild(item);
}
