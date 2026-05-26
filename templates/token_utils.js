/**
 * Token Management Utils
 * Xử lý lưu/lấy tokens từ localStorage
 */

// ============================================================
// 1. LƯỚI TOKEN
// ============================================================
function saveTokens(accessToken, refreshToken, userRole, userId, userName) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
    localStorage.setItem('user_role', userRole);
    localStorage.setItem('user_id', userId);
    localStorage.setItem('user_name', userName);
    localStorage.setItem('token_saved_at', new Date().toISOString());
}

// ============================================================
// 2. LẤY TOKENS
// ============================================================
function getAccessToken() {
    return localStorage.getItem('access_token');
}

function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

function getUserRole() {
    return localStorage.getItem('user_role');
}

function getUserId() {
    return localStorage.getItem('user_id');
}

function getUserName() {
    return localStorage.getItem('user_name');
}

// ============================================================
// 3. XÓA TOKENS (LOGOUT)
// ============================================================
function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_name');
    localStorage.removeItem('token_saved_at');
}

// ============================================================
// 4. KIỂM TRA CÓ TOKEN KHÔNG
// ============================================================
function hasAccessToken() {
    return !!localStorage.getItem('access_token');
}

function isAuthenticated() {
    return hasAccessToken();
}

// ============================================================
// 5. HEADER AUTHORIZATION
// ============================================================
function getAuthHeader() {
    const token = getAccessToken();
    if (token) {
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }
    return {
        'Content-Type': 'application/json'
    };
}

// ============================================================
// 6. REFRESH TOKEN (KHI TOKEN HẾT HẠN)
// ============================================================
async function refreshAccessToken() {
    const refreshToken = getRefreshToken();
    if (!refreshToken) return false;

    try {
        const response = await fetch('/api/xac-thuc/refresh/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return true;
        } else {
            // Refresh token expired - redirect to login
            clearTokens();
            window.location.href = '/';
            return false;
        }
    } catch (error) {
        console.error('Token refresh failed:', error);
        clearTokens();
        window.location.href = '/';
        return false;
    }
}

// ============================================================
// 7. FETCH WITH AUTO-REFRESH (RECOMMENDED)
// ============================================================
async function fetchWithAuth(url, options = {}) {
    let headers = getAuthHeader();
    
    // Merge custom headers
    if (options.headers) {
        headers = { ...headers, ...options.headers };
    }
    
    let response = await fetch(url, { ...options, headers });
    
    // If 401 → try refresh token
    if (response.status === 401) {
        const refreshed = await refreshAccessToken();
        if (refreshed) {
            headers = getAuthHeader();
            response = await fetch(url, { ...options, headers });
        }
    }
    
    return response;
}

// ============================================================
// 8. LOGOUT
// ============================================================
async function logout() {
    const refreshToken = getRefreshToken();
    
    try {
        // Gọi API logout để blacklist token
        if (refreshToken) {
            await fetch('/api/xac-thuc/logout/', {
                method: 'POST',
                headers: getAuthHeader(),
                body: JSON.stringify({ refresh_token: refreshToken })
            });
        }
    } catch (error) {
        console.error('Logout API error:', error);
    }
    
    // Xóa tokens khỏi localStorage
    clearTokens();
    
    // Redirect to login
    window.location.href = '/';
}

// ============================================================
// 9. CHECK ROLE
// ============================================================
function hasRole(requiredRole) {
    const userRole = getUserRole();
    return userRole === requiredRole;
}

function hasAnyRole(requiredRoles) {
    const userRole = getUserRole();
    return requiredRoles.includes(userRole);
}

// ============================================================
// 10. AUTO-LOGOUT ON STARTUP (IF TOKEN MISSING)
// ============================================================
function checkAuthOnPageLoad() {
    // Chỉ check trên public pages (login page không cần)
    const isLoginPage = window.location.pathname === '/' || window.location.pathname === '/login/';
    
    if (!isLoginPage && !isAuthenticated()) {
        window.location.href = '/';
    }
}

// Tự động check khi page load
document.addEventListener('DOMContentLoaded', checkAuthOnPageLoad);
