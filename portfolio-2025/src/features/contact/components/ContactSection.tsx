'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/shared/components/ui/Button'
import { createContactMessage } from '@/shared/lib/supabase'

export function ContactSection() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
    project_interest: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1 }
    )

    const section = document.getElementById('contact')
    if (section) {
      observer.observe(section)
    }

    return () => observer.disconnect()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      // Simulate API call (replace with actual Supabase call)
      await new Promise(resolve => setTimeout(resolve, 2000))

      // For demo, we'll just simulate success
      setIsSubmitted(true)
      setFormData({ name: '', email: '', subject: '', message: '', project_interest: '' })
    } catch (error) {
      console.error('Error submitting form:', error)
      alert('Error sending message. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const contactInfo = [
    { icon: '📧', label: 'Email', value: 'hello@aiportfolio.com', action: 'mailto:hello@aiportfolio.com' },
    { icon: '💼', label: 'LinkedIn', value: 'linkedin.com/in/ai-developer', action: 'https://linkedin.com' },
    { icon: '🐙', label: 'GitHub', value: 'github.com/ai-developer', action: 'https://github.com' },
    { icon: '📍', label: 'Location', value: 'San Francisco, CA', action: null }
  ]

  if (isSubmitted) {
    return (
      <section id="contact" className="min-h-screen bg-gradient-to-br from-background via-secondary-50/5 to-background py-20 flex items-center justify-center">
        <div className="max-w-2xl mx-auto text-center px-6">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5, type: "spring" }}
            className="text-8xl mb-8"
          >
            🎉
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-4xl font-bold mb-4 text-foreground"
          >
            Message Sent Successfully!
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-xl text-foreground/70 mb-8"
          >
            Thank you for reaching out! I'll get back to you within 24 hours.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Button
              variant="gradient"
              onClick={() => setIsSubmitted(false)}
              className="group"
            >
              <span className="flex items-center gap-2">
                <span>✉️</span>
                <span>Send Another Message</span>
              </span>
            </Button>
          </motion.div>
        </div>
      </section>
    )
  }

  return (
    <section id="contact" className="min-h-screen bg-gradient-to-br from-background via-secondary-50/5 to-background py-20 overflow-hidden">
      {/* Background elements */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(15)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-primary-400/30 rounded-full"
            initial={{
              x: Math.random() * 100,
              y: Math.random() * 100,
            }}
            animate={{
              x: Math.random() * 100,
              y: Math.random() * 100,
              opacity: [0.1, 0.6, 0.1],
            }}
            transition={{
              duration: Math.random() * 8 + 8,
              repeat: Infinity,
              ease: "easeInOut",
              delay: Math.random() * 4,
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
              Let's Connect
            </span>
          </h2>
          <p className="text-xl text-foreground/70 max-w-3xl mx-auto">
            Ready to build something amazing together? Whether you have a project in mind or just want to chat about AI and automation, I'd love to hear from you.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-16">
          {/* Contact Form */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={isVisible ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="glass-dark border border-primary-500/20 rounded-2xl p-8">
              <h3 className="text-2xl font-bold mb-6 text-foreground">Send Me a Message</h3>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-foreground font-medium mb-2">
                      Name *
                    </label>
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 bg-foreground/10 border border-foreground/20 rounded-lg text-foreground placeholder-foreground/50 focus:outline-none focus:border-primary-500 focus:bg-foreground/20 transition-colors"
                      placeholder="John Doe"
                    />
                  </div>
                  <div>
                    <label className="block text-foreground font-medium mb-2">
                      Email *
                    </label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 bg-foreground/10 border border-foreground/20 rounded-lg text-foreground placeholder-foreground/50 focus:outline-none focus:border-primary-500 focus:bg-foreground/20 transition-colors"
                      placeholder="john@example.com"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-foreground font-medium mb-2">
                    Subject
                  </label>
                  <input
                    type="text"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    className="w-full px-4 py-3 bg-foreground/10 border border-foreground/20 rounded-lg text-foreground placeholder-foreground/50 focus:outline-none focus:border-primary-500 focus:bg-foreground/20 transition-colors"
                    placeholder="Project Inquiry"
                  />
                </div>

                <div>
                  <label className="block text-foreground font-medium mb-2">
                    Project Interest
                  </label>
                  <select
                    name="project_interest"
                    value={formData.project_interest}
                    onChange={handleChange}
                    className="w-full px-4 py-3 bg-foreground/10 border border-foreground/20 rounded-lg text-foreground focus:outline-none focus:border-primary-500 focus:bg-foreground/20 transition-colors"
                  >
                    <option value="">Select a service</option>
                    <option value="ai-automation">AI Automation Systems</option>
                    <option value="web-development">Web Development</option>
                    <option value="consulting">AI Consulting</option>
                    <option value="custom-solution">Custom Solution</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-foreground font-medium mb-2">
                    Message *
                  </label>
                  <textarea
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows={5}
                    className="w-full px-4 py-3 bg-foreground/10 border border-foreground/20 rounded-lg text-foreground placeholder-foreground/50 focus:outline-none focus:border-primary-500 focus:bg-foreground/20 transition-colors resize-none"
                    placeholder="Tell me about your project..."
                  />
                </div>

                <Button
                  type="submit"
                  size="lg"
                  variant="gradient"
                  disabled={isLoading}
                  className="w-full group relative overflow-hidden"
                >
                  <span className="relative z-10 flex items-center justify-center gap-2">
                    {isLoading ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        <span>Sending...</span>
                      </>
                    ) : (
                      <>
                        <span>🚀</span>
                        <span>Send Message</span>
                      </>
                    )}
                  </span>
                  <div className="absolute inset-0 bg-white/20 transform translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
                </Button>
              </form>
            </div>
          </motion.div>

          {/* Contact Info */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={isVisible ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="space-y-8"
          >
            <div className="glass-dark border border-primary-500/20 rounded-2xl p-8">
              <h3 className="text-2xl font-bold mb-6 text-foreground">Contact Information</h3>
              <div className="space-y-6">
                {contactInfo.map((info, index) => (
                  <motion.div
                    key={index}
                    className="flex items-center gap-4"
                    initial={{ opacity: 0, y: 20 }}
                    animate={isVisible ? { opacity: 1, y: 0 } : {}}
                    transition={{ delay: 0.6 + index * 0.1 }}
                  >
                    <div className="text-2xl">{info.icon}</div>
                    <div className="flex-1">
                      <div className="text-sm text-foreground/60">{info.label}</div>
                      {info.action ? (
                        <a
                          href={info.action}
                          target={info.action?.startsWith('http') ? '_blank' : undefined}
                          rel={info.action?.startsWith('http') ? 'noopener noreferrer' : undefined}
                          className="text-foreground hover:text-primary-400 transition-colors cursor-pointer"
                        >
                          {info.value}
                        </a>
                      ) : (
                        <div className="text-foreground">{info.value}</div>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* AI Assistant Message */}
            <div className="glass-dark border border-primary-500/20 rounded-2xl p-8">
              <div className="flex items-start gap-4">
                <div className="text-4xl animate-pulse">🤖</div>
                <div>
                  <h4 className="text-lg font-bold text-foreground mb-2">AI Assistant Available</h4>
                  <p className="text-foreground/70">
                    Need immediate assistance? My AI assistant is available 24/7 to answer questions about services, pricing, and project timelines.
                  </p>
                  <Button
                    size="sm"
                    variant="outline"
                    className="mt-4 border-primary-500/50 hover:border-primary-400"
                  >
                    Start AI Chat
                  </Button>
                </div>
              </div>
            </div>

            {/* Response Time */}
            <div className="text-center p-6 bg-gradient-to-r from-primary-500/20 to-secondary-500/20 rounded-xl border border-primary-500/30">
              <div className="text-3xl mb-2">⏰</div>
              <h4 className="text-lg font-bold text-foreground mb-1">Average Response Time</h4>
              <p className="text-foreground/70">Less than 24 hours for all inquiries</p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}