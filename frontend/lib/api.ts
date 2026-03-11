const API_URL = "http://localhost:8000";

export async function uploadFile(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Upload failed");

  return res.json();
}

export async function query(question: string) {
  const res = await fetch(`${API_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: question,
    }),
  });

  if (!res.ok) throw new Error("Query failed");

  return res.json();
}

export async function checkFileSize(files: File[]) {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  const res = await fetch(`${API_URL}/check_size_file`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("File size is invalid ");

  return res.json();
}

export async function deleteFile(fileId: string) {
  const res = await fetch(`${API_URL}/delete_qdrant/${fileId}`, {
    method: "DELETE",
  });

  if (!res.ok) throw new Error("Delete failed");

  return res.json();
}

export async function getAllFiles() {
  const res = await fetch(`${API_URL}/get_all_files`, {
    method: "GET",
  });

  if (!res.ok) throw new Error("Failed to fetch files");

  return res.json();
}

export async function checkContentFile(file: File) {

  const formData = new FormData()
  formData.append("file", file)

  const res = await fetch(`${API_URL}/check_content_file`, {
    method: "POST",
    body: formData
  })

  if (!res.ok) throw new Error("Check content failed")

  const data = await res.json()

  return {
    exists: data.message === "Content file is already ingested"
  }
}

export async function deleteAllFiles() {
  const res = await fetch(`${API_URL}/delete_all_files`, {
    method: "DELETE",
  })

  if (!res.ok) {
    throw new Error("Failed to delete files")
  }

  return res.json()
}

export default { uploadFile, query, checkFileSize, deleteFile, checkContentFile, deleteAllFiles };
