import type { Metadata, Viewport } from "next";
import { Providers } from "@/shared/providers/Providers";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "AI Developer Portfolio - Automation Systems Expert",
    template: "%s | AI Portfolio 2025"
  },
  description: "Commercial portfolio showcasing innovative AI automation systems, cutting-edge development solutions, and next-generation technology implementations. Expert in AI-powered workflow optimization and intelligent system design.",
  keywords: [
    "AI Developer",
    "Automation Systems",
    "Machine Learning",
    "Portfolio 2025",
    "Next.js Development",
    "React Applications",
    "TypeScript",
    "AI Solutions",
    "Workflow Automation",
    "Intelligent Systems",
    "Software Development",
    "Full Stack Development"
  ],
  authors: [{ name: "AI Developer" }],
  creator: "AI Developer",
  publisher: "AI Portfolio",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: '/',
    title: 'AI Developer Portfolio - Automation Systems Expert',
    description: 'Commercial portfolio showcasing innovative AI automation systems and cutting-edge development solutions.',
    siteName: 'AI Portfolio 2025',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'AI Developer Portfolio',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AI Developer Portfolio',
    description: 'Innovative AI automation systems and cutting-edge development solutions.',
    images: ['/og-image.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: process.env.GOOGLE_SITE_VERIFICATION,
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#0f172a' }
  ],
  colorScheme: 'dark light',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="theme-color" content="#0f172a" />
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="icon" href="/icon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/site.webmanifest" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body
        className="min-h-screen bg-background font-sans antialiased"
        suppressHydrationWarning
      >
        <div id="root">
          <Providers>
            {children}
          </Providers>
        </div>

        {/* Performance monitoring */}
        {process.env.NODE_ENV === 'development' && (
          <script
            dangerouslySetInnerHTML={{
              __html: `
                if (typeof window !== 'undefined') {
                  window.addEventListener('load', function() {
                    console.log('Page load time:', performance.now());
                  });
                }
              `,
            }}
          />
        )}
      </body>
    </html>
  );
}
