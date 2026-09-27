import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "img2md — Offline Image to Markdown",
  description: "Convert screenshots and images to Markdown, fully offline.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}