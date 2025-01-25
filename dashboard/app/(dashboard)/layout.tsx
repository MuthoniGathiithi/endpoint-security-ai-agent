"use client";

import "../globals.css";
import { ReactNode } from "react";
import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "@/components/ui/use-toast";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-background text-foreground">
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
          <div className="min-h-screen flex flex-col">
            <main className="flex-1 flex flex-col">{children}</main>
          </div>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
