const API_BASE_URL = 'https://bryze.kr:5005/api';

let allRates = [];
let currentEditId = null;

// DOM Elements
const ratesTableBody = document.getElementById('ratesTableBody');
const brandFilter = document.getElementById('brandFilter');
const addNewBtn = document.getElementById('addNewBtn');
const rateModal = document.getElementById('rateModal');
const editModal = document.getElementById('editModal');
const rateForm = document.getElementById('rateForm');
const editForm = document.getElementById('editForm');
const notification = document.getElementById('notification');

// Modal controls
const closeBtn = document.querySelector('.close');
const editCloseBtn = document.querySelector('.edit-close');
const cancelBtn = document.getElementById('cancelBtn');
const editCancelBtn = document.querySelector('.edit-cancel');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadRates();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    addNewBtn.addEventListener('click', () => openAddModal());
    closeBtn.addEventListener('click', () => closeModal(rateModal));
    editCloseBtn.addEventListener('click', () => closeModal(editModal));
    cancelBtn.addEventListener('click', () => closeModal(rateModal));
    editCancelBtn.addEventListener('click', () => closeModal(editModal));

    window.addEventListener('click', (e) => {
        if (e.target === rateModal) closeModal(rateModal);
        if (e.target === editModal) closeModal(editModal);
    });

    brandFilter.addEventListener('change', () => filterRates());
    rateForm.addEventListener('submit', handleAddRate);
    editForm.addEventListener('submit', handleEditRate);
}

// API Calls
async function loadRates() {
    try {
        const response = await fetch(`${API_BASE_URL}/rates`);
        if (!response.ok) throw new Error('Failed to fetch rates');

        allRates = await response.json();
        updateBrandFilter();
        updateStats();
        renderRates(allRates);
    } catch (error) {
        console.error('Error loading rates:', error);
        showNotification('데이터 로드 실패', 'error');
        ratesTableBody.innerHTML = '<tr><td colspan="8" class="loading">데이터 로드 실패</td></tr>';
    }
}

async function createRate(rateData) {
    try {
        const response = await fetch(`${API_BASE_URL}/rates`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(rateData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create rate');
        }

        showNotification('요율이 성공적으로 추가되었습니다', 'success');
        closeModal(rateModal);
        loadRates();
    } catch (error) {
        console.error('Error creating rate:', error);
        showNotification(error.message, 'error');
    }
}

async function updateRate(id, rateData) {
    try {
        const response = await fetch(`${API_BASE_URL}/rates/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(rateData)
        });

        if (!response.ok) throw new Error('Failed to update rate');

        showNotification('요율이 성공적으로 수정되었습니다', 'success');
        closeModal(editModal);
        loadRates();
    } catch (error) {
        console.error('Error updating rate:', error);
        showNotification('요율 수정 실패', 'error');
    }
}

async function deleteRate(id) {
    if (!confirm('정말 이 요율을 삭제하시겠습니까?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/rates/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete rate');

        showNotification('요율이 성공적으로 삭제되었습니다', 'success');
        loadRates();
    } catch (error) {
        console.error('Error deleting rate:', error);
        showNotification('요율 삭제 실패', 'error');
    }
}

// UI Functions
function renderRates(rates) {
    if (rates.length === 0) {
        ratesTableBody.innerHTML = '<tr><td colspan="8" class="loading">데이터가 없습니다</td></tr>';
        return;
    }

    ratesTableBody.innerHTML = rates.map(rate => `
        <tr>
            <td>${rate.id}</td>
            <td>${rate.brand}</td>
            <td>${rate.marketplace}</td>
            <td class="rate-value">${(rate.shipping * 100).toFixed(1)}%</td>
            <td class="rate-value">${(rate.commission * 100).toFixed(1)}%</td>
            <td>${new Date(rate.created_at).toLocaleDateString('ko-KR')}</td>
            <td>${new Date(rate.updated_at).toLocaleDateString('ko-KR')}</td>
            <td class="action-btns">
                <button class="btn btn-edit" onclick="openEditModal(${rate.id})">수정</button>
                <button class="btn btn-delete" onclick="deleteRate(${rate.id})">삭제</button>
            </td>
        </tr>
    `).join('');
}

function updateBrandFilter() {
    const brands = [...new Set(allRates.map(rate => rate.brand))].sort();

    brandFilter.innerHTML = '<option value="">전체 브랜드</option>' +
        brands.map(brand => `<option value="${brand}">${brand}</option>`).join('');
}

function updateStats() {
    document.getElementById('totalRecords').textContent = allRates.length;

    const brands = new Set(allRates.map(rate => rate.brand));
    document.getElementById('totalBrands').textContent = brands.size;

    const marketplaces = new Set(allRates.map(rate => rate.marketplace));
    document.getElementById('totalMarketplaces').textContent = marketplaces.size;
}

function filterRates() {
    const selectedBrand = brandFilter.value;

    if (selectedBrand === '') {
        renderRates(allRates);
    } else {
        const filtered = allRates.filter(rate => rate.brand === selectedBrand);
        renderRates(filtered);
    }
}

function openAddModal() {
    document.getElementById('modalTitle').textContent = '새 요율 추가';
    rateForm.reset();
    rateModal.style.display = 'block';
}

function openEditModal(id) {
    const rate = allRates.find(r => r.id === id);
    if (!rate) return;

    currentEditId = id;
    document.getElementById('editRateId').value = id;
    document.getElementById('editBrand').value = rate.brand;
    document.getElementById('editMarketplace').value = rate.marketplace;
    document.getElementById('editShipping').value = rate.shipping;
    document.getElementById('editCommission').value = rate.commission;

    editModal.style.display = 'block';
}

function closeModal(modal) {
    modal.style.display = 'none';
    currentEditId = null;
}

function handleAddRate(e) {
    e.preventDefault();

    const rateData = {
        brand: document.getElementById('brand').value.trim(),
        marketplace: document.getElementById('marketplace').value.trim(),
        shipping: parseFloat(document.getElementById('shipping').value),
        commission: parseFloat(document.getElementById('commission').value)
    };

    createRate(rateData);
}

function handleEditRate(e) {
    e.preventDefault();

    const rateData = {
        shipping: parseFloat(document.getElementById('editShipping').value),
        commission: parseFloat(document.getElementById('editCommission').value)
    };

    updateRate(currentEditId, rateData);
}

function showNotification(message, type) {
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}
