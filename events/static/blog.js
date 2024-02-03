document.addEventListener("DOMContentLoaded", function() {
    const loadMoreBtn = document.getElementById('load-more-btn');
    let page = 2; // starting page for additional posts

    loadMoreBtn.addEventListener('click', loadMorePosts);

    function loadMorePosts() {
        const lastBlogCard = document.querySelector('.latest-blogs-card:last-child');
        if (!lastBlogCard) {
            console.error('No blog cards found.');
            return;
        }
        const category = lastBlogCard.getAttribute('data-category');
        fetchMorePosts(category, page);
        page++;
    }

    async function fetchMorePosts(category, page) {
        try {
            const response = await fetch(`/load_more_posts/?category=${category}&page=${page}`);
            if (!response.ok) {
                throw new Error('Failed to fetch data.');
            }
            const data = await response.json();
            if (data.length > 0) {
                data.forEach(post => {
                    const blogCard = createBlogCard(post);
                    document.getElementById('latest-blogs-container').appendChild(blogCard);
                });
            } else {
                loadMoreBtn.style.display = 'none'; // Hide the button if no more posts
            }
        } catch (error) {
            console.error('Error fetching more posts:', error);
        }
    }

    function createBlogCard(post) {
        const blogCard = document.createElement('div');
        blogCard.classList.add('latest-blogs-card');
        blogCard.setAttribute('data-category', post.category);
        blogCard.innerHTML = `
            <figure class="latest-blogs-banner">
                <img src="${post.image}" alt="${post.title}" loading="lazy">
            </figure>
            <div class="latest-blogs-card-content">
                <ul class="latest-blogs-category-tag">
                    <li>
                        <a href="#" class="latest-blogs-category-card-tag">${post.category}</a>
                    </li>
                </ul>
                <h3 class="h4">
                    <a href="${post.url}" class="latest-blogs-title">${post.title}</a>
                </h3>
                <p class="latest-blogs-text">${post.short_description}</p>
                <button class="link">
                    <a href="${post.url}" class="latest-blogs-title">Read More</a>
                </button>
            </div>
        `;
        return blogCard;
    }
});
