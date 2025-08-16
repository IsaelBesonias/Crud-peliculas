let movieList = [];
let editingItem = null;

const CREDENTIALS = {
  username: "Isael",
  password: "12345"
};

function checkLoginStatus() {
  const isLoggedIn = localStorage.getItem("loggedIn") === "true";
  document.getElementById("login-container").style.display = isLoggedIn ? "none" : "block";
  document.getElementById("app-container").style.display = isLoggedIn ? "block" : "none";

  if (isLoggedIn) renderMovieList();
}

document.getElementById("login-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const user = document.getElementById("login-user").value.trim();
  const pass = document.getElementById("login-pass").value.trim();

  if (user === CREDENTIALS.username && pass === CREDENTIALS.password) {
    localStorage.setItem("loggedIn", "true");
    checkLoginStatus();
  } else {
    alert("Credenciales incorrectas. Usuario: Isael / Contraseña: 12345");
  }
});

document.getElementById("logout").addEventListener("click", () => {
  localStorage.removeItem("loggedIn");
  location.reload();
});

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
      <img src="${movie.image}" alt="Poster" style="height: 100px; margin-right: 10px; border-radius: 5px;">
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
    document.getElementById("image-preview").src = movie.image;
    document.getElementById("image-preview").style.display = "block";

    editingItem = index;
    document.querySelector("button[type='submit']").textContent = "Actualizar Película";
  });

  list.appendChild(item);
}

document.getElementById("movie-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const title = document.getElementById("title").value.trim();
  const director = document.getElementById("director").value.trim();
  const year = parseInt(document.getElementById("year").value.trim());
  const image = document.getElementById("image").value.trim();

  const currentYear = new Date().getFullYear();

  if (!title || !director || !year || !image) {
    alert("Por favor, completa todos los campos.");
    return;
  }
  if (isNaN(year) || year < 1888 || year > currentYear) {
    alert(`Por favor, ingresa un año válido entre 1888 y ${currentYear}.`);
    return;
  }

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
  document.getElementById("image-preview").style.display = "none";
});

document.getElementById("image").addEventListener("input", function () {
  const url = this.value.trim();
  const preview = document.getElementById("image-preview");
  if (url) {
    preview.src = url;
    preview.style.display = "block";
  } else {
    preview.style.display = "none";
  }
});

window.addEventListener("load", () => {
  const storedMovies = localStorage.getItem("movies");
  if (storedMovies) {
    movieList = JSON.parse(storedMovies);
  }

  const yearInput = document.getElementById("year");
  if (yearInput) {
    yearInput.setAttribute("min", "1888");
    yearInput.setAttribute("max", new Date().getFullYear().toString());
  }

  checkLoginStatus();
});

const searchInput = document.getElementById("search");
if (searchInput) {
  searchInput.addEventListener("input", renderMovieList);
}

const clearBtn = document.getElementById("clear-all");
if (clearBtn) {
  clearBtn.addEventListener("click", () => {
    const confirmDelete = confirm("¿Estás seguro de que deseas eliminar todas las películas?");
    if (confirmDelete) {
      movieList = [];
      saveToLocalStorage();
      renderMovieList();
    }
  });
}
