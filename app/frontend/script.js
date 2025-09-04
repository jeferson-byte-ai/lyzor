// ========= SELECT PAGE =========
const navItems = document.querySelectorAll(".nav-item");
const pages = document.querySelectorAll(".page");

navItems.forEach(item => {
  item.addEventListener("click", () => {
    // Remove active de todos
    navItems.forEach(i => i.classList.remove("active"));
    pages.forEach(p => p.classList.remove("active"));
    
    // Ativa o clicado
    item.classList.add("active");
    const pageId = item.dataset.page;
    document.getElementById(pageId).classList.add("active");
  });
});

// ========= THEME TOGGLE =========
const themeButtons = [document.getElementById("themeToggle"), document.getElementById("themeToggle2")];

themeButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    const html = document.documentElement;
    const current = html.getAttribute("data-theme");
    const newTheme = current === "light" ? "dark" : "light";
    html.setAttribute("data-theme", newTheme);

    // Atualiza ícones e texto
    themeButtons.forEach(b => {
      b.querySelector("i").setAttribute("data-lucide", newTheme === "light" ? "sun" : "moon");
      b.querySelector("span")?.remove();
      const span = document.createElement("span");
      span.textContent = newTheme === "light" ? "Light" : "Dark";
      b.appendChild(span);
    });

    // Re-renderiza ícones Lucide
    if (window.lucide) lucide.replace();
  });
});

// ========= LOAD LANGUAGES =========
const speakSelect = document.getElementById("speakSelect");
const understandSelect = document.getElementById("understandSelect");
const langStatus = document.getElementById("langStatus");

const languages = [
  { code: "en", name: "English" },
  { code: "pt", name: "Português" },
  { code: "es", name: "Español" },
  { code: "fr", name: "Français" },
  { code: "de", name: "Deutsch" }
  // Pode adicionar mais
];

// Preenche selects
languages.forEach(lang => {
  const opt1 = document.createElement("option");
  opt1.value = lang.code;
  opt1.textContent = lang.name;
  speakSelect.appendChild(opt1);

  const opt2 = document.createElement("option");
  opt2.value = lang.code;
  opt2.textContent = lang.name;
  understandSelect.appendChild(opt2);
});

// Salva preferências local
document.getElementById("saveLang").addEventListener("click", () => {
  const speak = speakSelect.value;
  const understand = understandSelect.value;
  localStorage.setItem("lyzor_speak", speak);
  localStorage.setItem("lyzor_understand", understand);
  langStatus.textContent = "Preferences saved locally!";
  setTimeout(() => langStatus.textContent = "", 2000);
});

// ========= FILE INPUT LABEL =========
const voiceInput = document.getElementById("voiceFile");
voiceInput.addEventListener("change", (e) => {
  const fileName = e.target.files[0]?.name || "Choose audio file";
  e.target.nextElementSibling.querySelector("span").textContent = fileName;
});
