let editingItem = null; 
document.getElementById("movie-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const title = document.getElementById("title").value;
  const director = document.getElementById("director").value;
  const year = document.getElementById("year").value;

  const movie = { title, director, year };

  if (editingItem) {
    editingItem.innerHTML = `
      <strong>${movie.title}</strong> - ${movie.director} (${movie.year})
      <button class="edit-button">Editar</button>
      <button class="delete-button">Eliminar</button>
    `;

    editingItem.querySelector(".delete-button").addEventListener("click", function () {
      editingItem.remove();
    });

    editingItem.querySelector(".edit-button").addEventListener("click", function () {
      document.getElementById("title").value = movie.title;
      document.getElementById("director").value = movie.director;
      document.getElementById("year").value = movie.year;

      editingItem = editingItem;
      document.querySelector("button[type='submit']").textContent = "Actualizar Película";
    });

    editingItem = null;
    document.querySelector("button[type='submit']").textContent = "Agregar Película";
  } else {
    addMovieToList(movie);
  }

  this.reset();
});



function addMovieToList(movie) {
  const list = document.getElementById("movie-list");
  const item = document.createElement("li");

  item.innerHTML = `
    <strong>${movie.title}</strong> - ${movie.director} (${movie.year})
    <button class="edit-button">Editar</button>
    <button class="delete-button">Eliminar</button>
  `;

  
  item.querySelector(".delete-button").addEventListener("click", function () {
    list.removeChild(item);
  });

  
  item.querySelector(".edit-button").addEventListener("click", function () {
    document.getElementById("title").value = movie.title;
    document.getElementById("director").value = movie.director;
    document.getElementById("year").value = movie.year;

    editingItem = item;
    document.querySelector("button[type='submit']").textContent = "Actualizar Película";
  });

  list.appendChild(item);
}
