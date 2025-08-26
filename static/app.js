// simple submit handler so pressing Enter in the search input works nicely
document.addEventListener("DOMContentLoaded", () => {
    const f = document.getElementById("search-form");
    if (f) {
        f.addEventListener("submit", (e) => {
            // let the browser handle navigation normally
        });
    }
});
