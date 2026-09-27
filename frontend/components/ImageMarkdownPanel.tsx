"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Copy, Download, Loader2, Check, UploadCloud } from "lucide-react";
import { imageToMarkdown, downloadUrl } from "@/lib/api";

type Tab = "preview" | "edit";

export default function ImageMarkdownPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>("");
  const [md, setMd] = useState("");
  const [fileId, setFileId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<Tab>("preview");
  const [copied, setCopied] = useState(false);

  const run = useCallback(async (f: File) => {
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setMd("");
    setFileId(null);
    setError(null);
    setLoading(true);
    setTab("preview");
    try {
      const res = await imageToMarkdown(f);
      setMd(res.markdown);
      setFileId(res.file_id);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : String(e);
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  const onDrop = useCallback(
    (accepted: File[]) => {
      if (accepted[0]) run(accepted[0]);
    },
    [run]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/png": [".png"],
      "image/jpeg": [".jpg", ".jpeg"],
      "image/webp": [".webp"],
      "image/tiff": [".tiff", ".tif"],
    },
    multiple: false,
  });

  const copyMd = async () => {
    await navigator.clipboard.writeText(md);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const reset = () => {
    setFile(null);
    setPreview("");
    setMd("");
    setFileId(null);
    setError(null);
  };

  return (
    <div className="grid lg:grid-cols-2 gap-4">
      <div className="rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-4 min-h-[400px] flex flex-col">
        {preview ? (
          <div className="flex-1 flex items-center justify-center overflow-auto">
            <img
              src={preview}
              alt="uploaded"
              className="max-w-full max-h-[70vh] rounded-lg shadow-sm"
            />
          </div>
        ) : (
          <div
            {...getRootProps()}
            className={`flex-1 flex flex-col items-center justify-center border-2 border-dashed rounded-xl cursor-pointer transition ${
              isDragActive
                ? "border-blue-500 bg-blue-50 dark:bg-blue-950/30"
                : "border-zinc-300 dark:border-zinc-700 hover:border-zinc-400"
            }`}
          >
            <input {...getInputProps()} />
            <UploadCloud className="w-10 h-10 text-zinc-400 mb-3" />
            <p className="text-sm text-zinc-600 dark:text-zinc-400">
              {isDragActive
                ? "Drop the image here…"
                : "Drop an image or click to browse"}
            </p>
            <p className="text-xs text-zinc-400 mt-1">
              PNG, JPG, WEBP, TIFF · max 20 MB
            </p>
          </div>
        )}

        {file && (
          <div className="mt-3 flex items-center justify-between text-sm text-zinc-500">
            <span className="truncate">{file.name}</span>
            <button
              onClick={reset}
              className="text-zinc-500 hover:text-red-500 ml-3"
            >
              Clear
            </button>
          </div>
        )}
      </div>

      <div className="rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 flex flex-col min-h-[400px]">
        <div className="flex items-center justify-between border-b border-zinc-200 dark:border-zinc-800 px-4 py-2">
          <div className="flex gap-1">
            <TabButton
              active={tab === "preview"}
              onClick={() => setTab("preview")}
            >
              Preview
            </TabButton>
            <TabButton active={tab === "edit"} onClick={() => setTab("edit")}>
              Edit
            </TabButton>
          </div>

          <div className="flex gap-1">
            <IconBtn onClick={copyMd} disabled={!md} title="Copy markdown">
              {copied ? <Check size={16} /> : <Copy size={16} />}
            </IconBtn>
            {fileId && (
              <a
                href={downloadUrl(fileId)}
                className="p-2 rounded hover:bg-zinc-100 dark:hover:bg-zinc-800"
                title="Download .md"
              >
                <Download size={16} />
              </a>
            )}
          </div>
        </div>

        <div className="flex-1 overflow-auto">
          {loading && (
            <div className="h-full flex flex-col items-center justify-center gap-3 text-zinc-500">
              <Loader2 className="animate-spin" />
              <span className="text-sm">Running OCR…</span>
            </div>
          )}

          {!loading && error && (
            <div className="p-4 text-sm text-red-600 dark:text-red-400 whitespace-pre-wrap">
              <strong>Error:</strong> {error}
            </div>
          )}

          {!loading && !error && !md && (
            <div className="h-full flex items-center justify-center text-sm text-zinc-400">
              Markdown will appear here
            </div>
          )}

          {!loading && !error && md && tab === "preview" && (
            <article className="prose prose-zinc dark:prose-invert max-w-none p-4">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{md}</ReactMarkdown>
            </article>
          )}

          {!loading && !error && md && tab === "edit" && (
            <textarea
              value={md}
              onChange={(e) => setMd(e.target.value)}
              className="w-full h-full p-4 font-mono text-sm bg-transparent resize-none outline-none"
              spellCheck={false}
            />
          )}
        </div>
      </div>
    </div>
  );
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1.5 text-sm rounded-md transition ${
        active
          ? "bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 font-medium"
          : "text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100"
      }`}
    >
      {children}
    </button>
  );
}

function IconBtn({
  onClick,
  disabled,
  title,
  children,
}: {
  onClick: () => void;
  disabled?: boolean;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      title={title}
      className="p-2 rounded hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-40 disabled:cursor-not-allowed"
    >
      {children}
    </button>
  );
}