// ===== DemoShop Frontend Logic =====

document.addEventListener("DOMContentLoaded", () => {
    // --- Chat Widget ---
    const chatHeader = document.getElementById("chat-header");
    const chatBody = document.getElementById("chat-body");
    const chatToggle = document.getElementById("chat-toggle");
    const chatInput = document.getElementById("chat-input");
    const chatSendBtn = document.getElementById("chat-send");
    const messagesContainer = document.getElementById("messages");

    let sessionId = localStorage.getItem('demoShopChatSession');
    if (!sessionId) {
        sessionId = Math.floor(Math.random() * 1000000);
        localStorage.setItem('demoShopChatSession', sessionId);
    }

    if (chatHeader) {
        chatHeader.addEventListener("click", () => {
            if (chatBody.style.display === "none") {
                chatBody.style.display = "flex";
                chatToggle.textContent = "▼";
                setTimeout(() => chatInput.focus(), 100);
            } else {
                chatBody.style.display = "none";
                chatToggle.textContent = "▲";
            }
        });
    }

    function appendMessage(role, content) {
        if (!content) return; // Skip empty messages
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", role);
        if (role === 'assistant') {
            msgDiv.innerHTML = marked.parse(content);
        } else {
            msgDiv.textContent = content;
        }
        messagesContainer.appendChild(msgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async function loadChatHistory() {
        try {
            const response = await fetch(`/api/chat/history/${sessionId}`);
            if (response.ok) {
                const history = await response.json();
                history.forEach(msg => {
                    // Only show user and assistant text messages
                    if ((msg.role === 'user' || msg.role === 'assistant') && msg.content) {
                        appendMessage(msg.role, msg.content);
                    }
                });
            }
        } catch (e) {
            console.error("Failed to load chat history:", e);
        }
    }
    
    loadChatHistory();

    function showLoading() {
        const loadingDiv = document.createElement("div");
        loadingDiv.classList.add("message", "assistant", "loading-msg");
        loadingDiv.innerHTML = `<div class="typing-indicator"><span></span><span></span><span></span></div>`;
        messagesContainer.appendChild(loadingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return loadingDiv;
    }

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        appendMessage('user', message);
        chatInput.value = '';
        chatInput.disabled = true;
        chatSendBtn.disabled = true;

        const loadingIndicator = showLoading();

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message: message,
                    user_id: 1,
                    session_id: sessionId
                })
            });
            const data = await response.json();
            loadingIndicator.remove();
            appendMessage('assistant', data.response || "Sorry, I couldn't process that request.");
        } catch (error) {
            console.error("Error communicating with chat API:", error);
            loadingIndicator.remove();
            appendMessage('assistant', "Network error. Please try again later.");
        } finally {
            chatInput.disabled = false;
            chatSendBtn.disabled = false;
            chatInput.focus();
        }
    }

    if (chatSendBtn) {
        chatSendBtn.addEventListener("click", sendMessage);
    }
    if (chatInput) {
        chatInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") sendMessage();
        });
    }

    // --- Live Search ---
    const searchInput = document.getElementById("search-input");
    const searchResults = document.getElementById("search-results");
    let searchTimeout;

    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            const query = e.target.value.trim();
            clearTimeout(searchTimeout);

            if (query.length < 2) {
                if (searchResults) {
                    searchResults.classList.remove("active");
                    searchResults.innerHTML = "";
                }
                return;
            }

            searchTimeout = setTimeout(async () => {
                try {
                    const resp = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                    const results = await resp.json();
                    
                    if (!searchResults) return;

                    if (results.length === 0) {
                        searchResults.innerHTML = '<div style="padding: 1rem; text-align: center; color: var(--text-muted); font-size: 0.85rem;">No results found</div>';
                        searchResults.classList.add("active");
                        return;
                    }

                    let html = '';
                    results.forEach(p => {
                        html += `
                            <a href="/product/${p.id}" class="search-result-item">
                                <img src="${p.image_url}" alt="${p.name}">
                                <div class="search-result-info">
                                    <div class="name">${p.name}</div>
                                    <div class="meta">${p.category} · $${p.price.toFixed(2)}</div>
                                </div>
                            </a>
                        `;
                    });
                    html += `<a href="/search?q=${encodeURIComponent(query)}" class="search-all-link">View all results →</a>`;
                    
                    searchResults.innerHTML = html;
                    searchResults.classList.add("active");
                } catch (err) {
                    console.error("Search error:", err);
                }
            }, 250); // debounce 250ms
        });

        // Submit search on Enter
        searchInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                const query = searchInput.value.trim();
                if (query) {
                    window.location.href = `/search?q=${encodeURIComponent(query)}`;
                }
            }
        });

        // Close dropdown when clicking outside
        document.addEventListener("click", (e) => {
            if (searchResults && !searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.remove("active");
            }
        });
    }

    // --- Cart UI ---
    updateCartUI();
    renderCartPage();
});

