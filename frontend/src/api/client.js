/**
 * Centralized API Client for DriveShare
 *
 * All HTTP requests to the FastAPI backend go through this module.
 * The client automatically attaches the X-Auth-Token header from
 * localStorage for authenticated requests.
 */

const BASE = '/api';

/**
 * Internal helper that performs a fetch and normalises the response.
 * @param {string} path  - API path (e.g. "/auth/login")
 * @param {object} opts  - fetch options (method, body, etc.)
 * @returns {Promise<{ok: boolean, data: any, error: string|null}>}
 */
async function request(path, opts = {}) {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json', ...opts.headers };
  if (token) headers['X-Auth-Token'] = token;

  try {
    const res = await fetch(`${BASE}${path}`, { ...opts, headers });
    const data = await res.json().catch(() => null);
    if (!res.ok) {
      return { ok: false, data: null, error: data?.detail || res.statusText };
    }
    return { ok: true, data, error: null };
  } catch (err) {
    return { ok: false, data: null, error: err.message };
  }
}

/** GET request */
export function get(path) {
  return request(path, { method: 'GET' });
}

/** POST request with JSON body */
export function post(path, body) {
  return request(path, { method: 'POST', body: JSON.stringify(body) });
}

/** PUT request with JSON body */
export function put(path, body) {
  return request(path, { method: 'PUT', body: JSON.stringify(body) });
}

/** DELETE request */
export function del(path) {
  return request(path, { method: 'DELETE' });
}
