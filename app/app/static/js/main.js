document.addEventListener("DOMContentLoaded", () => {
    const dashboard = document.getElementById("dashboard");
    const searchBar = document.getElementById("search-bar");
    const loadingBar = document.getElementById("loading");

    // Like / Save buttons
    document.addEventListener("click", async (e) => {
        if(e.target.classList.contains("like-btn")){
            const img = e.target.closest(".card").querySelector("img").src;
            const form = new FormData();
            form.append("image_url", img);
            await fetch("/like", { method:"POST", body:form });
            e.target.textContent = "❤️ Liked";
        }
        if(e.target.classList.contains("save-btn")){
            const card = e.target.closest(".card");
            const img = card.querySelector("img").src;
            const photographer = card.querySelectorAll("p")[1].textContent;
            const form = new FormData();
            form.append("image_url", img);
            form.append("photographer", photographer);
            await fetch("/save", { method:"POST", body:form });
            e.target.textContent = "💾 Saved";
        }
    });

    // Infinite scroll
    let page = 1;
    let loading = false;

    async function loadMore(){
        if(loading) return;
        loading = true;
        loadingBar.style.display = "block";

        const interests = Array.from(document.querySelectorAll("input[name='interests']:checked")).map(i=>i.value);
        const query = searchBar.value;
        page++;

        const form = new FormData();
        form.append("page", page);
        interests.forEach(i => form.append("interests", i));
        if(query) form.append("search", query);

        const resp = await fetch("/load_more", { method:"POST", body:form });
        const data = await resp.json();

        data.images.forEach(img=>{
            const card = document.createElement("div");
            card.classList.add("card");
            card.innerHTML = `
                <img src="${img.url}" alt="${img.tags}">
                <p>${img.tags}</p>
                <p>${img.photographer || ""}</p>
                <div class="icons">
                    <button class="like-btn">❤️</button>
                    <button class="save-btn">💾</button>
                    <a href="${img.download}" download><button>⬇️</button></a>
                </div>
            `;
            dashboard.appendChild(card);
        });

        loadingBar.style.display = "none";
        loading = false;
    }

    window.addEventListener("scroll", () => {
        if(window.innerHeight + window.scrollY >= document.body.offsetHeight - 500){
            loadMore();
        }
    });

    // Search functionality
    searchBar.addEventListener("keypress", (e)=>{
        if(e.key === "Enter"){
            e.preventDefault();
            dashboard.innerHTML = "";
            page = 0;
            loadMore();
        }
    });
});
