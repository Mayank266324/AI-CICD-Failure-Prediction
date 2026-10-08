const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

async function request(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status} ${response.statusText}`
    );
  }

  return response.json();
}


export async function getAnalytics() {
  return request("/analytics");
}


export async function getPipelines(limit = 50) {
  return request(`/pipelines?limit=${limit}`);
}


export async function getShapAnalytics() {
  return request("/analytics/shap");
}


export async function getPipeline(id) {
  return request(`/pipelines/${id}`);
}