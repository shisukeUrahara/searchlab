import type { Metadata, Viewport } from "next";
import { Geist, Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Nav } from "@/components/Nav";
import { ThemeProvider } from "@/components/ThemeProvider";

const inter = Inter({ variable: "--font-inter", subsets: ["latin"] });
const geist = Geist({ variable: "--font-geist", subsets: ["latin"] });
const mono = JetBrains_Mono({ variable: "--font-jetbrains", subsets: ["latin"] });

export const metadata: Metadata = {
  title: { default: "SearchLab", template: "%s · SearchLab" },
  description:
    "Compare BM25, vector and hybrid retrieval over 3,203 chunks of NASA engineering handbooks, with labeled evaluation and an embedding map.",
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f6f4ef" },
    { media: "(prefers-color-scheme: dark)", color: "#0a0f1a" },
  ],
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${inter.variable} ${geist.variable} ${mono.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col">
        <ThemeProvider>
          <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-3 focus:z-50 focus:rounded-lg focus:bg-surface focus:px-3 focus:py-2">
            Skip to content
          </a>
          <Nav />
          <main id="main" className="mx-auto w-full max-w-7xl flex-1 px-4 py-6 md:py-10">
            {children}
          </main>
          <footer className="border-t border-line py-6 text-center text-xs text-muted">
            SearchLab · independent portfolio project · NASA documents are US Government works ·{" "}
            <a className="underline underline-offset-2" href="https://github.com/shisukeUrahara/searchlab">source</a>
          </footer>
        </ThemeProvider>
      </body>
    </html>
  );
}
