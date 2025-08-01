let movieList = [];
let editingItem = null;

function saveToLocalStorage() {
  localStorage.setItem("movies", JSON.stringify(movieList));
}

function renderMovieList() {
  const list = document.getElementById("movie-list");
  const searchTerm = document.getElementById("search")?.value?.toLowerCase() || "";
  list.innerHTML = "";

  movieList.forEach((movie, index) => {
    if (movie.title.toLowerCase().includes(searchTerm)) {
      addMovieToList(movie, index);
    }
  });
}

function addMovieToList(movie, index) {
  const list = document.getElementById("movie-list");
  const item = document.createElement("li");

  item.innerHTML = `
    <div style="display: flex; align-items: center;">
      <img src="${movie.image}" alt="Poster" style="height: 100px; margin-right: 10px;">
      <div>
        <strong>${movie.title}</strong> - ${movie.director} (${movie.year})<br>
        <button class="edit-button">Editar</button>
        <button class="delete-button">Eliminar</button>
      </div>
    </div>
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
    document.getElementById("image").value = movie.image;

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
  const image = document.getElementById("image").value;

  const movie = { title, director, year, image };

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

const searchInput = document.getElementById("search");
if (searchInput) {
  searchInput.addEventListener("input", renderMovieList);
}
