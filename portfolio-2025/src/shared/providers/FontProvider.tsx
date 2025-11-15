'use client'

import { ReactNode, useEffect } from 'react'

interface FontProviderProps {
  children: ReactNode
}

export function FontProvider({ children }: FontProviderProps) {
  useEffect(() => {
    // Load Inter and JetBrains Mono fonts from Google Fonts
    const linkInter = document.createElement('link')
    linkInter.href = 'https://fonts.googleapis.com/css2?family=Inter:slnt,wght@-10..0,100..900&display=swap'
    linkInter.rel = 'stylesheet'

    const linkJetBrains = document.createElement('link')
    linkJetBrains.href = 'https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap'
    linkJetBrains.rel = 'stylesheet'

    // Add fonts to head
    document.head.appendChild(linkInter)
    document.head.appendChild(linkJetBrains)

    // Cleanup
    return () => {
      if (document.head.contains(linkInter)) {
        document.head.removeChild(linkInter)
      }
      if (document.head.contains(linkJetBrains)) {
        document.head.removeChild(linkJetBrains)
      }
    }
  }, [])

  return <>{children}</>
}