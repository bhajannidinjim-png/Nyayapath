const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const REQUEST_TIMEOUT_MS = Number(
  import.meta.env.VITE_REQUEST_TIMEOUT_MS || 60000
);

async function request(path, options = {}) {
  const controller = new AbortController();

  const timeout = window.setTimeout(
    () => controller.abort(),
    REQUEST_TIMEOUT_MS
  );

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      signal: controller.signal
    });

    if (!response.ok) {
      const body = await response.json().catch(() => ({}));

      throw new Error(body.detail || "Request failed. Please try again.");
    }

    return response.json();
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error(
        "The request took too long. Please retry or upload a smaller PDF."
      );
    }

    throw error;
  } finally {
    window.clearTimeout(timeout);
  }
}

export function uploadJudgment(file) {
  const formData = new FormData();

  formData.append("file", file);

  return request("/judgments/upload", {
    method: "POST",
    body: formData
  });
}

export function getJudgments() {
  return request("/judgments");
}

export function getJudgment(id) {
  return request(`/judgments/${id}`);
}

export function getActions(params = {}) {
  const search = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value) {
      search.append(key, value);
    }
  });

  return request(
    `/api/actions${search.toString() ? `?${search}` : ""}`
  );
}

export function getAction(id) {
  return request(`/api/actions/${id}`);
}

export function verifyAction(id, payload) {
  return request(`/api/actions/${id}/verify`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
}
