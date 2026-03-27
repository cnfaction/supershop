const productsGrid = document.getElementById('productsGrid');
const pageTitle = document.getElementById('pageTitle');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebarOverlay');
const modal = document.getElementById('modalOverlay');
const modalContent = document.getElementById('modalContent');
const scrollTopBtn = document.getElementById('scrollTop');
const searchInput = document.getElementById('searchInput');

let activeFilters = {
  category: 'shoes',
  subCategories: [],
  brands: [],
  priceMin: null,
  priceMax: null,
  query: ''
};

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
  populateBrandsDropdown();
  renderProducts();
  setupEventListeners();
  
  // Check for product ID in URL on load for direct link sharing
  const urlParams = new URLSearchParams(window.location.search);
  const productId = urlParams.get('id');
  if (productId) {
    setTimeout(() => openProductDetail(parseInt(productId)), 100);
  }
});

// Sync UI with browser back/forward buttons
window.addEventListener('popstate', (event) => {
  const urlParams = new URLSearchParams(window.location.search);
  const productId = urlParams.get('id');
  if (!productId) {
    closeModal(true);
  } else {
    openProductDetail(parseInt(productId), true);
  }
});

function populateBrandsDropdown() {
  const menu = document.getElementById('brandsDropdownMenu');
  if (!menu) return;
  
  const allBrands = [...new Set(getProducts().map(p => p.brand).filter(Boolean))].sort((a,b) => a.localeCompare(b));
  
  const html = allBrands.map(b => `<a class="cat-link brand-link" style="padding: 0.5rem 0.75rem; border-radius: 0.5rem; border-bottom: none; display: block; text-align: left;" onclick="setBrand('${b.replace(/'/g, "\\'")}',this); document.getElementById('brandsDropdownMenu').style.display='none'">${b}</a>`).join('');
  
  menu.insertAdjacentHTML('beforeend', html);
}

function setupEventListeners() {
  window.addEventListener('scroll', () => {
    scrollTopBtn.style.display = window.scrollY > 400 ? 'flex' : 'none';
  });
}

function openSidebar() {
  sidebar.classList.add('open');
  overlay.classList.add('open');
}

function closeSidebar() {
  sidebar.classList.remove('open');
  overlay.classList.remove('open');
}

function setCategory(cat, el) {
  activeFilters.category = cat;
  pageTitle.textContent = el.textContent.trim();
  
  // Highlight active link
  document.querySelectorAll('.cat-link:not(.brand-link)').forEach(link => link.classList.remove('active'));
  el.classList.add('active');
  
  renderProducts();
}

function setBrand(brand, el) {
  // Highlight active brand link
  document.querySelectorAll('.brand-link').forEach(link => link.classList.remove('active'));
  el.classList.add('active');
  
  if (brand === 'all') {
    activeFilters.brands = [];
  } else {
    activeFilters.brands = [brand];
  }
  
  renderProducts();
}

function applyFilters() {
  const catCheckboxes = document.querySelectorAll('#catFilterList input:checked');
  const brandCheckboxes = document.querySelectorAll('#brandsAcc input:checked');
  
  activeFilters.subCategories = Array.from(catCheckboxes).map(cb => cb.value);
  activeFilters.brands = Array.from(brandCheckboxes).map(cb => cb.value);
  activeFilters.priceMin = parseFloat(document.getElementById('priceMin').value) || null;
  activeFilters.priceMax = parseFloat(document.getElementById('priceMax').value) || null;
  
  renderProducts();
}

function clearFilters() {
  document.querySelectorAll('.filter-item input:checked').forEach(cb => cb.checked = false);
  document.getElementById('priceMin').value = '';
  document.getElementById('priceMax').value = '';
  
  activeFilters.subCategories = [];
  activeFilters.brands = [];
  activeFilters.priceMin = null;
  activeFilters.priceMax = null;
  
  renderProducts();
}

