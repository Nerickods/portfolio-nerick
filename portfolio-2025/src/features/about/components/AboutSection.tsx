'use client'

import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/shared/components/ui/Button'
import { useTheme } from '@/shared/providers/ThemeProvider'

export function AboutSection() {
  const { theme } = useTheme()
  const [isVisible, setIsVisible] = useState(false)
  const sectionRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1 }
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  const skills = [
    { name: 'AI/ML', level: 95, color: 'from-purple-500 to-pink-500' },
    { name: 'React/Next.js', level: 90, color: 'from-blue-500 to-cyan-500' },
    { name: 'TypeScript', level: 88, color: 'from-blue-600 to-indigo-600' },
    { name: 'Python', level: 85, color: 'from-yellow-500 to-orange-500' },
    { name: 'Cloud Architecture', level: 82, color: 'from-green-500 to-teal-500' },
    { name: 'Database Design', level: 78, color: 'from-orange-500 to-red-500' }
  ]

  const achievements = [
    { icon: '🏆', title: '50+ Projects Delivered', description: 'Successfully launched automation solutions' },
    { icon: '⚡', title: '10M+ API Calls', description: 'Handling massive scale with 99.9% uptime' },
    { icon: '🤖', title: 'AI Systems Built', description: 'Custom ML models for business automation' },
    { icon: '🚀', title: 'Performance Expert', description: 'Optimized systems running 10x faster' }
  ]

  return (
    <section ref={sectionRef} className="min-h-screen bg-gradient-to-br from-background via-primary-50/5 to-background py-20 overflow-hidden">
      {/* Background animated elements */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-primary-400/20 rounded-full"
            initial={{
              x: Math.random() * 100,
              y: Math.random() * 100,
            }}
            animate={{
              x: Math.random() * 100,
              y: Math.random() * 100,
              opacity: [0.2, 0.8, 0.2],
              scale: [1, 1.5, 1],
            }}
            transition={{
              duration: Math.random() * 10 + 10,
              repeat: Infinity,
              ease: "easeInOut",
              delay: Math.random() * 5,
            }}
          />
        ))}
      </div>

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        {/* Section Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          animate={isVisible ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            <span className="gradient-text bg-gradient-to-r from-primary-600 via-secondary-500 to-accent-400 bg-clip-text text-transparent">
              About Me
            </span>
          </h2>
          <p className="text-xl text-foreground/70 max-w-3xl mx-auto">
            Passionate AI Developer and Automation Architect building the future of intelligent systems.
          </p>
        </motion.div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Left Column - Text Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={isVisible ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="space-y-8">
              {/* Introduction */}
              <div>
                <h3 className="text-3xl font-bold mb-4 text-foreground">
                  Crafting Intelligent Solutions
                </h3>
                <p className="text-lg text-foreground/80 leading-relaxed mb-4">
                  I'm an AI Developer and Automation Architect with a passion for transforming complex challenges into elegant, intelligent solutions. My expertise spans from machine learning algorithms to scalable web applications.
                </p>
                <p className="text-lg text-foreground/80 leading-relaxed">
                  With over 5 years of experience in developing cutting-edge automation systems, I help businesses leverage artificial intelligence to streamline operations, reduce costs, and unlock new possibilities.
                </p>
              </div>

              {/* Call to Action */}
              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  size="lg"
                  variant="gradient"
                  className="flex items-center gap-2"
                  onClick={() => {
                    const element = document.getElementById('contact')
                    element?.scrollIntoView({ behavior: 'smooth' })
                  }}
                >
                  <span>💼</span>
                  Let's Work Together
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="border-2 border-primary-500/50 hover:border-primary-400"
                  onClick={() => window.open('/resume.pdf', '_blank')}
                >
                  <span>📄</span>
                  Download Resume
                </Button>
              </div>
            </div>
          </motion.div>

          {/* Right Column - Skills & Visual Elements */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={isVisible ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            {/* Skills Chart */}
            <div className="glass-dark border border-primary-500/20 rounded-2xl p-8 mb-8">
              <h4 className="text-2xl font-bold mb-6 text-foreground">Technical Skills</h4>
              <div className="space-y-4">
                {skills.map((skill, index) => (
                  <motion.div
                    key={skill.name}
                    initial={{ opacity: 0, y: 20 }}
                    animate={isVisible ? { opacity: 1, y: 0 } : {}}
                    transition={{ delay: 0.6 + index * 0.1 }}
                  >
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-foreground font-medium">{skill.name}</span>
                      <span className="text-foreground/70 text-sm">{skill.level}%</span>
                    </div>
                    <div className="w-full bg-foreground/10 rounded-full h-3 overflow-hidden">
                      <motion.div
                        className={`h-full bg-gradient-to-r ${skill.color} rounded-full`}
                        initial={{ width: 0 }}
                        animate={isVisible ? { width: `${skill.level}%` } : {}}
                        transition={{ delay: 0.8 + index * 0.1, duration: 1, ease: "easeOut" }}
                      />
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* AI Brain Animation */}
            <div className="relative h-64 glass-dark border border-primary-500/20 rounded-2xl p-8 flex items-center justify-center">
              <div className="text-center">
                <motion.div
                  className="text-6xl mb-4"
                  animate={{
                    rotate: [0, 10, -10, 0],
                    scale: [1, 1.1, 1],
                  }}
                  transition={{
                    duration: 4,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                >
                  🧠
                </motion.div>
                <h4 className="text-xl font-bold text-foreground mb-2">AI-Powered Mindset</h4>
                <p className="text-foreground/70">Continuously learning and adapting</p>
              </div>

              {/* Neural network overlay */}
              <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-20">
                {[...Array(6)].map((_, i) => (
                  <motion.circle
                    key={`brain-node-${i}`}
                    cx={`${20 + i * 15}%`}
                    cy={`${30 + Math.sin(i * 1.2) * 20}%`}
                    r="2"
                    fill="url(#brainGradient)"
                    animate={{
                      r: [2, 4, 2],
                      opacity: [0.3, 1, 0.3]
                    }}
                    transition={{
                      duration: 2 + i * 0.3,
                      repeat: Infinity,
                      delay: i * 0.2
                    }}
                  />
                ))}
                <defs>
                  <linearGradient id="brainGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.8" />
                    <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.8" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </motion.div>
        </div>

        {/* Achievements Grid */}
        <motion.div
          className="mt-20"
          initial={{ opacity: 0, y: 30 }}
          animate={isVisible ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          <h3 className="text-3xl font-bold text-center mb-12 text-foreground">Key Achievements</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {achievements.map((achievement, index) => (
              <motion.div
                key={index}
                className="glass-dark border border-primary-500/20 rounded-xl p-6 text-center hover:border-primary-500/50 transition-all duration-300 group"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={isVisible ? { opacity: 1, scale: 1 } : {}}
                transition={{ delay: 0.8 + index * 0.1 }}
                whileHover={{ y: -5, scale: 1.05 }}
              >
                <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">
                  {achievement.icon}
                </div>
                <h4 className="text-lg font-bold text-foreground mb-2">{achievement.title}</h4>
                <p className="text-foreground/70 text-sm">{achievement.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}