const pages = [...document.querySelectorAll(".page")];
const routeButtons = [...document.querySelectorAll("[data-route]")];
const toast = document.getElementById("toast");

function navigate(route) {
  const target = document.getElementById(route);
  if (!target) return;
  pages.forEach(page => page.classList.toggle("active", page === target));
  document.querySelectorAll(".mobile-nav button").forEach(btn => btn.classList.toggle("active", btn.dataset.route === route));
  window.scrollTo({ top: 0, behavior: "smooth" });
  history.replaceState(null, "", route === "home" ? "#" : `#${route}`);
}
routeButtons.forEach(button => button.addEventListener("click", event => {
  event.preventDefault();
  navigate(button.dataset.route);
}));
const initialRoute = location.hash.slice(1);
if (initialRoute && document.getElementById(initialRoute)) navigate(initialRoute);

document.getElementById("themeToggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
  localStorage.setItem("namo-theme", document.body.classList.contains("dark") ? "dark" : "light");
});
if (localStorage.getItem("namo-theme") === "dark") document.body.classList.add("dark");

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 2400);
}

document.getElementById("languageBtn").addEventListener("click", () => showToast("Language options: English · हिंदी · தமிழ் · ગુજરાતી"));
document.getElementById("menuBtn").addEventListener("click", () => navigate("discover"));
document.getElementById("aiSearch").addEventListener("submit", event => {
  event.preventDefault();
  const prompt = event.currentTarget.querySelector("input").value.trim();
  navigate("planner");
  if (prompt) document.querySelector('#plannerForm input[name="destination"]').value = prompt.match(/(?:in|to)\s+([A-Za-z ]+?)(?:\s+under|$)/i)?.[1]?.trim() || prompt;
});

const track = document.getElementById("destinationTrack");
document.getElementById("nextDest").addEventListener("click", () => track.scrollBy({ left: 310, behavior: "smooth" }));
document.getElementById("prevDest").addEventListener("click", () => track.scrollBy({ left: -310, behavior: "smooth" }));
document.querySelectorAll(".destination-card").forEach(card => card.addEventListener("click", () => {
  navigate("planner");
  document.querySelector('#plannerForm input[name="destination"]').value = card.dataset.place;
}));

const search = document.getElementById("templeSearch");
search.addEventListener("input", () => {
  const query = search.value.toLowerCase().trim();
  document.querySelectorAll("#templeGrid article").forEach(card => {
    card.style.display = card.dataset.name.toLowerCase().includes(query) ? "" : "none";
  });
});
document.querySelectorAll(".filter-row button").forEach(button => button.addEventListener("click", () => {
  document.querySelectorAll(".filter-row button").forEach(item => item.classList.remove("active"));
  button.classList.add("active");
  showToast(`${button.textContent} places selected`);
}));

document.querySelectorAll(".choice-row button").forEach(button => button.addEventListener("click", () => button.classList.toggle("selected")));
document.getElementById("plannerForm").addEventListener("submit", event => {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  const destination = data.get("destination");
  const days = data.get("days");
  document.getElementById("plannerPreview").innerHTML = `<div class="itinerary"><span class="kicker light">YOUR NAMO PLAN</span><h2>${days} in ${destination}</h2><p>A comfortable pace with time for rest and reflection.</p><div><b>Day 1 · Arrive & settle in</b><small>Verified pickup · Check-in · Evening orientation</small></div><div><b>Day 2 · Sacred darshan</b><small>Priority morning route · Local guide · Satvik lunch</small></div><div><b>Day 3 · River & heritage</b><small>Accessible ghat route · Aarti · Flexible departure</small></div><button class="cream-btn" style="margin-top:18px">Save this journey →</button></div>`;
  showToast("Your personalised yatra is ready");
});

const modal = document.getElementById("assistantModal");
const voiceStatus = document.getElementById("voiceStatus");
function openVoice() { modal.classList.add("open"); modal.setAttribute("aria-hidden", "false"); }
function closeVoice() { modal.classList.remove("open", "listening"); modal.setAttribute("aria-hidden", "true"); }
document.getElementById("voiceBtn").addEventListener("click", openVoice);
document.getElementById("modalClose").addEventListener("click", closeVoice);
modal.addEventListener("click", event => { if (event.target === modal) closeVoice(); });
document.getElementById("voiceMain").addEventListener("click", () => {
  modal.classList.toggle("listening");
  voiceStatus.textContent = modal.classList.contains("listening") ? "Listening… speak naturally." : "I heard: “Plan a family trip to Varanasi.”";
});
document.getElementById("sosBtn").addEventListener("click", () => showToast("Emergency support panel opened — call 112 for immediate danger"));
function applyPreference(input, className, key) {
  if (!input) return;
  input.checked = localStorage.getItem(key) === "true";
  document.body.classList.toggle(className, input.checked);
  input.addEventListener("change", () => {
    document.body.classList.toggle(className, input.checked);
    localStorage.setItem(key, input.checked);
  });
}
applyPreference(document.getElementById("largeText"), "large-text", "namo-large-text");
applyPreference(document.getElementById("highContrast"), "high-contrast", "namo-high-contrast");
document.getElementById("autoTheme").addEventListener("change", event => {
  if (event.target.checked) document.body.classList.toggle("dark", matchMedia("(prefers-color-scheme: dark)").matches);
  showToast(event.target.checked ? "Theme will follow this device" : "Manual theme control restored");
});

const adminSearch = document.getElementById("adminSearch");
adminSearch.addEventListener("input", () => {
  const query = adminSearch.value.toLowerCase();
  document.querySelectorAll("#bookingTable tbody tr").forEach(row => {
    row.hidden = !row.textContent.toLowerCase().includes(query);
  });
});
document.getElementById("exportCsv").addEventListener("click", () => {
  const rows = [...document.querySelectorAll("#bookingTable tr")].filter(row => !row.hidden);
  const csv = rows.map(row => [...row.children].map(cell => `"${cell.textContent.trim().replaceAll('"', '""')}"`).join(",")).join("\n");
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
  link.download = `namo-setu-bookings-${new Date().toISOString().slice(0, 10)}.csv`;
  link.click();
  URL.revokeObjectURL(link.href);
  showToast("Booking report exported");
});
window.addEventListener("offline", () => document.getElementById("offlineBar").style.display = "block");
window.addEventListener("online", () => document.getElementById("offlineBar").style.display = "none");

let installPrompt;
const installBtn = document.getElementById("installBtn");
window.addEventListener("beforeinstallprompt", event => {
  event.preventDefault();
  installPrompt = event;
  installBtn.hidden = false;
});
installBtn.addEventListener("click", async () => {
  if (!installPrompt) return;
  installPrompt.prompt();
  const result = await installPrompt.userChoice;
  showToast(result.outcome === "accepted" ? "NAMO SETU installed" : "Install available anytime");
  installPrompt = undefined;
  installBtn.hidden = true;
});
window.addEventListener("appinstalled", () => showToast("NAMO SETU is ready on your device"));

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => navigator.serviceWorker.register("/service-worker.js")
    .catch(() => showToast("Offline setup will retry automatically")));
}