function handleSearch() {
  activeFilters.query = searchInput.value.toLowerCase().trim();
  renderProducts();
}

function renderProducts() {
  const allProducts = getProducts();
  
  const filtered = allProducts.filter(p => {
    // Category check
    if (activeFilters.category !== 'all' && p.category !== activeFilters.category) return false;
    
    // Search check
    if (activeFilters.query && !p.title.toLowerCase().includes(activeFilters.query)) return false;
    
    // Sub-category check
    if (activeFilters.subCategories.length > 0 && !activeFilters.subCategories.includes(p.category)) return false;
    
    // Brand check
    if (activeFilters.brands.length > 0) {
        // Simple string contains for brand array
        const found = activeFilters.brands.some(b => (p.brand || '').toLowerCase().includes(b.toLowerCase()));
        if (!found) return false;
    }
    
    // Price check
    if (activeFilters.priceMin !== null && p.price < activeFilters.priceMin) return false;
    if (activeFilters.priceMax !== null && p.price > activeFilters.priceMax) return false;
    
    return true;
  });

  productsGrid.innerHTML = filtered.map(p => {
    const primaryImage = Array.isArray(p.images) && p.images.length > 0 ? p.images[0] : p.image;
    const imgPath = primaryImage || 'https://via.placeholder.com/600x600?text=No+Image+Available';
    return `
    <div class="product-card" onclick="openProductDetail(${p.id})">
      <div class="card-img-wrap">
        <img src="${imgPath}" alt="${p.title}" loading="lazy" onerror="this.src='https://via.placeholder.com/600x600?text=Image+Not+Found'">
      </div>
      <div class="card-info">
        <h3 class="card-title">${p.title}</h3>
        <span class="card-brand">${p.brand}</span>
      </div>
      <div class="card-footer">
        <span class="card-price">$${p.price.toFixed(2)}</span>
        <button class="card-btn">Details</button>
      </div>
    </div>
  `;
  }).join('');
  
  document.getElementById('noResults').style.display = filtered.length === 0 ? 'block' : 'none';
}