// ===== Cart Logic =====

let cart = JSON.parse(localStorage.getItem('demoShopCart')) || [];

function saveCart() {
    localStorage.setItem('demoShopCart', JSON.stringify(cart));
    updateCartUI();
}

function addToCart(id, name, price, imageUrl) {
    const existingItem = cart.find(item => item.id === id);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ id, name, price, imageUrl, quantity: 1 });
    }
    saveCart();
    showToast(`Added ${name} to cart`);
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    saveCart();
    renderCartPage();
}

function updateCartUI() {
    const cartCountEl = document.getElementById('nav-cart-count');
    if (cartCountEl) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCountEl.textContent = `🛒 Cart (${totalItems})`;
    }
}

function showToast(message) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>✓</span> ${message}`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('hiding');
        toast.addEventListener('animationend', () => toast.remove());
    }, 3000);
}

function renderCartPage() {
    const container = document.getElementById('cart-items-container');
    if (!container) return;

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>Your cart is empty</h3>
                <p>Add some products to get started.</p>
                <a href="/" class="btn btn-primary" style="margin-top: 1rem;">Browse Products</a>
            </div>
        `;
        const subtotalEl = document.getElementById('cart-subtotal');
        const totalEl = document.getElementById('cart-total');
        if (subtotalEl) subtotalEl.textContent = '$0.00';
        if (totalEl) totalEl.textContent = '$0.00';
        return;
    }

    let html = '';
    let subtotal = 0;

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;
        
        html += `
            <div class="cart-item">
                <img src="${item.imageUrl}" alt="${item.name}">
                <div class="cart-item-info">
                    <div class="cart-item-title">${item.name}</div>
                    <div class="cart-item-price">$${item.price.toFixed(2)} × ${item.quantity}</div>
                </div>
                <div>
                    <button class="remove-btn" onclick="removeFromCart('${item.id}')">Remove</button>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
    
    const formattedSubtotal = `$${subtotal.toFixed(2)}`;
    const subtotalEl = document.getElementById('cart-subtotal');
    const totalEl = document.getElementById('cart-total');
    if (subtotalEl) subtotalEl.textContent = formattedSubtotal;
    if (totalEl) totalEl.textContent = formattedSubtotal;
}

async function checkout() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }
    
    let items = [];
    cart.forEach(item => {
        for(let i = 0; i < item.quantity; i++) {
            items.push(item.id);
        }
    });

    try {
        const response = await fetch("/api/checkout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ items: items })
        });
        
        if (response.status === 401) {
            alert("Please log in to checkout.");
            window.location.href = "/login";
            return;
        }
        
        if (response.ok) {
            alert("Checkout successful! Your items have been added to your order history.");
            cart = [];
            saveCart();
            renderCartPage();
            window.location.href = "/dashboard";
        } else {
            alert("Checkout failed.");
        }
    } catch(e) {
        alert("Network error.");
    }
}

function goToCheckout() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }
    window.location.href = "/checkout";
}
