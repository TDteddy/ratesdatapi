const API_BASE_URL = 'http://bryze.kr:5005/api';

let allProducts = [];
let currentEditId = null;

// DOM Elements
const productsTableBody = document.getElementById('productsTableBody');
const brandFilter = document.getElementById('brandFilter');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const addNewBtn = document.getElementById('addNewBtn');
const productModal = document.getElementById('productModal');
const editModal = document.getElementById('editModal');
const productForm = document.getElementById('productForm');
const editForm = document.getElementById('editForm');
const notification = document.getElementById('notification');

// Modal controls
const closeBtn = document.querySelector('.close');
const editCloseBtn = document.querySelector('.edit-close');
const cancelBtn = document.getElementById('cancelBtn');
const editCancelBtn = document.querySelector('.edit-cancel');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    addNewBtn.addEventListener('click', () => openAddModal());
    closeBtn.addEventListener('click', () => closeModal(productModal));
    editCloseBtn.addEventListener('click', () => closeModal(editModal));
    cancelBtn.addEventListener('click', () => closeModal(productModal));
    editCancelBtn.addEventListener('click', () => closeModal(editModal));

    window.addEventListener('click', (e) => {
        if (e.target === productModal) closeModal(productModal);
        if (e.target === editModal) closeModal(editModal);
    });

    brandFilter.addEventListener('change', () => filterProducts());
    searchBtn.addEventListener('click', () => searchProducts());
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchProducts();
    });

    productForm.addEventListener('submit', handleAddProduct);
    editForm.addEventListener('submit', handleEditProduct);
}

// API Calls
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        if (!response.ok) throw new Error('Failed to fetch products');

        allProducts = await response.json();
        updateBrandFilter();
        updateStats();
        renderProducts(allProducts);
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('데이터 로드 실패', 'error');
        productsTableBody.innerHTML = '<tr><td colspan="7" class="loading">데이터 로드 실패</td></tr>';
    }
}

async function searchProducts() {
    const searchTerm = searchInput.value.trim();

    if (!searchTerm) {
        loadProducts();
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/products/search?q=${encodeURIComponent(searchTerm)}`);
        if (!response.ok) throw new Error('Failed to search products');

        const products = await response.json();
        renderProducts(products);

        if (products.length === 0) {
            showNotification('검색 결과가 없습니다', 'error');
        }
    } catch (error) {
        console.error('Error searching products:', error);
        showNotification('검색 실패', 'error');
    }
}

async function createProduct(productData) {
    try {
        const response = await fetch(`${API_BASE_URL}/products`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(productData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create product');
        }

        showNotification('상품이 성공적으로 추가되었습니다', 'success');
        closeModal(productModal);
        loadProducts();
    } catch (error) {
        console.error('Error creating product:', error);
        showNotification(error.message, 'error');
    }
}

async function updateProduct(id, productData) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(productData)
        });

        if (!response.ok) throw new Error('Failed to update product');

        showNotification('상품이 성공적으로 수정되었습니다', 'success');
        closeModal(editModal);
        loadProducts();
    } catch (error) {
        console.error('Error updating product:', error);
        showNotification('상품 수정 실패', 'error');
    }
}

async function deleteProduct(id) {
    if (!confirm('정말 이 상품을 삭제하시겠습니까?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/products/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete product');

        showNotification('상품이 성공적으로 삭제되었습니다', 'success');
        loadProducts();
    } catch (error) {
        console.error('Error deleting product:', error);
        showNotification('상품 삭제 실패', 'error');
    }
}

// UI Functions
function renderProducts(products) {
    if (products.length === 0) {
        productsTableBody.innerHTML = '<tr><td colspan="7" class="loading">데이터가 없습니다</td></tr>';
        return;
    }

    productsTableBody.innerHTML = products.map(product => `
        <tr>
            <td>${product.id}</td>
            <td>${product.product_name}</td>
            <td>${product.brand}</td>
            <td class="price-value">₩${parseFloat(product.cost_price).toLocaleString('ko-KR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
            <td>${new Date(product.created_at).toLocaleDateString('ko-KR')}</td>
            <td>${new Date(product.updated_at).toLocaleDateString('ko-KR')}</td>
            <td class="action-btns">
                <button class="btn btn-edit" onclick="openEditModal(${product.id})">수정</button>
                <button class="btn btn-delete" onclick="deleteProduct(${product.id})">삭제</button>
            </td>
        </tr>
    `).join('');
}

function updateBrandFilter() {
    const brands = [...new Set(allProducts.map(product => product.brand))].sort();

    brandFilter.innerHTML = '<option value="">전체 브랜드</option>' +
        brands.map(brand => `<option value="${brand}">${brand}</option>`).join('');
}

function updateStats() {
    document.getElementById('totalProducts').textContent = allProducts.length;

    const brands = new Set(allProducts.map(product => product.brand));
    document.getElementById('totalBrands').textContent = brands.size;

    const avgCost = allProducts.length > 0
        ? allProducts.reduce((sum, p) => sum + parseFloat(p.cost_price), 0) / allProducts.length
        : 0;
    document.getElementById('avgCost').textContent =
        '₩' + avgCost.toLocaleString('ko-KR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function filterProducts() {
    const selectedBrand = brandFilter.value;

    if (selectedBrand === '') {
        renderProducts(allProducts);
    } else {
        const filtered = allProducts.filter(product => product.brand === selectedBrand);
        renderProducts(filtered);
    }
}

function openAddModal() {
    document.getElementById('modalTitle').textContent = '새 상품 추가';
    productForm.reset();
    productModal.style.display = 'block';
}

function openEditModal(id) {
    const product = allProducts.find(p => p.id === id);
    if (!product) return;

    currentEditId = id;
    document.getElementById('editProductId').value = id;
    document.getElementById('editProductName').value = product.product_name;
    document.getElementById('editBrand').value = product.brand;
    document.getElementById('editCostPrice').value = parseFloat(product.cost_price);

    editModal.style.display = 'block';
}

function closeModal(modal) {
    modal.style.display = 'none';
    currentEditId = null;
}

function handleAddProduct(e) {
    e.preventDefault();

    const productData = {
        product_name: document.getElementById('productName').value.trim(),
        brand: document.getElementById('brand').value,
        cost_price: parseFloat(document.getElementById('costPrice').value)
    };

    createProduct(productData);
}

function handleEditProduct(e) {
    e.preventDefault();

    const productData = {
        product_name: document.getElementById('editProductName').value.trim(),
        brand: document.getElementById('editBrand').value,
        cost_price: parseFloat(document.getElementById('editCostPrice').value)
    };

    updateProduct(currentEditId, productData);
}

function showNotification(message, type) {
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}