function openProductDetail(id, isPopState = false) {
  const p = getProducts().find(item => item.id === id);
  if (!p) return;

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

  modalContent.innerHTML = `
    <div class="modal-left">
      <div class="modal-img-container">
        <img id="mainModalImg" src="${images[0]}" alt="${p.title}" onerror="this.src='https://via.placeholder.com/600x600?text=Image+Not+Found'">
      </div>
      <div class="thumbnail-gallery">
        ${images.map((img, i) => `
          <img src="${img}" class="modal-thumb ${i === 0 ? 'active' : ''}" 
               onclick="switchMainImg(this, '${img}')">
        `).join('')}
      </div>
    </div>
    
    <div class="modal-right">
      <div class="modal-header-info">
        <span class="batch-badge">${p.brand || 'Premium'} Batch</span>
        <h2 class="modal-title">${p.title}</h2>
        <div class="modal-meta">Product ID: ${p.id} | Shop: ${shopType.toUpperCase()}</div>
      </div>
      
      <div class="price-section">
        <span class="price-amount">$${p.price.toFixed(2)}</span>
        <span class="price-cny">≈ ¥${(p.price * 7.2).toFixed(0)}</span>
      </div>

      <div class="source-actions">
        <button class="btn-source btn-source-primary" onclick="copyToClipboard('${rawUrl}')">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
          Copy Source
        </button>
        <a href="${rawUrl}" target="_blank" class="btn-source">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>
          Original Link
        </a>
      </div>

      <div class="agent-section">
        <h4 class="agent-section-title">Select Buying Agent</h4>
        <div class="agent-links">
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
            <a href="${agent.url}" target="_blank" class="purchase-card ${i === 0 ? 'highlight' : ''}">
              <div class="card-top-row">
                <div class="agent-logo-sq">
                   <img src="${agent.logo}" alt="${agent.name}" onerror="this.src='https://via.placeholder.com/40x40?text=${agent.name[0]}'">
                </div>
                <div class="agent-header-info">
                  <div class="agent-name-row">
                    <span class="name-text">${agent.name}</span>
                  </div>
                  <div class="promo-tagline">${agent.promo}</div>
                </div>
                <div class="chevron-arrow">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
                </div>
              </div>
            </a>
          `).join('')}
        </div>
      </div>
      
      <button onclick="toggleFavorite(${p.id})" style="margin-top: 2rem; color: #64748b; font-size: 0.9rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem; width: 100%; border-top: 1px solid #1e293b; padding-top: 1.5rem; background: transparent;">
         Add to Wishlist <span style="font-size: 1.2rem;">❤</span>
      </button>
    </div>
  `;
  
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';

  // Update URL for independent link sharing (if not triggered by back/forward button)
  if (!isPopState) {
    const newUrl = new URL(window.location.href);
    newUrl.searchParams.set('id', id);
    window.history.pushState({ id }, "", newUrl);
  }
}

function toggleAgentList() {
  const wrapper = document.getElementById('agentListWrapper');
  if (wrapper.style.display === 'none') {
    wrapper.style.display = 'block';
    wrapper.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    wrapper.style.display = 'none';
  }
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert('Source URL copied to clipboard!');
  }).catch(err => {
    console.error('Failed to copy: ', err);
    // Fallback
    const textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("copy");
    document.body.removeChild(textArea);
    alert('Source URL copied to clipboard!');
  });
}

function switchMainImg(thumb, src) {
  const mainImg = document.getElementById('mainModalImg');
  
  // Fade out current
  mainImg.style.opacity = '0';
  
  setTimeout(() => {
    mainImg.src = src;
    mainImg.style.opacity = '1';
    
    // Update active state
    document.querySelectorAll('.modal-thumb').forEach(t => t.classList.remove('active'));
    thumb.classList.add('active');
    
    // Auto-scroll thumbnail into view
    thumb.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  }, 200);
}

function closeModal(e) {
  if (e === true || !e || e.target === modal || e.target.classList.contains('modal-close-btn')) {
    modal.classList.remove('open');
    document.body.style.overflow = '';
    
    // Clear URL parameter when modal closes (only if manually closed)
    if (e !== true) {
      const newUrl = new URL(window.location.href);
      newUrl.searchParams.delete('id');
      window.history.pushState({}, "", newUrl);
    }
  }
}

function toggleAccordion(id) {
  const acc = document.getElementById(id);
  const arrow = document.getElementById(id + 'Arrow');
  const isOpen = acc.style.display !== 'none';
  acc.style.display = isOpen ? 'none' : 'flex';
  arrow.textContent = isOpen ? '▼' : '▲';
}

function toggleAdmin() {
    window.location.href = 'admin/index.html';
}

// Categories Scroll Logic
function scrollCats(px) {
    const bar = document.getElementById('catBar');
    if (bar) {
        bar.scrollBy({ left: px, behavior: 'smooth' });
        setTimeout(updateScrollBtns, 400); // Check after animation
    }
}

function updateScrollBtns() {
    const bar = document.getElementById('catBar');
    const prev = document.getElementById('catPrev');
    const next = document.getElementById('catNext');
    if (!bar || !prev || !next) return;

    // Show prev if scrolled right, show next if more content to the right
    prev.style.display = bar.scrollLeft > 20 ? 'flex' : 'none';
    const isAtEnd = bar.scrollLeft + bar.clientWidth >= bar.scrollWidth - 20;
    next.style.display = isAtEnd ? 'none' : 'flex';
}

// Initial check
window.addEventListener('load', updateScrollBtns);
window.addEventListener('resize', updateScrollBtns);
document.getElementById('catBar')?.addEventListener('scroll', updateScrollBtns);
