const API = process.env.NEXT_PUBLIC_API ?? "http://127.0.0.1:8000";

export type ConvertResponse = {
  file_id: string;
  markdown: string;
  line_count: number;
};

export async function imageToMarkdown(
  file: File,
  lang = "eng"
): Promise<ConvertResponse> {
  const fd = new FormData();
  fd.append("file", file);
  fd.append("lang", lang);

  const res = await fetch(`${API}/api/image-to-markdown`, {
    method: "POST",
    body: fd,
  });

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`HTTP ${res.status}: ${txt}`);
  }
  return res.json();
}

export const downloadUrl = (id: string) => `${API}/api/download/${id}`;