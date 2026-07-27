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
  closeMenu();
}));
const initialRoute = location.hash.slice(1).split("/")[0];
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
const mobileMenu = document.getElementById("mobileMenu");
const menuBackdrop = document.getElementById("menuBackdrop");
function openMenu() {
  mobileMenu.classList.add("open");
  mobileMenu.setAttribute("aria-hidden", "false");
  menuBackdrop.hidden = false;
  document.body.classList.add("menu-open");
  document.getElementById("menuClose").focus();
}
function closeMenu() {
  if (!mobileMenu) return;
  mobileMenu.classList.remove("open");
  mobileMenu.setAttribute("aria-hidden", "true");
  menuBackdrop.hidden = true;
  document.body.classList.remove("menu-open");
}
document.getElementById("menuBtn").addEventListener("click", openMenu);
document.getElementById("menuClose").addEventListener("click", closeMenu);
menuBackdrop.addEventListener("click", closeMenu);
document.addEventListener("keydown", event => { if (event.key === "Escape") closeMenu(); });
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

const adminOverview = document.getElementById("adminOverview");
const adminPanel = document.getElementById("adminPanel");
const adminViews = {
  users: { title: "Users & CRM", copy: "Manage members, consent, cohorts and support context.", stats: [["2,48,691", "Total users"], ["68.4%", "30-day retention"], ["1,842", "New this week"]], rows: [["Meera Sharma", "Premium family", "Active"], ["Rajesh Patel", "Yatra member", "Needs follow-up"], ["Anita Iyer", "Temple explorer", "Active"]] },
  partners: { title: "Partner verification", copy: "Review onboarding evidence and activate trusted supply.", stats: [["486", "Active partners"], ["18", "Awaiting review"], ["96.8%", "SLA compliance"]], rows: [["Shiv Shakti Residency", "Hotel · Varanasi", "Documents ready"], ["Ravi Heritage Walks", "Guide · Ujjain", "Identity check"], ["Ganga Seva Sadan", "Dharamshala · Kashi", "Bank review"]] },
  temples: { title: "Temple network", copy: "Govern verified profiles, timings, festivals and live darshan.", stats: [["1,284", "Published temples"], ["23", "Approval queue"], ["98.2%", "Fresh information"]], rows: [["Kashi Vishwanath", "Varanasi", "Crowd alert"], ["Mahakaleshwar", "Ujjain", "Verified"], ["Somnath Temple", "Gujarat", "Content review"]] },
  bookings: { title: "Booking management", copy: "Track inventory, confirmations, cancellations and fulfillment.", stats: [["1,284", "Today"], ["97.6%", "Success rate"], ["14", "Needs action"]], rows: [["NS8F42A1", "Kashi Puja · ₹1,100", "Confirmed"], ["NS6D19C4", "Dharamshala · ₹2,400", "Pending"], ["NS9A15F2", "Hotel Stay · ₹7,600", "Refund review"]] },
  finance: { title: "Finance & settlements", copy: "Reconcile payments, donations, refunds and partner settlements.", stats: [["₹38.6L", "Gross revenue"], ["₹12.4L", "Donations"], ["₹2.8L", "Settlement due"]], rows: [["RZP-847219", "Booking capture", "Reconciled"], ["DON-291847", "Temple donation", "Receipted"], ["RFN-038472", "Hotel refund", "Approval needed"]] },
  operations: { title: "Live operations", copy: "Monitor platform health, crowds, queues and provider incidents.", stats: [["99.98%", "Platform health"], ["3", "Open alerts"], ["42ms", "Queue age"]], rows: [["Live darshan CDN", "Kashi stream", "Degraded"], ["Crowd service", "Varanasi", "High load"], ["Notification queue", "All regions", "Healthy"]] },
  ai: { title: "AI control room", copy: "Observe grounded conversations, safety, quality, latency and cost.", stats: [["18,492", "Conversations"], ["4.7/5", "User rating"], ["0.04%", "Safety flags"]], rows: [["Planner v3.4", "Grounding 97.8%", "Healthy"], ["Hindi RAG", "Citation 96.1%", "Healthy"], ["Weather tool", "p95 1.9s", "Watch"]] },
  content: { title: "Content & CMS", copy: "Draft, review, localize and publish verified pilgrimage content.", stats: [["3,842", "Published items"], ["27", "In review"], ["8", "Scheduled"]], rows: [["Dev Deepawali Guide", "Hindi + English", "Scheduled"], ["Accessible Kashi Route", "Operations review", "Draft"], ["Mahakal Bhasma Aarti", "Temple verified", "Published"]] },
  support: { title: "Support desk", copy: "Resolve user, money, safety and partner cases against clear SLAs.", stats: [["12", "Open tickets"], ["18m", "First response"], ["94.6%", "Within SLA"]], rows: [["SUP-1842", "Payment captured, booking pending", "Urgent"], ["SUP-1838", "Guide meeting point", "In progress"], ["SUP-1829", "Receipt correction", "Waiting user"]] },
  settings: { title: "Platform settings", copy: "Control roles, integrations, notification policy and audit settings.", stats: [["42", "Admin users"], ["11", "Integrations"], ["100%", "MFA coverage"]], rows: [["Roles & permissions", "Last reviewed today", "Configured"], ["Payment gateway", "Webhook healthy", "Connected"], ["Retention policy", "Review due in 8 days", "Action"]] }
};

function renderAdminView(view) {
  document.querySelectorAll(".admin-sidebar [data-admin-view]").forEach(button => button.classList.toggle("active", button.dataset.adminView === view));
  if (view === "executive") {
    adminOverview.hidden = false;
    adminPanel.hidden = true;
    history.replaceState(null, "", "#admin");
    return;
  }
  const data = adminViews[view];
  if (!data) return;
  adminOverview.hidden = true;
  adminPanel.hidden = false;
  adminPanel.innerHTML = `<header class="admin-panel-head"><div><small>ADMIN WORKSPACE</small><h1>${data.title}</h1><p>${data.copy}</p></div><button class="admin-back" data-admin-view="executive">← Executive overview</button></header><div class="admin-panel-grid">${data.stats.map(([value, label]) => `<article class="admin-module-card"><small>${label.toUpperCase()}</small><b>${value}</b><button data-admin-action="inspect">View details</button></article>`).join("")}</div><div class="admin-list">${data.rows.map(([name, detail, status]) => `<div class="admin-list-row"><b>${name}</b><span>${detail}</span><span>${status}</span><button data-admin-action="open">Open</button></div>`).join("")}</div>`;
  history.replaceState(null, "", `#admin/${view}`);
  adminPanel.querySelector("h1").focus?.();
}

document.getElementById("admin").addEventListener("click", event => {
  const viewButton = event.target.closest("[data-admin-view]");
  if (viewButton) {
    event.preventDefault();
    renderAdminView(viewButton.dataset.adminView);
    return;
  }
  const actionButton = event.target.closest("[data-admin-action]");
  if (actionButton) showToast(actionButton.dataset.adminAction === "open" ? "Record opened in review mode" : "Detailed report loaded");
});

if (location.hash.startsWith("#admin/")) renderAdminView(location.hash.split("/")[1]);

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
