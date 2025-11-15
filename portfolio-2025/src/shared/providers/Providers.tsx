'use client'

import { ThemeProvider } from './ThemeProvider'
import { FontProvider } from './FontProvider'
import { AnalyticsProvider } from './AnalyticsProvider'
import { ReactNode } from 'react'

interface ProvidersProps {
  children: ReactNode
}

export function Providers({ children }: ProvidersProps) {
  return (
    <AnalyticsProvider>
      <FontProvider>
        <ThemeProvider defaultTheme="dark">
          {children}
        </ThemeProvider>
      </FontProvider>
    </AnalyticsProvider>
  )
}