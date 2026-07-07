"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Terminal, Cpu, Network, Database, Brain, Globe, Mail, 
  Code, CloudSun, MapPin, Search, Calendar, 
  FileText, Compass, Server, Check, ArrowRight, Play, 
  Eye, BookOpen, Layers, History, ArrowDown
} from "lucide-react";
import Link from "next/link";

// Custom SVG component for Github to avoid dependency version export bugs
const GithubIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    viewBox="0 0 24 24"
    width="24"
    height="24"
    stroke="currentColor"
    strokeWidth="2"
    fill="none"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
  </svg>
);

// -------------------------------------------------------------
// Interactive Particle Starfield Background
// -------------------------------------------------------------
function StarField() {
  const [stars, setStars] = useState<{ id: number; top: number; left: number; delay: number; duration: number }[]>([]);

  useEffect(() => {
    // Generate stars dynamically on the client to avoid SSR mismatch
    const generatedStars = Array.from({ length: 80 }).map((_, i) => ({
      id: i,
      top: Math.random() * 100,
      left: Math.random() * 100,
      delay: Math.random() * 5,
      duration: 3 + Math.random() * 4
    }));
    setStars(generatedStars);
  }, []);

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
      {stars.map((star) => (
        <div
          key={star.id}
          className="absolute w-[2px] h-[2px] bg-white rounded-full"
          style={{
            top: `${star.top}%`,
            left: `${star.left}%`,
            animation: `twinkle ${star.duration}s ease-in-out infinite`,
            animationDelay: `${star.delay}s`,
            boxShadow: "0 0 4px rgba(255, 255, 255, 0.8)",
          }}
        />
      ))}
      <style jsx global>{`
        @keyframes twinkle {
          0%, 100% { opacity: 0.15; transform: scale(0.8); }
          50% { opacity: 1; transform: scale(1.3); }
        }
      `}</style>
    </div>
  );
}

