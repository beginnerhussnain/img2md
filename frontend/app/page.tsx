import ImageMarkdownPanel from "@/components/ImageMarkdownPanel";

export default function Home() {
  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100">
      <header className="border-b border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-900/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-sm font-bold">
              M
            </div>
            <div>
              <h1 className="font-semibold leading-none">img2md</h1>
              <p className="text-xs text-zinc-500 mt-0.5">
                Offline image → Markdown
              </p>
            </div>
          </div>
          <span className="text-xs text-zinc-500 hidden sm:block">
            Local OCR · files auto-deleted in 30 min
          </span>
        </div>
      </header>

      <section className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold">
            Convert an image to Markdown
          </h2>
          <p className="text-sm text-zinc-500 mt-1">
            Drop a screenshot, photo, or scan. Everything runs on your machine.
          </p>
        </div>

        <ImageMarkdownPanel />
      </section>

      <footer className="max-w-7xl mx-auto px-6 py-8 text-xs text-zinc-400">
        Built with FastAPI + Tesseract + Next.js
      </footer>
    </main>
  );
}