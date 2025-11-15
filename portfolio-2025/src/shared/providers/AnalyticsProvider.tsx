'use client'

import { useEffect } from 'react'
import { ReactNode } from 'react'

interface AnalyticsProviderProps {
  children: ReactNode
}

export function AnalyticsProvider({ children }: AnalyticsProviderProps) {
  useEffect(() => {
    // Initialize Google Analytics if configured
    if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_GA_ID) {
      // Load gtag script
      const script = document.createElement('script')
      script.async = true
      script.src = `https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`
      document.head.appendChild(script)

      // Initialize gtag
      const inlineScript = document.createElement('script')
      inlineScript.innerHTML = `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}');
      `
      document.head.appendChild(inlineScript)
    }

    // Initialize Vercel Analytics if configured
    // Note: This will be handled by the @vercel/analytics package if installed
    // We're using a conditional load approach here to avoid build errors
    if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_VERCEL_ANALYTICS_ID) {
      // Manual Vercel Analytics implementation when package is available
      // In production, this should be handled by the actual @vercel/analytics package
      console.log('Vercel Analytics configured')
    }
  }, [])

  return <>{children}</>
}