export default function Home() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth - 0.5) * 30,
        y: (e.clientY / window.innerHeight - 0.5) * 30,
      });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  // Section Title Component
  const SectionHeader = ({ tag, title, subtitle }: { tag: string; title: string; subtitle: string }) => (
    <div className="flex flex-col items-center text-center mb-16 relative z-10">
      <motion.span 
        initial={{ opacity: 0, y: 15 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="px-3 py-1 text-xs font-semibold tracking-widest text-[#e056fd] uppercase bg-[#e056fd]/10 border border-[#e056fd]/30 rounded-full mb-4 shadow-[0_0_15px_rgba(224,86,253,0.1)]"
      >
        {tag}
      </motion.span>
      <motion.h2 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.1 }}
        className="text-4xl md:text-5xl font-bold tracking-tight text-white mb-4 bg-clip-text text-transparent bg-gradient-to-r from-white via-zinc-200 to-zinc-500"
      >
        {title}
      </motion.h2>
      <motion.p 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.2 }}
        className="max-w-2xl text-zinc-400 text-lg leading-relaxed"
      >
        {subtitle}
      </motion.p>
    </div>
  );

  return (
    <div className="relative min-h-screen bg-[#050505] text-white overflow-hidden font-sans noise-bg selection:bg-[#e056fd]/30 selection:text-white">
      {/* -------------------------------------------------------------
          BACKGROUND NEBULAS & GRID OVERLAYS
          ------------------------------------------------------------- */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        {/* Glow Nebula 1 (Blue) */}
        <div className="absolute top-[-10%] left-[-10%] w-[60%] h-[60%] rounded-full bg-gradient-to-br from-blue-600/15 to-transparent blur-[120px] animate-pulse-slow" />
        
        {/* Glow Nebula 2 (Purple) */}
        <div className="absolute bottom-[-10%] right-[-10%] w-[65%] h-[65%] rounded-full bg-gradient-to-tr from-[#e056fd]/15 to-transparent blur-[140px] animate-pulse-slow" style={{ animationDelay: "2s" }} />

        {/* Ambient Center Glow */}
        <div className="absolute top-[35%] left-[30%] w-[40%] h-[40%] rounded-full bg-indigo-500/5 blur-[160px]" />

        {/* Fine Neon Grid Overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff03_1px,transparent_1px),linear-gradient(to_bottom,#ffffff03_1px,transparent_1px)] bg-[size:32px_32px] opacity-75" />
      </div>

      <StarField />

      {/* -------------------------------------------------------------
          1. HERO SECTION (Apple + Cyberpunk Aesthetic)
          ------------------------------------------------------------- */}
      <section className="relative min-h-screen flex flex-col justify-center items-center px-6 pt-20 pb-16 z-10">
        <div className="max-w-7xl w-full grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Column: Hero Texts */}
          <div className="lg:col-span-7 flex flex-col justify-center text-center lg:text-left">
            {/* Tag Badge */}
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="inline-flex self-center lg:self-start items-center gap-2 px-3 py-1.5 rounded-full border border-zinc-800 bg-[#0d0d11]/80 backdrop-blur-md text-xs font-medium text-zinc-300 mb-8 hover:border-zinc-700 transition-all cursor-pointer shadow-[0_4px_12px_rgba(0,0,0,0.5)]"
            >
              <span className="flex h-2 w-2 rounded-full bg-[#e056fd] animate-pulse" />
              <span>Version 1.0 Now Available</span>
              <ArrowRight className="w-3.5 h-3.5 text-[#e056fd]" />
            </motion.div>

            {/* Headline */}
            <motion.h1 
              initial={{ opacity: 0, y: 25 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-6xl md:text-8xl font-extrabold tracking-tight text-white mb-4 leading-[1.1]"
            >
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#e056fd] via-indigo-400 to-[#00d2ff] animate-text-shine">
                Nexus-AI
              </span>
              <br />
              <span className="text-2xl md:text-4xl text-zinc-300 font-semibold tracking-tight mt-2 block">
                Universal Personal Smart System
              </span>
            </motion.h1>

            {/* Subtitle */}
            <motion.p 
              initial={{ opacity: 0, y: 25 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="max-w-xl text-zinc-400 text-lg md:text-xl leading-relaxed mb-10 mx-auto lg:mx-0"
            >
              Plan, reason, execute, automate, and collaborate using autonomous AI agents powered by a unified local memory layer.
            </motion.p>

            {/* Action Buttons */}
            <motion.div 
              initial={{ opacity: 0, y: 25 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start items-center mb-12"
            >
              <Link href="/login">
                <button className="relative group overflow-hidden px-8 py-4 rounded-full font-bold text-white bg-gradient-to-r from-[#e056fd] to-[#be2edd] transition-all hover:scale-105 active:scale-95 shadow-[0_0_30px_rgba(224,86,253,0.3)] hover:shadow-[0_0_40px_rgba(224,86,253,0.5)]">
                  <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 skew-y-12 transition-transform duration-500 origin-bottom" />
                  <span className="relative flex items-center gap-2">
                    Get Started Free <ArrowRight className="w-5 h-5" />
                  </span>
                </button>
              </Link>
              
              <a href="/downloads/nexus-ai.apk" download>
                <button className="flex items-center gap-2 px-6 py-4 rounded-full font-bold border border-green-500/20 bg-green-500/5 hover:bg-green-500/10 hover:border-green-500/40 text-green-400 backdrop-blur-md transition-all hover:scale-105 active:scale-95 shadow-[0_0_15px_rgba(34,197,94,0.1)]">
                  <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M17.523 15.3l1.816 3.146a.5.5 0 1 1-.866.5l-1.833-3.177a11.1 11.1 0 0 1-9.28 0L5.527 18.95a.5.5 0 1 1-.866-.5L6.477 15.3C3.076 13.565 1 10.057 1 6h22c0 4.057-2.076 13.565-5.477 9.3zM7 9a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm10 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
                  </svg>
                  Download APK
                </button>
              </a>

              <a href="/downloads/nexus-ai-extension.vsix" download>
                <button className="flex items-center gap-2 px-6 py-4 rounded-full font-bold border border-blue-500/20 bg-blue-500/5 hover:bg-blue-500/10 hover:border-blue-500/40 text-blue-400 backdrop-blur-md transition-all hover:scale-105 active:scale-95 shadow-[0_0_15px_rgba(59,130,246,0.1)]">
                  <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Download VSIX
                </button>
              </a>

              <a href="#features">
                <button className="flex items-center gap-2 px-6 py-4 rounded-full font-bold border border-zinc-800 bg-[#0c0c10]/40 hover:bg-[#12121a]/60 hover:border-zinc-700 backdrop-blur-md transition-all hover:scale-105 active:scale-95">
                  <Play className="w-4 h-4 fill-white text-white" />
                  Watch Demo
                </button>
              </a>
            </motion.div>

            {/* Trust Badges */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="flex flex-wrap gap-x-8 gap-y-4 justify-center lg:justify-start items-center border-t border-zinc-900/60 pt-8"
            >
              <span className="text-zinc-600 text-xs font-semibold uppercase tracking-wider">Trusted Integration Technologies</span>
              <div className="flex gap-4 items-center opacity-40 hover:opacity-60 transition-opacity">
                <Database className="w-5 h-5" /> <span className="font-semibold text-sm">Postgres</span>
              </div>
              <div className="flex gap-4 items-center opacity-40 hover:opacity-60 transition-opacity">
                <Server className="w-5 h-5" /> <span className="font-semibold text-sm">FastAPI</span>
              </div>
              <div className="flex gap-4 items-center opacity-40 hover:opacity-60 transition-opacity">
                <Cpu className="w-5 h-5" /> <span className="font-semibold text-sm">LLaMA 3</span>
              </div>
            </motion.div>
          </div>

          {/* Right Column: Dynamic Abstract 3D UI & Orbit Simulation */}
          <div className="lg:col-span-5 relative flex justify-center items-center py-12 lg:py-0">
            {/* Animated Sphere Container with Mouse Parallax */}
            <motion.div 
              style={{
                transform: `translate3d(${mousePosition.x}px, ${mousePosition.y}px, 0)`,
              }}
              transition={{ type: "spring", stiffness: 100, damping: 20 }}
              className="relative w-[320px] h-[320px] md:w-[400px] md:h-[400px] flex justify-center items-center"
            >
              {/* Star Core Glow */}
              <div className="absolute w-24 h-24 rounded-full bg-gradient-to-r from-[#e056fd] to-blue-500 blur-2xl opacity-60 animate-pulse-slow" />

              {/* Dhaansu Futuristic Cyber HUD Scanner Overlay */}
              {/* Sweeping Radar Scanner Line */}
              <div className="absolute w-[300px] h-[300px] rounded-full overflow-hidden pointer-events-none" style={{ animation: "rotate-slow 10s linear infinite" }}>
                <div className="w-1/2 h-full bg-gradient-to-r from-[#e056fd]/10 to-transparent origin-right transform rotate-12 blur-sm" />
              </div>

              {/* Outer Glowing Cyber Ring */}
              <div className="absolute w-[340px] h-[340px] rounded-full border-2 border-blue-500/20 border-t-[#e056fd]/40 border-b-[#be2edd]/40 animate-rotate-slow" />

              {/* Inner Pulsing Radar Grid */}
              <div className="absolute w-[260px] h-[260px] rounded-full border border-zinc-800/80 bg-[radial-gradient(circle,rgba(224,86,253,0.04)_1px,transparent_1px)] bg-[size:16px_16px] animate-pulse" />

              {/* Counter Rotating Ring with gaps */}
              <div className="absolute w-[210px] h-[210px] rounded-full border border-dashed border-[#e056fd]/30" style={{ animation: "rotate-slow 15s linear infinite reverse" }} />

              {/* Target Scope Crosshair lines */}
              <div className="absolute w-[320px] h-[1px] bg-zinc-950" />
              <div className="absolute h-[320px] w-[1px] bg-zinc-950" />
              
              {/* Rotating Ring with little notches */}
              <div className="absolute w-[380px] h-[380px] rounded-full border border-zinc-900 border-t-2 border-t-indigo-500/30 animate-rotate-slow" />

              {/* Floating Center Assistant Sphere */}
              <div className="absolute w-36 h-36 rounded-full bg-gradient-to-tr from-[#050505] to-[#121217] border border-zinc-800 flex justify-center items-center shadow-[0_0_50px_rgba(224,86,253,0.15)] animate-float">
                <Brain className="w-16 h-16 text-[#e056fd] drop-shadow-[0_0_10px_rgba(224,86,253,0.6)]" />
              </div>

              {/* Floating Task Feedback Status Cards */}
              {/* Card 1: Email Sent */}
              <motion.div 
                initial={{ opacity: 0, x: -30, y: -40 }}
                animate={{ opacity: 1, x: -140, y: -100 }}
                transition={{ delay: 0.3, duration: 0.8 }}
                className="absolute flex items-center gap-2 px-3 py-2 rounded-xl border border-emerald-500/20 bg-[#0d0d12]/90 backdrop-blur-md shadow-[0_8px_30px_rgba(0,0,0,0.6)] animate-float-slow"
              >
                <div className="flex h-5 w-5 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-400">
                  <Check className="w-3 h-3" />
                </div>
                <span className="text-xs font-semibold text-zinc-200">Email Sent</span>
              </motion.div>

              {/* Card 2: Flight Booked */}
              <motion.div 
                initial={{ opacity: 0, x: 30, y: -40 }}
                animate={{ opacity: 1, x: 120, y: -70 }}
                transition={{ delay: 0.4, duration: 0.8 }}
                className="absolute flex items-center gap-2 px-3 py-2 rounded-xl border border-blue-500/20 bg-[#0d0d12]/90 backdrop-blur-md shadow-[0_8px_30px_rgba(0,0,0,0.6)]"
                style={{ animation: "float 5s ease-in-out infinite" }}
              >
                <Compass className="w-4 h-4 text-blue-400" />
                <span className="text-xs font-semibold text-zinc-200">Flight Booked</span>
              </motion.div>

              {/* Card 3: Code Generated */}
              <motion.div 
                initial={{ opacity: 0, x: -30, y: 40 }}
                animate={{ opacity: 1, x: -150, y: 40 }}
                transition={{ delay: 0.5, duration: 0.8 }}
                className="absolute flex items-center gap-2 px-3 py-2 rounded-xl border border-[#e056fd]/20 bg-[#0d0d12]/90 backdrop-blur-md shadow-[0_8px_30px_rgba(0,0,0,0.6)]"
                style={{ animation: "float-slow 6s ease-in-out infinite" }}
              >
                <Code className="w-4 h-4 text-[#e056fd]" />
                <span className="text-xs font-semibold text-zinc-200">Code Generated</span>
              </motion.div>

              {/* Card 4: Calendar Updated */}
              <motion.div 
                initial={{ opacity: 0, x: 30, y: 40 }}
                animate={{ opacity: 1, x: 130, y: 70 }}
                transition={{ delay: 0.6, duration: 0.8 }}
                className="absolute flex items-center gap-2 px-3 py-2 rounded-xl border border-amber-500/20 bg-[#0d0d12]/90 backdrop-blur-md shadow-[0_8px_30px_rgba(0,0,0,0.6)] animate-float"
              >
                <Calendar className="w-4 h-4 text-amber-400" />
                <span className="text-xs font-semibold text-zinc-200">Calendar Updated</span>
              </motion.div>

              {/* Card 5: Research Complete */}
              <motion.div 
                initial={{ opacity: 0, y: 80 }}
                animate={{ opacity: 1, y: 150 }}
                transition={{ delay: 0.7, duration: 0.8 }}
                className="absolute flex items-center gap-2 px-3.5 py-2 rounded-xl border border-indigo-500/20 bg-[#0d0d12]/90 backdrop-blur-md shadow-[0_8px_30px_rgba(0,0,0,0.6)]"
                style={{ animation: "float 4.5s ease-in-out infinite" }}
              >
                <Search className="w-4 h-4 text-indigo-400" />
                <span className="text-xs font-semibold text-zinc-200">Research Complete</span>
              </motion.div>
            </motion.div>
          </div>
        </div>

        {/* Scroll Indicator */}
        <motion.div 
          animate={{ y: [0, 8, 0] }}
          transition={{ repeat: Infinity, duration: 2 }}
          className="absolute bottom-6 flex flex-col items-center gap-1.5 cursor-pointer opacity-40 hover:opacity-80 transition-opacity"
        >
          <span className="text-[10px] uppercase font-bold tracking-widest text-zinc-500">Discover Features</span>
          <ArrowDown className="w-4 h-4 text-[#e056fd]" />
        </motion.div>
      </section>

      {/* -------------------------------------------------------------
          2. CORE FEATURES SECTION (Glassmorphism Cards Grid)
          ------------------------------------------------------------- */}
      <section id="features" className="relative py-28 px-6 z-10 border-t border-zinc-900 bg-[#07070a]/20">
        <div className="max-w-7xl mx-auto">
          <SectionHeader
            tag="System Capabilities"
            title="Engineered for Universal Automation"
            subtitle="Explore the modular components that make UPSS the most versatile personal operating agent system."
          />

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: Cpu, label: "Multi-Agent Intelligence", desc: "Coordinated orchestration across specialized LLM agents cooperating to solve nested workflows." },
              { icon: Terminal, label: "Autonomous Planning", desc: "Dynamic execution graph generation which automatically adapts if execution failures occur." },
              { icon: History, label: "Long-Term Memory", desc: "Relational context engines that maintain state, parameters, user facts, and history persistent loops." },
              { icon: Database, label: "RAG + Knowledge Graph", desc: "Combines semantic vector databases with relational SQL graphs for hyper-accurate document lookups." },
              { icon: Globe, label: "Browser Automation", desc: "Full E2E web browsing sandbox capable of searching, reading tables, and downloading files dynamically." },
              { icon: Code, label: "Code Execution", desc: "Local sandboxed execution environments for running Python scripts, debugging, and data science workflows." },
              { icon: Search, label: "Research Assistant", desc: "Synthesizes web searches and local documentation databases to draft research analysis reports." },
              { icon: Mail, label: "Email Automation", desc: "Customized SMTP workflows to send, draft, read and dynamically attach workspace files recursively." },
              { icon: Compass, label: "Android App Integration (APK)", desc: "Download the standalone APK to sync notification channels, run voice commands, and control Nexus-AI on the go." },
              { icon: Server, label: "VS Code Extension Sync", desc: "Connect your local IDE to execute code blocks, run terminal commands, and cooperate with coding agents directly from the editor." }
            ].map((feat, idx) => (
              <motion.div
                key={feat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.05 }}
                whileHover={{ y: -6, scale: 1.01 }}
                className="relative group p-6 rounded-2xl border border-zinc-800/80 bg-[#0d0d12]/40 backdrop-blur-md shadow-[0_8px_30px_rgba(0,0,0,0.5)] hover:border-[#e056fd]/40 transition-all duration-300 overflow-hidden"
              >
                {/* Glow Background Hover effect */}
                <div className="absolute inset-0 bg-gradient-to-br from-[#e056fd]/5 to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                
                {/* Card Icon Header */}
                <div className="relative mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-tr from-zinc-800 to-zinc-900 border border-zinc-700/50 text-white group-hover:text-[#e056fd] group-hover:border-[#e056fd]/30 transition-colors">
                  <feat.icon className="w-6 h-6 transition-transform group-hover:scale-110" />
                </div>
                
                {/* Text Content */}
                <h3 className="text-xl font-bold text-white mb-2 relative z-10 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-zinc-300 transition-all">{feat.label}</h3>
                <p className="text-zinc-400 text-sm leading-relaxed relative z-10">{feat.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* -------------------------------------------------------------
          3. HOW IT WORKS (Animated Pipeline Diagram)
          ------------------------------------------------------------- */}
      <section className="relative py-28 px-6 z-10 border-t border-zinc-900">
        <div className="max-w-7xl mx-auto">
          <SectionHeader
            tag="Reasoning Architecture"
            title="The Lifecycle of an Execution"
            subtitle="Witness the pipeline process that converts simple natural language inputs into autonomous operations."
          />

          {/* Pipeline Flex Box */}
          <div className="relative flex flex-col lg:flex-row justify-between items-center gap-8 lg:gap-4 z-10">
            {/* SVG Connector Lines */}
            <div className="absolute top-1/2 left-0 w-full h-1 bg-zinc-900/60 hidden lg:block -translate-y-1/2 z-0" />

            {[
              { step: "01", name: "User Input", desc: "Task query received" },
              { step: "02", name: "Planner", desc: "Builds execution graph" },
              { step: "03", name: "Reasoning", desc: "Decomposes requirements" },
              { step: "04", name: "Tool Selection", desc: "Finds best integration" },
              { step: "05", name: "Execution", desc: "Runs sandboxed scripts" },
              { step: "06", name: "Memory Sync", desc: "Updates semantic database" },
              { step: "07", name: "Response", desc: "Delivers complete output" }
            ].map((pipe, idx) => (
              <motion.div
                key={pipe.name}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.08 }}
                className="relative z-10 flex flex-col items-center p-5 w-44 rounded-2xl border border-zinc-800 bg-[#0d0d12] text-center shadow-[0_10px_25px_rgba(0,0,0,0.6)] hover:border-[#e056fd]/40 transition-colors group"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-r from-[#e056fd] to-indigo-600 text-xs font-bold text-white mb-4 shadow-[0_0_15px_rgba(224,86,253,0.3)]">
                  {pipe.step}
                </div>
                <h4 className="text-sm font-bold text-white mb-1 group-hover:text-[#e056fd] transition-colors">{pipe.name}</h4>
                <p className="text-zinc-500 text-[11px] leading-tight">{pipe.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* -------------------------------------------------------------
          4. AGENT SHOWCASE (Gradient Border Glow Showcase)
          ------------------------------------------------------------- */}
      <section className="relative py-28 px-6 z-10 border-t border-zinc-900 bg-[#07070a]/20">
        <div className="max-w-7xl mx-auto">
          <SectionHeader
            tag="Universal Agents"
            title="Meet the Intelligent Agent Team"
            subtitle="Six specialized system models that collaborate dynamically to process complex multi-domain operations."
          />

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { icon: Brain, title: "General Agent", desc: "Handles casual interactions, prompts, user facts memorization, and overall conversation orchestrations." },
              { icon: Search, title: "Research Agent", desc: "Gathers web documentation, extracts reports, reads tables, and synthesizes semantic indexes." },
              { icon: Code, title: "Coding Agent", desc: "Generates complex scripts, conducts automated code reviews, handles git commands, and resolves debugging." },
              { icon: Mail, title: "Communication Agent", desc: "Sends custom SMTP emails, configures safe display headers, auto-heals attachment folder paths, and parses incoming emails." },
              { icon: Compass, title: "Travel Agent", desc: "Searches public transit schedules, flight bookings, hotel fares, and curates optimized packages." },
              { icon: Database, title: "Data Science Agent", desc: "Loads structured CSV files, generates analytics summaries, plots datasets, and executes regression algorithms." }
            ].map((agent, idx) => (
              <motion.div
                key={agent.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.08 }}
                className="relative group p-8 rounded-2xl bg-gradient-to-b from-[#0d0d12] to-[#08080b] border border-zinc-800 hover:border-[#e056fd]/35 shadow-[0_15px_35px_rgba(0,0,0,0.5)] transition-all overflow-hidden"
              >
                {/* Orbit Glow Ring effect */}
                <div className="absolute top-0 right-0 w-32 h-32 rounded-full bg-gradient-to-br from-[#e056fd]/10 to-transparent blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

                {/* Agent Icon */}
                <div className="relative mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-[#14141d] border border-zinc-800 text-[#e056fd] shadow-[0_4px_15px_rgba(0,0,0,0.4)] group-hover:scale-105 transition-transform">
                  <agent.icon className="w-7 h-7 drop-shadow-[0_0_8px_rgba(224,86,253,0.4)]" />
                </div>

                {/* Texts */}
                <h3 className="text-2xl font-bold text-white mb-3">{agent.title}</h3>
                <p className="text-zinc-400 text-sm leading-relaxed mb-4">{agent.desc}</p>

                {/* Badge link */}
                <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#e056fd] opacity-0 group-hover:opacity-100 transition-opacity">
                  Active in Planner <Check className="w-3.5 h-3.5" />
                </span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* -------------------------------------------------------------
          5. WORKFLOW VISUALIZATION (Animated Flow Diagram)
          ------------------------------------------------------------- */}
      <section className="relative py-28 px-6 z-10 border-t border-zinc-900">
        <div className="max-w-7xl mx-auto">
          <SectionHeader
            tag="Operational Flow"
            title="Unified Agent Workflow Lifecycle"
            subtitle="An animated blueprint representing how the executor compiles and learns from tasks."
          />

          {/* SVG Connector Flow Diagram */}
          <div className="relative p-8 md:p-12 rounded-3xl border border-zinc-800/80 bg-[#0d0d12]/30 backdrop-blur-md overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-[#e056fd]/3 to-blue-500/3 pointer-events-none" />
            
            {/* Flow grid */}
            <div className="relative grid grid-cols-2 md:grid-cols-4 gap-6 z-10">
              {[
                { name: "1. PLAN", desc: "Execution plan compilation" },
                { name: "2. THINK", desc: "Logical reasoning cycle" },
                { name: "3. SELECT TOOLS", desc: "Dynamic dependency binding" },
                { name: "4. EXECUTE", desc: "Sandboxed tool execution" },
                { name: "5. VERIFY", desc: "Checks output validations" },
                { name: "6. LEARN", desc: "Memory fact update" },
                { name: "7. MEMORY", desc: "Vector DB persistent write" },
                { name: "8. RESPOND", desc: "Dynamic report output" }
              ].map((flow, idx) => (
                <motion.div
                  key={flow.name}
                  initial={{ opacity: 0, y: 15 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.05 }}
                  className="p-5 rounded-2xl border border-zinc-800 bg-[#07070b]/90 hover:border-zinc-700 transition-colors"
                >
                  <h4 className="text-sm font-bold text-[#e056fd] mb-1.5">{flow.name}</h4>
                  <p className="text-zinc-400 text-xs leading-relaxed">{flow.desc}</p>
                </motion.div>
              ))}
            </div>
            
            {/* Animated Connector Path in background */}
            <div className="absolute top-1/2 left-0 w-full h-[2px] bg-zinc-800/20 pointer-events-none hidden md:block -translate-y-1/2">
              <svg className="w-full h-2 overflow-visible">
                <line x1="0" y1="1" x2="100%" y2="1" stroke="url(#flow-gradient)" strokeWidth="2" className="animate-flow" />
                <defs>
                  <linearGradient id="flow-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#e056fd" />
                    <stop offset="50%" stopColor="#00d2ff" />
                    <stop offset="100%" stopColor="#e056fd" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </div>
        </div>
      </section>

      {/* -------------------------------------------------------------
          6. MEMORY SYSTEMS SECTION (Timeline Nodes)
          ------------------------------------------------------------- */}
      <section className="relative py-28 px-6 z-10 border-t border-zinc-900 bg-[#07070a]/20">
        <div className="max-w-7xl mx-auto">
          <SectionHeader
            tag="Cognitive Layer"
            title="The Memory Matrix Engine"
            subtitle="Five layers of relational and semantic cache memory that keep local agents context-aware."
          />

          <div className="relative border-l border-zinc-800 ml-6 pl-8 md:pl-12 py-4 space-y-12">
            {[
              { type: "Semantic Memory", desc: "Stores long-term vector embeddings of documents and projects using sentence embeddings.", icon: Database },
              { type: "Episodic Memory", desc: "Retains temporal event sequences, milestone checkpoints, and technical decisions made in previous runs.", icon: History },
              { type: "Conversation Memory", desc: "Full text chat history database containing user queries and assistant markdown response logs.", icon: Mail },
              { type: "Knowledge Memory", desc: "Structures persistent system declarations, domain facts, and business rules logic.", icon: BookOpen },
              { type: "RAG Memory", desc: "Checks context indexes dynamically and maps source references with direct line-range anchors.", icon: Layers }
            ].map((mem, idx) => (
              <motion.div
                key={mem.type}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.08 }}
                className="relative flex flex-col md:flex-row md:items-center gap-4 bg-[#0d0d12]/40 border border-zinc-800/80 p-6 rounded-2xl hover:border-[#e056fd]/30 transition-all group"
              >
                {/* Circle Timeline Bullet */}
                <div className="absolute left-[-41px] md:left-[-49px] flex h-8 w-8 items-center justify-center rounded-full bg-[#050505] border border-zinc-800 text-zinc-500 group-hover:text-[#e056fd] group-hover:border-[#e056fd] transition-all">
                  <mem.icon className="w-4 h-4" />
                </div>

                <div className="flex-1">
                  <h3 className="text-xl font-bold text-white mb-1 group-hover:text-[#e056fd] transition-colors">{mem.type}</h3>
                  <p className="text-zinc-400 text-sm leading-relaxed">{mem.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* -------------------------------------------------------------
          7. INTEGRATED TOOLS (Icons Grid Showcase)
          ------------------------------------------------------------- */}
      <section className="relative py-28 px-6 z-10 border-t border-zinc-900">
        <div className="max-w-7xl mx-auto">
          <SectionHeader
            tag="Tool Integrations"
            title="Fully Connected Ecosystem"
            subtitle="Twelve custom pre-installed tools that allow agents to interface directly with external environments."
          />

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-6">
            {[
              { name: "Browser", icon: Globe, color: "hover:text-[#00d2ff]" },
              { name: "Email", icon: Mail, color: "hover:text-[#e056fd]" },
              { name: "GitHub", icon: GithubIcon, color: "hover:text-zinc-200" },
              { name: "Python", icon: Code, color: "hover:text-yellow-400" },
              { name: "Weather", icon: CloudSun, color: "hover:text-amber-400" },
              { name: "Maps", icon: MapPin, color: "hover:text-rose-400" },
              { name: "Search", icon: Search, color: "hover:text-indigo-400" },
              { name: "Calendar", icon: Calendar, color: "hover:text-orange-400" },
              { name: "Files", icon: FileText, color: "hover:text-sky-400" },
              { name: "Database", icon: Database, color: "hover:text-emerald-400" },
              { name: "Terminal", icon: Terminal, color: "hover:text-[#be2edd]" },
              { name: "Infrastructure", icon: Server, color: "hover:text-violet-400" }
            ].map((tool, idx) => (
              <motion.div
                key={tool.name}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.04 }}
                whileHover={{ y: -4 }}
                className="flex flex-col items-center justify-center p-6 rounded-2xl border border-zinc-800/80 bg-[#0d0d12]/60 hover:border-zinc-700 transition-all cursor-pointer group"
              >
                <tool.icon className={`w-8 h-8 text-zinc-500 transition-colors duration-300 ${tool.color} group-hover:scale-110`} />
                <span className="text-zinc-400 text-xs font-semibold mt-3 group-hover:text-white transition-colors">{tool.name}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* -------------------------------------------------------------
          8. CTA / GET STARTED SECTION
          ------------------------------------------------------------- */}
      <section className="relative py-32 px-6 z-10 border-t border-zinc-900 bg-gradient-to-b from-transparent to-[#07070a]">
        <div className="max-w-4xl mx-auto text-center relative">
          {/* Centered glow behind CTA */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 rounded-full bg-gradient-to-r from-[#e056fd]/10 to-blue-500/10 blur-[80px]" />
          
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl md:text-6xl font-bold tracking-tight text-white mb-6"
          >
            Build the Future with <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#e056fd] to-blue-400">
              Autonomous AI Multi-Collaborative Agent Systems
            </span>
          </motion.h2>

          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="max-w-lg mx-auto text-zinc-400 text-lg mb-10 leading-relaxed"
          >
            Deploy local, persistent memory architectures and connect multi-agent tools to completely automate your workspace today.
          </motion.p>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <Link href="/login">
              <button className="px-8 py-4 rounded-full font-bold text-white bg-gradient-to-r from-[#e056fd] to-[#be2edd] transition-transform hover:scale-105 active:scale-95 shadow-[0_0_30px_rgba(224,86,253,0.3)]">
                Get Started Free
              </button>
            </Link>
            
            <Link href="/docs">
              <button className="px-8 py-4 rounded-full font-bold border border-zinc-800 bg-[#0d0d12]/50 hover:bg-[#121217] backdrop-blur-md transition-transform hover:scale-105 active:scale-95">
                Read Documentation
              </button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* -------------------------------------------------------------
          9. FOOTER SECTION
          ------------------------------------------------------------- */}
      <footer className="relative py-16 px-6 z-10 border-t border-zinc-900 bg-[#030305]">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8 text-zinc-500 text-sm">
          <div className="flex flex-col items-center md:items-start gap-2">
            <div className="flex items-center gap-2">
              <Brain className="w-6 h-6 text-[#e056fd]" />
              <span className="font-extrabold text-white tracking-widest">UPSS</span>
            </div>
            <p className="text-zinc-600 text-xs">© 2026 UPSS Universal Systems. All rights reserved.</p>
          </div>

          <div className="flex flex-wrap justify-center gap-x-8 gap-y-2 font-medium">
            <a href="#" className="hover:text-white transition-colors">Features</a>
            <a href="#" className="hover:text-white transition-colors">Documentation</a>
            <a href="#" className="hover:text-white transition-colors">Security Policy</a>
            <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
          </div>

          <div className="flex gap-4">
            <a href="https://github.com/jadonvansh2005" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
              <GithubIcon className="w-5 h-5" />
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
