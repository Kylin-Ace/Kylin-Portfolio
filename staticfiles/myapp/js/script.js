// Dark Mode Toggle
document.getElementById("themeToggle").addEventListener("click", function() {
    document.body.classList.toggle("bg-gray-900");
    document.body.classList.toggle("text-white");
});

// Modal Functions
function openModal(title, description, imageUrl, link) {
    document.getElementById("modalTitle").textContent = title;
    document.getElementById("modalDescription").textContent = description;
    document.getElementById("modalImage").src = imageUrl;
    document.getElementById("modalLink").href = link;
    document.getElementById("modal").classList.remove("hidden");
}

function closeModal() {
    document.getElementById("modal").classList.add("hidden");
}
