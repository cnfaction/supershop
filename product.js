document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = parseInt(urlParams.get('id'));
    
    if (!productId) {
        window.location.href = 'index.html';
        return;
    }

    const product = getProducts().find(p => p.id === productId);
    if (!product) {
        document.getElementById('productDetail').innerHTML = `
            <div class="error-container">
                <h2>Product Not Found</h2>
                <p>Sorry, we couldn't find the product you're looking for.</p>
                <a href="index.html" class="btn-primary">Back to Home</a>
            </div>
        `;
        return;
    }

    renderProduct(product);
});

function renderProduct(p) {
    const container = document.getElementById('productDetail');
    const images = (Array.isArray(p.images) ? p.images : (p.image ? [p.image] : [])).filter(i => i).slice(0, 40);
    if (images.length === 0) images.push('https://via.placeholder.com/600x600?text=No+Image+Available');

    const rawUrl = p.link || '#';
    const encUrl = encodeURIComponent(rawUrl);
    let shopType = 'weidian';
    let itemId = '';
    
    if (rawUrl.includes('weidian.com') || rawUrl.includes('k.youshop10.com')) {
        shopType = 'weidian';
        const match = rawUrl.match(/itemID=(\d+)/);
        if (match) itemId = match[1];
    } else if (rawUrl.includes('taobao.com') || rawUrl.includes('tmall.com')) {
        shopType = 'taobao';
        const match = rawUrl.match(/id=(\d+)/);
        if (match) itemId = match[1];
    } else if (rawUrl.includes('1688.com')) {
        shopType = '1688';
        const match = rawUrl.match(/\/(\d+)\.html/);
        if (match) itemId = match[1];
    }

    // Update Page Title
    document.title = `${p.title} - Supershop`;

    container.innerHTML = `
        <div class="product-detail-layout">
            <div class="detail-left">
                <div class="main-image-viewport">
                    <img id="mainDetailImg" src="${images[0]}" alt="${p.title}" onerror="this.src='https://via.placeholder.com/600x600?text=Image+Not+Found'">
                </div>
                <div class="detail-thumbnails">
                    ${images.map((img, i) => `
                        <div class="thumb-item ${i === 0 ? 'active' : ''}" onclick="switchDetailImg(this, '${img}')">
                            <img src="${img}" alt="Thumbnail ${i+1}" onerror="this.src='https://via.placeholder.com/100x100?text=Error'">
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="detail-right">
                <div class="product-header">
                    <span class="batch-badge">${p.brand || 'Premium'} Batch</span>
                    <h1 class="product-title">${p.title}</h1>
                    <div class="product-meta">Product ID: ${p.id} | Shop: ${shopType.toUpperCase()}</div>
                </div>

                <div class="price-box">
                    <div class="price-main">$${p.price.toFixed(2)}</div>
                    <div class="price-sub">≈ ¥${(p.price * 7.2).toFixed(0)}</div>
                </div>

                <div class="action-buttons">
                    <button class="btn-action btn-copy" onclick="copyToClipboard('${rawUrl}')">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
                        Copy Source Link
                    </button>
                    <a href="${rawUrl}" target="_blank" class="btn-action btn-original">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>
                        View Original
                    </a>
                </div>

                <div class="agent-list-container">
                    <h3 class="section-label">Purchase with Agent</h3>
                    <div class="agent-grid">
                        ${[
                            { name: 'Kakobuy', promo: '$410 coupons!', url: `https://www.kakobuy.com/item/details?url=${encUrl}&spider_token=bd73&affcode=tg59k`, logo: 'https://www.kakobuy.com/favicon.ico' },
                            { name: 'ACBuy', promo: '$150 coupons!', url: itemId ? `https://www.acbuy.com/product?id=${itemId}&source=${shopType === 'weidian' ? 'WD' : 'TB'}` : `https://www.acbuy.com/en/page/buy/?url=${encUrl}`, logo: 'https://www.acbuy.com/favicon.ico' },
                            { name: 'OopBuy', promo: '$210 coupons!', url: itemId ? `https://oopbuy.com/product/${shopType}/${itemId}?inviteCode=PXA0M2UXQ` : `https://www.oopbuy.com/en/page/buy/?url=${encUrl}`, logo: 'logos/oopbuy.png' },
                            { name: 'MuleBuy', promo: '1288 Coupons!', url: itemId ? `https://mulebuy.com/product/?shop_type=${shopType}&id=${itemId}&ref=200943051` : `https://mulebuy.com/product/?url=${encUrl}`, logo: 'https://mulebuy.com/favicon.ico' },
                            { name: 'AllChinaBuy', promo: '$150 coupons!', url: `https://www.allchinabuy.com/en/page/buy/?nTag=Home-search&from=search-input&_search=url&position=&url=${encUrl}`, logo: 'https://www.allchinabuy.com/favicon.ico' },
                            { name: 'CSSBuy', promo: 'Pro Sourcing!', url: itemId ? `https://www.cssbuy.com/item-${shopType === 'micro' ? 'micro' : shopType}-${itemId}.html` : `https://www.cssbuy.com/?url=${encUrl}`, logo: 'https://www.cssbuy.com/favicon.ico' },
                            { name: 'Superbuy', promo: 'Reliable Agent!', url: `https://www.superbuy.com/en/page/buy/?url=${encUrl}`, logo: 'https://www.superbuy.com/favicon.ico' },
                            { name: 'HipoBuy', promo: 'Fast Delivery!', url: itemId ? `https://hipobuy.com/product/${shopType}/${itemId}` : `https://hipobuy.com/product/?url=${encUrl}`, logo: 'logos/hipobuy.png' },
                            { name: 'HubBuyCN', promo: 'Trusted!', url: `https://hubbuycn.com/product/item?url=${encUrl}`, logo: 'https://hubbuycn.com/favicon.ico' },
                            { name: 'USFANS', promo: 'Global Fans!', url: itemId ? `https://usfans.com/product/${shopType === 'weidian' ? '3' : (shopType === 'taobao' ? '2' : '1')}/${itemId}` : `https://usfans.com/?url=${encUrl}`, logo: 'https://usfans.com/favicon.ico' }
                        ].map((agent, i) => `
                            <a href="${agent.url}" target="_blank" class="agent-card ${i === 0 ? 'highlight' : ''}">
                                <div class="agent-logo">
                                    <img src="${agent.logo}" alt="${agent.name}" onerror="this.src='https://via.placeholder.com/40x40?text=${agent.name[0]}'">
                                </div>
                                <div class="agent-info">
                                    <span class="agent-name">${agent.name}</span>
                                    <span class="agent-promo">${agent.promo}</span>
                                </div>
                                <svg class="chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
                            </a>
                        `).join('')}
                    </div>
                </div>

                <div class="product-description">
                    <h3 class="section-label">Product Information</h3>
                    <p>${p.description || 'No description available for this item.'}</p>
                </div>
            </div>
        </div>
    `;
}

function switchDetailImg(thumb, src) {
    const mainImg = document.getElementById('mainDetailImg');
    mainImg.style.opacity = '0';
    setTimeout(() => {
        mainImg.src = src;
        mainImg.style.opacity = '1';
        document.querySelectorAll('.thumb-item').forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
    }, 200);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Link copied to clipboard!');
    }).catch(err => {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("copy");
        document.body.removeChild(textArea);
        alert('Link copied to clipboard!');
    });
}
