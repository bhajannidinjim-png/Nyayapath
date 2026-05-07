const API_BASE_URL =
  "https://nyaypath-production.up.railway.app";

async function request(path, options = {}) {
  const response = await fetch(
    `${API_BASE_URL}${path}`,
    options
  );

  if (!response.ok) {
    throw new Error("Request failed");
  }

  return response.json();
}

export function getActions(status = "approved") {
  return request(`/actions?status=${status}`);
}
