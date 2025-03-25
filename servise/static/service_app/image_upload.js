const uploadBox = document.getElementById("uploadBox");
const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");

// Handle file input change
fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
        displayImage(file);
    }
});

// Handle drag-and-drop
uploadBox.addEventListener("dragover", (event) => {
    event.preventDefault();
    uploadBox.style.backgroundColor = "#6096c6";
});

uploadBox.addEventListener("dragleave", () => {
    uploadBox.style.backgroundColor = "#4a90e2";
});

uploadBox.addEventListener("drop", (event) => {
    event.preventDefault();
    uploadBox.style.backgroundColor = "#4a90e2";
    const file = event.dataTransfer.files[0];
    if (file) {
        displayImage(file);
    }
});

// Display uploaded image and hide upload box
function displayImage(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        // Hide upload box
        uploadBox.classList.add("hidden");

        // Show preview
        preview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`;
        preview.classList.remove("hidden");
    };
    reader.readAsDataURL(file);
}
