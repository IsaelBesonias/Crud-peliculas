let movieList = [];
let editingItem = null;

function saveToLocalStorage() {
  localStorage.setItem("movies", JSON.stringify(movieList));
}

function renderMovieList() {
  const list = document.getElementById("movie-list");
  list.innerHTML = "";
  movieList.forEach((movie, index) => {
    addMovieToList(movie, index);
  });
}

function addMovieToList(movie, index) {
  const list = document.getElementById("movie-list");
  const item = document.createElement("li");

  item.innerHTML = `
    <strong>${movie.title}</strong> - ${movie.director} (${movie.year})
    <button class="edit-button">Editar</button>
    <button class="delete-button">Eliminar</button>
  `;

  item.querySelector(".delete-button").addEventListener("click", function () {
    movieList.splice(index, 1);
    saveToLocalStorage();
    renderMovieList();
  });

  item.querySelector(".edit-button").addEventListener("click", function () {
    document.getElementById("title").value = movie.title;
    document.getElementById("director").value = movie.director;
    document.getElementById("year").value = movie.year;
    editingItem = index;
    document.querySelector("button[type='submit']").textContent = "Actualizar Película";
  });

  list.appendChild(item);
}


document.getElementById("movie-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const title = document.getElementById("title").value;
  const director = document.getElementById("director").value;
  const year = document.getElementById("year").value;

  const movie = { title, director, year };

  if (editingItem !== null) {
    movieList[editingItem] = movie;
    editingItem = null;
    document.querySelector("button[type='submit']").textContent = "Agregar Película";
  } else {
    movieList.push(movie);
  }

  saveToLocalStorage();
  renderMovieList();
  this.reset();
});

window.addEventListener("load", () => {
  const storedMovies = localStorage.getItem("movies");
  if (storedMovies) {
    movieList = JSON.parse(storedMovies);
    renderMovieList();
  }
});
