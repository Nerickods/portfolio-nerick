'use client'

import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/shared/components/ui/Button'
import { useTheme } from '@/shared/providers/ThemeProvider'

export function HeroSection() {
  const { theme } = useTheme()
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const [isLoading, setIsLoading] = useState(true)
  const heroRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!heroRef.current) return

      const rect = heroRef.current.getBoundingClientRect()
      const x = ((e.clientX - rect.left) / rect.width - 0.5) * 2
      const y = ((e.clientY - rect.top) / rect.height - 0.5) * 2

      setMousePosition({ x, y })
    }

    window.addEventListener('mousemove', handleMouseMove)

    // Simulate loading completion
    setTimeout(() => setIsLoading(false), 1000)

    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])

  const typewriterTexts = [
    'AI Developer',
    'Automation Expert',
    'Systems Architect',
    'Innovation Driver'
  ]

  const [currentTextIndex, setCurrentTextIndex] = useState(0)
  const [currentText, setCurrentText] = useState('')
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    const text = typewriterTexts[currentTextIndex]
    const timeout = setTimeout(() => {
      if (!isDeleting && currentText.length < text.length) {
        setCurrentText(text.slice(0, currentText.length + 1))
      } else if (isDeleting && currentText.length > 0) {
        setCurrentText(text.slice(0, currentText.length - 1))
      } else if (!isDeleting && currentText.length === text.length) {
        setTimeout(() => setIsDeleting(true), 2000)
      } else if (isDeleting && currentText.length === 0) {
        setIsDeleting(false)
        setCurrentTextIndex((prev) => (prev + 1) % typewriterTexts.length)
      }
    }, isDeleting ? 50 : 150)

    return () => clearTimeout(timeout)
  }, [currentText, isDeleting, currentTextIndex])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="relative w-24 h-24 mx-auto mb-8">
            <div className="absolute inset-0 border-4 border-primary-200 dark:border-primary-800 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-primary-600 rounded-full border-t-transparent animate-spin"></div>
          </div>
          <h2 className="text-2xl font-bold text-foreground animate-pulse">
            Initializing AI Portfolio...
          </h2>
        </div>
      </div>
    )
  }

  return (
    <section
      ref={heroRef}
      className="min-h-screen relative overflow-hidden bg-gradient-to-br from-background via-background to-secondary-50/10 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800/50"
    >
      {/* Animated background particles */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(50)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-primary-400/30 dark:bg-primary-600/30 rounded-full"
            initial={{
              x: Math.random() * 100,
              y: Math.random() * 100,
              scale: 0,
            }}
            animate={{
              x: Math.random() * 100,
              y: Math.random() * 100,
              scale: [0, 1, 0],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: Math.random() * 5 + 5,
              repeat: Infinity,
              ease: "easeInOut",
              delay: Math.random() * 5,
            }}
          />
        ))}
      </div>

      {/* Glass morphism background elements */}
      <div className="absolute inset-0">
        <motion.div
          className="absolute top-20 left-20 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl"
          animate={{
            x: mousePosition.x * 50,
            y: mousePosition.y * 50,
          }}
          transition={{ type: "spring", damping: 50, stiffness: 100 }}
        />
        <motion.div
          className="absolute bottom-20 right-20 w-96 h-96 bg-secondary-500/10 rounded-full blur-3xl"
          animate={{
            x: mousePosition.x * -30,
            y: mousePosition.y * -30,
          }}
          transition={{ type: "spring", damping: 50, stiffness: 100 }}
        />
      </div>

      {/* Main content */}
      <div className="relative z-10 min-h-screen flex items-center justify-center px-6">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            {/* Greeting with glitch effect */}
            <motion.div
              className="mb-6"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              <span className="text-lg md:text-xl font-mono text-primary-600 dark:text-primary-400">
                &lt;/&gt; Hello, I'm
              </span>
            </motion.div>

            {/* Main title with gradient and glow effect */}
            <motion.h1
              className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3, duration: 0.8 }}
            >
              <span className="gradient-text bg-gradient-to-r from-primary-600 via-secondary-500 to-accent-400 bg-clip-text text-transparent animate-pulse">
                AI Developer
              </span>
              <span className="block text-3xl md:text-5xl lg:text-6xl mt-2 text-foreground">
                & Automation Expert
              </span>
            </motion.h1>

            {/* Typewriter effect for roles */}
            <motion.div
              className="h-8 mb-8 flex items-center justify-center"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              <span className="text-xl md:text-2xl font-mono text-foreground/80">
                {currentText}
                <span className="animate-pulse text-primary-500">|</span>
              </span>
            </motion.div>

            {/* Description with AI-themed content */}
            <motion.p
              className="max-w-2xl mx-auto text-lg md:text-xl text-foreground/70 mb-12 leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
            >
              Crafting intelligent automation systems that transform businesses through
              cutting-edge AI solutions. Specializing in machine learning integration,
              workflow optimization, and next-generation web experiences.
            </motion.p>

            {/* Call-to-action buttons */}
            <motion.div
              className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9 }}
            >
              <Button
                size="lg"
                variant="gradient"
                className="group relative overflow-hidden"
                onClick={() => {
                  const element = document.getElementById('projects')
                  element?.scrollIntoView({ behavior: 'smooth' })
                }}
              >
                <span className="relative z-10">View My Work</span>
                <div className="absolute inset-0 bg-white/20 transform translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
              </Button>

              <Button
                size="lg"
                variant="outline"
                className="border-2 border-primary-500/50 hover:border-primary-500 hover:bg-primary-500/10"
                onClick={() => {
                  const element = document.getElementById('contact')
                  element?.scrollIntoView({ behavior: 'smooth' })
                }}
              >
                Get In Touch
              </Button>
            </motion.div>

            {/* Tech stack showcase with animated icons */}
            <motion.div
              className="grid grid-cols-3 md:grid-cols-6 gap-8 max-w-3xl mx-auto"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.1 }}
            >
              {[
                { name: 'React', color: 'text-cyan-400' },
                { name: 'TypeScript', color: 'text-blue-400' },
                { name: 'Python', color: 'text-yellow-400' },
                { name: 'Next.js', color: 'text-gray-100' },
                { name: 'AI/ML', color: 'text-purple-400' },
                { name: 'Node.js', color: 'text-green-400' }
              ].map((tech, index) => (
                <motion.div
                  key={tech.name}
                  className={`flex flex-col items-center ${tech.color}`}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 1.1 + index * 0.1 }}
                  whileHover={{ scale: 1.1, rotate: 5 }}
                >
                  <div className="w-12 h-12 rounded-lg bg-foreground/10 dark:bg-background/50 backdrop-blur-sm border border-foreground/20 dark:border-border flex items-center justify-center mb-2">
                    <div className="w-6 h-6 bg-current rounded-sm" />
                  </div>
                  <span className="text-xs font-medium opacity-70">{tech.name}</span>
                </motion.div>
              ))}
            </motion.div>
          </motion.div>

          {/* Floating AI elements */}
          <motion.div
            className="absolute top-20 right-10 text-4xl animate-bounce"
            animate={{
              y: [0, -20, 0],
              rotate: [0, 5, -5, 0]
            }}
            transition={{ duration: 4, repeat: Infinity }}
          >
            🤖
          </motion.div>

          <motion.div
            className="absolute bottom-20 left-10 text-3xl animate-pulse"
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.5, 1, 0.5]
            }}
            transition={{ duration: 3, repeat: Infinity }}
          >
            ⚡
          </motion.div>

          {/* Neural network animation overlay */}
          <div className="absolute inset-0 pointer-events-none opacity-20">
            <svg className="w-full h-full">
              <defs>
                <linearGradient id="neuralGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.5" />
                  <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.3" />
                  <stop offset="100%" stopColor="#ec4899" stopOpacity="0.1" />
                </linearGradient>
              </defs>
              {[...Array(8)].map((_, i) => (
                <motion.circle
                  key={`node-${i}`}
                  cx={`${20 + i * 10}%`}
                  cy={`${30 + Math.sin(i * 0.8) * 20}%`}
                  r="3"
                  fill="url(#neuralGradient)"
                  animate={{
                    r: [3, 6, 3],
                    opacity: [0.3, 1, 0.3]
                  }}
                  transition={{
                    duration: 2 + i * 0.2,
                    repeat: Infinity,
                    delay: i * 0.3
                  }}
                />
              ))}
              {/* Neural connections */}
              {[...Array(7)].map((_, i) => (
                <motion.line
                  key={`line-${i}`}
                  x1={`${20 + i * 10}%`}
                  y1={`${30 + Math.sin(i * 0.8) * 20}%`}
                  x2={`${30 + i * 10}%`}
                  y2={`${30 + Math.sin((i + 1) * 0.8) * 20}%`}
                  stroke="url(#neuralGradient)"
                  strokeWidth="1"
                  animate={{
                    opacity: [0.1, 0.6, 0.1]
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    delay: i * 0.2
                  }}
                />
              ))}
            </svg>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.5 }}
      >
        <motion.div
          className="w-6 h-10 border-2 border-foreground/30 rounded-full flex justify-center"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <motion.div
            className="w-1 h-3 bg-foreground/60 rounded-full mt-2"
            animate={{ y: [0, 16, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </motion.div>
        <span className="text-xs text-foreground/50 mt-2 block">Scroll to explore</span>
      </motion.div>
    </section>
  )
}