import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Jay AI",
  description: "감정이 있는 AI 봇 만들기",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
      return (
            <html lang="ko" className={`${geistSans.variable} ${geistMono.variable}`}>
                  <body>{children}</body>
            </html>
      );
}
