const themeToggle = document.getElementById("theme-toggle");
const gallery = document.getElementById("gallery");

// Theme functionality
const setTheme = (theme) => {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);
};

const currentTheme = localStorage.getItem("theme") || "light";
setTheme(currentTheme);

themeToggle.addEventListener("click", () => {
  const newTheme =
    document.documentElement.getAttribute("data-theme") === "dark"
      ? "light"
      : "dark";
  setTheme(newTheme);
});

// Image generation (placeholders)
const images = [
  { src: "https://picsum.photos/id/10/600/400", title: "Forest Path" },
  { src: "https://picsum.photos/id/20/600/400", title: "Urban Life" },
  { src: "https://picsum.photos/id/30/600/400", title: "Quiet Moments" },
  { src: "https://picsum.photos/id/40/600/400", title: "Ocean Breeze" },
  { src: "https://picsum.photos/id/50/600/400", title: "Golden Hour" },
  { src: "https://picsum.photos/id/60/600/400", title: "Mountain Peak" },
  { src: "https://picsum.photos/id/70/600/400", title: "Street Lights" },
  { src: "https://picsum.photos/id/80/600/400", title: "Night Sky" },
];

const loadGallery = () => {
  images.forEach((img) => {
    const item = document.createElement("div");
    item.className = "gallery-item";
    item.innerHTML = `
            <img src="${img.src}" alt="${img.title}" loading="lazy">
            <div class="caption">${img.title}</div>
        `;
    gallery.appendChild(item);
  });
};

loadGallery();
