'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/shared/components/ui/Button'

export function Footer() {
  const [currentYear] = useState(new Date().getFullYear())

  const socialLinks = [
    { name: 'GitHub', icon: '🐙', url: 'https://github.com' },
    { name: 'LinkedIn', icon: '💼', url: 'https://linkedin.com' },
    { name: 'Twitter', icon: '🐦', url: 'https://twitter.com' },
    { name: 'Email', icon: '📧', url: 'mailto:hello@aiportfolio.com' }
  ]

  const quickLinks = [
    { name: 'About', href: '#about' },
    { name: 'Projects', href: '#projects' },
    { name: 'Contact', href: '#contact' },
    { name: 'Resume', href: '/resume.pdf' }
  ]

  return (
    <footer className="relative bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 border-t border-primary-500/20 overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(30)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-primary-400/20 rounded-full"
            initial={{
              x: Math.random() * 100,
              y: Math.random() * 100,
            }}
            animate={{
              x: Math.random() * 100,
              y: Math.random() * 100,
              opacity: [0.1, 0.5, 0.1],
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

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-16">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {/* Brand Section */}
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="flex items-center gap-3">
              <div className="text-3xl">🤖</div>
              <h3 className="text-xl font-bold gradient-text bg-gradient-to-r from-primary-400 to-secondary-400 bg-clip-text text-transparent">
                AI Portfolio
              </h3>
            </div>
            <p className="text-foreground/70 leading-relaxed">
              Building the future with intelligent automation systems and cutting-edge AI solutions.
            </p>
            <div className="flex gap-3">
              {socialLinks.map((link) => (
                <motion.a
                  key={link.name}
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 rounded-full bg-foreground/10 hover:bg-primary-500/20 border border-foreground/20 hover:border-primary-500/50 flex items-center justify-center text-xl transition-all duration-300"
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {link.icon}
                </motion.a>
              ))}
            </div>
          </motion.div>

          {/* Quick Links */}
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <h4 className="text-lg font-bold text-foreground">Quick Links</h4>
            <nav className="space-y-2">
              {quickLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  className="block text-foreground/70 hover:text-primary-400 transition-colors duration-200"
                >
                  {link.name}
                </a>
              ))}
            </nav>
          </motion.div>

          {/* Services */}
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h4 className="text-lg font-bold text-foreground">Services</h4>
            <nav className="space-y-2 text-foreground/70">
              <div className="hover:text-primary-400 transition-colors duration-200 cursor-pointer">
                🤖 AI Automation Systems
              </div>
              <div className="hover:text-primary-400 transition-colors duration-200 cursor-pointer">
                🚀 Web Development
              </div>
              <div className="hover:text-primary-400 transition-colors duration-200 cursor-pointer">
                🧠 Machine Learning Solutions
              </div>
              <div className="hover:text-primary-400 transition-colors duration-200 cursor-pointer">
                ☁️ Cloud Architecture
              </div>
            </nav>
          </motion.div>

          {/* CTA Section */}
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <h4 className="text-lg font-bold text-foreground">Ready to Build?</h4>
            <p className="text-foreground/70 text-sm">
              Let's discuss how AI can transform your business operations.
            </p>
            <Button
              variant="gradient"
              size="sm"
              className="w-full group"
              onClick={() => {
                const element = document.getElementById('contact')
                element?.scrollIntoView({ behavior: 'smooth' })
              }}
            >
              <span className="flex items-center justify-center gap-2">
                <span>💬</span>
                <span>Start Conversation</span>
              </span>
            </Button>
          </motion.div>
        </div>

        {/* Divider */}
        <div className="border-t border-foreground/10 mb-8" />

        {/* Bottom Section */}
        <motion.div
          className="flex flex-col md:flex-row justify-between items-center gap-4"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-foreground/60 text-sm">
            © {currentYear} AI Portfolio. Crafted with{' '}
            <span className="text-red-500 animate-pulse">❤️</span>{' '}
            and lots of{' '}
            <span className="text-primary-400">☕</span>
          </div>

          <div className="flex items-center gap-6 text-sm text-foreground/60">
            <div className="flex items-center gap-2">
              <span>⚡</span>
              <span>Powered by Next.js 16</span>
            </div>
            <div className="flex items-center gap-2">
              <span>🎨</span>
              <span>Designed with AI</span>
            </div>
          </div>
        </motion.div>

        {/* Floating AI Bot */}
        <motion.div
          className="fixed bottom-8 right-8 z-50"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 2, type: "spring" }}
        >
          <Button
            size="lg"
            variant="gradient"
            className="w-14 h-14 rounded-full p-0 relative overflow-hidden group"
          >
            <span className="text-2xl absolute inset-0 flex items-center justify-center">
              🤖
            </span>
            <div className="absolute inset-0 bg-white/20 transform translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
          </Button>
          <motion.div
            className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-slate-900"
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </motion.div>
      </div>
    </footer>
  )
}