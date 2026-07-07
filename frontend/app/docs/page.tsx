"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { 
  ArrowLeft, Terminal, Cpu, Database, Brain, Globe, Mail, 
  Code, Shield, Check, Layers, User, Sparkles, Server, Info, BookOpen
} from "lucide-react";
import Link from "next/link";

interface DocSection {
  id: string;
  title: string;
}

export default function DocsPage() {
  const [activeTab, setActiveTab] = useState("overview");

  // Force dark theme by default on mount
  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);

  const sections: DocSection[] = [
    { id: "overview", title: "System Overview" },
    { id: "architecture", title: "System Architecture" },
    { id: "workflow", title: "E2E Workflow" },
    { id: "commands", title: "Setup & Roadmap" },
    { id: "team", title: "The Team" }
  ];

  return (
    <div className="min-h-screen bg-zinc-50 text-zinc-800 dark:bg-[#050508] dark:text-white transition-colors duration-300 font-sans px-6 py-12 relative overflow-hidden noise-bg">
      {/* Background gradients */}
      <div className="absolute inset-0 z-0 pointer-events-none opacity-40 dark:opacity-40 opacity-10">
        <div className="absolute top-[-10%] right-[-10%] w-[50%] h-[50%] rounded-full bg-gradient-to-br from-[#e056fd]/15 to-transparent blur-[120px]" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[45%] h-[45%] rounded-full bg-gradient-to-tr from-indigo-500/10 to-transparent blur-[120px]" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff02_1px,transparent_1px),linear-gradient(to_bottom,#ffffff02_1px,transparent_1px)] bg-[size:32px_32px] dark:block hidden" />
      </div>

      <div className="max-w-6xl mx-auto relative z-10">
        {/* Navigation header */}
        <div className="mb-10 flex justify-between items-center">
          <Link href="/">
            <button className="group flex items-center gap-2 px-4 py-2.5 text-xs font-bold rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/80 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-all hover:scale-105 shadow-sm dark:shadow-none">
              <ArrowLeft className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform" />
              Back to Home
            </button>
          </Link>
          
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-[#e056fd]" />
            <span className="text-sm font-extrabold tracking-widest text-[#e056fd] uppercase">Technical Docs</span>
          </div>
        </div>

        {/* Page Title */}
        <div className="mb-12 text-center lg:text-left">
          <h1 className="text-4xl lg:text-5xl font-black tracking-tight mb-3">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#e056fd] via-indigo-400 to-[#00d2ff]">
              Universal Problem Solving System
            </span>
          </h1>
          <p className="text-zinc-500 dark:text-zinc-400 text-sm font-semibold max-w-2xl leading-relaxed">
            Complete technical system architecture, multi-agent workflow specifications, development setups, database models, and author profiles for UPSS (Nexus-AI).
          </p>
        </div>

        {/* Tab Selection */}
        <div className="flex flex-wrap gap-2 mb-8 border-b border-zinc-200 dark:border-zinc-850 pb-4">
          {sections.map((sec) => (
            <button
              key={sec.id}
              onClick={() => setActiveTab(sec.id)}
              className={`px-5 py-2.5 rounded-xl text-xs font-extrabold tracking-wide transition-all ${
                activeTab === sec.id
                  ? "bg-gradient-to-r from-[#e056fd] to-[#be2edd] text-white shadow-[0_0_15px_rgba(224,86,253,0.25)]"
                  : "bg-white dark:bg-[#0d0d12]/80 text-zinc-500 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700"
              }`}
            >
              {sec.title}
            </button>
          ))}
        </div>

        {/* Content Container */}
        <div className="min-h-[500px]">
          
          {/* TAB 1: SYSTEM OVERVIEW */}
          {activeTab === "overview" && (
            <motion.div 
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-8 shadow-lg dark:shadow-none">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
                  
                  {/* Left Column: Problem Statement */}
                  <div>
                    <h2 className="text-xl font-extrabold mb-4 text-[#e056fd] flex items-center gap-2">
                      <span className="h-2 w-2 rounded-full bg-[#e056fd]" />
                      The Problem Statement
                    </h2>
                    <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed mb-4 font-semibold">
                      Modern Large Language Models (LLMs) are remarkably capable of generating responses, yet they operate primarily as isolated assistants rather than autonomous problem solvers. They lack persistent memory, stateful context management, secure runtime execution, dynamic planning, and coordinated multi-agent collaboration. As a result, they struggle to execute complex, multi-step workflows that require reasoning, tool usage, validation, and real-world actions.
                    </p>
                    <p className="text-sm text-zinc-650 dark:text-zinc-400 leading-relaxed font-semibold">
                      In practice, users rely on multiple disconnected AI platforms for different tasks, while existing AI assistants often provide answers instead of completing end-to-end objectives. Their limited cross-domain intelligence, minimal personalization, unreliable execution, and inability to adapt dynamically to changing user requirements make them unsuitable for solving real-world problems that span multiple domains.
                    </p>
                  </div>

                  {/* Right Column: Solution */}
                  <div>
                    <h2 className="text-xl font-extrabold mb-4 text-[#00d2ff] flex items-center gap-2">
                      <span className="h-2 w-2 rounded-full bg-[#00d2ff]" />
                      Our Solution: UPSS (Nexus-AI)
                    </h2>
                    <p className="text-sm text-zinc-650 dark:text-zinc-400 leading-relaxed mb-4 font-semibold">
                      UPSS (Universal Problem Solving System) is an intelligent multi-agent execution framework that transforms AI from a conversational assistant into an autonomous problem-solving platform. By combining a scalable Next.js frontend with a FastAPI-powered backend, LangGraph-based agent orchestration, Retrieval-Augmented Generation (RAG), persistent memory, secure runtime execution, and tool-augmented intelligence, UPSS autonomously understands user goals, decomposes complex tasks, coordinates specialized agents, and executes real-world actions across multiple domains.
                    </p>
                    <p className="text-sm text-zinc-650 dark:text-zinc-400 leading-relaxed font-semibold">
                      The platform integrates dynamic agent generation, autonomous planning, cross-domain reasoning, API and tool execution, human-in-the-loop validation for critical operations, and continuous learning through personalized memory. Rather than simply generating responses, UPSS delivers reliable, transparent, context-aware, and end-to-end intelligent solutions.
                    </p>
                  </div>
                </div>

                {/* Visual Architecture Flow Diagram */}
                <div className="mt-8 pt-8 border-t border-zinc-150 dark:border-zinc-800/80">
                  <h4 className="text-[10px] font-black text-zinc-450 dark:text-zinc-550 uppercase tracking-widest text-center mb-6">Autonomous Orchestration Paradigm Shift</h4>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center text-center">
                    
                    {/* Problem Node */}
                    <div className="p-5 rounded-2xl border border-rose-500/10 bg-rose-500/5 backdrop-blur-md relative overflow-hidden group">
                      <div className="absolute inset-0 bg-gradient-to-br from-rose-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                      <h5 className="text-[10px] font-black text-rose-500 uppercase tracking-wider mb-2">Isolated LLM Assistants (Before)</h5>
                      <p className="text-[10px] text-zinc-500 dark:text-zinc-400 leading-relaxed font-semibold">
                        Fragmented workflows • Answers only • No state/memory • Disconnected platforms • Zero validation checks
                      </p>
                    </div>

                    {/* Transition Connector */}
                    <div className="flex flex-col items-center justify-center py-2">
                      <div className="h-0.5 w-16 bg-gradient-to-r from-rose-500 via-indigo-500 to-emerald-500 animate-pulse hidden md:block" />
                      <span className="text-[8px] font-black text-indigo-400 uppercase tracking-widest mt-2 animate-pulse">UPSS Agentic Engine</span>
                      <div className="h-8 w-0.5 bg-gradient-to-b from-rose-500 via-indigo-500 to-emerald-500 animate-pulse md:hidden my-2" />
                    </div>

                    {/* Solution Node */}
                    <div className="p-5 rounded-2xl border border-emerald-500/10 bg-emerald-500/5 backdrop-blur-md relative overflow-hidden group">
                      <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                      <h5 className="text-[10px] font-black text-emerald-500 uppercase tracking-wider mb-2">UPSS Autonomous Teams (After)</h5>
                      <p className="text-[10px] text-zinc-500 dark:text-zinc-400 leading-relaxed font-semibold">
                        LangGraph state • Vector memory RAG • End-to-end planning • Sandboxed tool execution • Safe HITL gates
                      </p>
                    </div>

                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="p-6 rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90">
                  <div className="h-10 w-10 rounded-xl bg-purple-500/10 flex items-center justify-center text-[#e056fd] mb-4 border border-[#e056fd]/20">
                    <Brain className="w-5 h-5" />
                  </div>
                  <h3 className="text-sm font-bold mb-2">Autonomous Teams</h3>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                    Dynamically spawns specialized agent teams (Data Agent, Planning Agent, Reporting Agent) based on query context.
                  </p>
                </div>

                <div className="p-6 rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90">
                  <div className="h-10 w-10 rounded-xl bg-blue-500/10 flex items-center justify-center text-[#00d2ff] mb-4 border border-blue-500/20">
                    <Shield className="w-5 h-5" />
                  </div>
                  <h3 className="text-sm font-bold mb-2">Human-in-the-Loop</h3>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                    Ensures strict safety gates with user approval prompts before executing high-risk file writes or SMTP actions.
                  </p>
                </div>

                <div className="p-6 rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90">
                  <div className="h-10 w-10 rounded-xl bg-emerald-500/10 flex items-center justify-center text-emerald-500 mb-4 border border-emerald-500/20">
                    <Database className="w-5 h-5" />
                  </div>
                  <h3 className="text-sm font-bold mb-2">Relational Vector RAG</h3>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                    Combines SQL conversation histories with Qdrant vector databases to deliver contextually rich and accurate prompts.
                  </p>
                </div>
              </div>
            </motion.div>
          )}

          {/* TAB 2: SYSTEM ARCHITECTURE */}
          {activeTab === "architecture" && (
            <motion.div 
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className="grid grid-cols-1 lg:grid-cols-3 gap-6"
            >
              {/* Architecture Columns */}
              <div className="lg:col-span-2 space-y-6">
                
                {/* Core Architecture Matrix */}
                <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-6 shadow-md">
                  <div className="flex items-center gap-2 mb-4">
                    <Layers className="w-5 h-5 text-[#e056fd]" />
                    <h3 className="text-base font-extrabold">Technical Layers Breakdown</h3>
                  </div>

                  <div className="space-y-4">
                    {[
                      { 
                        title: "1. Frontend Layer (Next.js + Tailwind)", 
                        details: "Implements the maximalism workspace UI, conversation lists sidebar, active model selection configs, and real-time status checking loop."
                      },
                      { 
                        title: "2. Backend services Layer (FastAPI)", 
                        details: "Hosts the main REST API endpoints, security JWT tokens generation, and the auto-copy dynamic file parser engine."
                      },
                      { 
                        title: "3. Agent Orchestration Layer (LangGraph)", 
                        details: "Hosts the orchestration flow chart. Executes task plans offline, handles agent communications, and manages state checkpointing."
                      },
                      { 
                        title: "4. Memory & Storage Layer", 
                        details: "SQLite/PostgreSQL database structures conversation records. Redis stores active caching queues, and Qdrant saves semantic embeddings."
                      },
                      { 
                        title: "5. Tool Execution Layer", 
                        details: "Twelve specialized pre-installed system tools (Browser scraping, secure Docker sandbox execution, automated SMTP email dispatchers)."
                      }
                    ].map((layer) => (
                      <div key={layer.title} className="p-3.5 rounded-xl bg-zinc-50 dark:bg-[#111117] border border-zinc-205 dark:border-zinc-850">
                        <h4 className="text-xs font-bold text-zinc-900 dark:text-zinc-200 mb-1">{layer.title}</h4>
                        <p className="text-[11px] text-zinc-500 dark:text-zinc-400 leading-relaxed font-semibold">{layer.details}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Sidebar recommendations */}
              <div className="space-y-6">
                <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-6 shadow-md">
                  <div className="flex items-center gap-2 mb-4">
                    <Cpu className="w-5 h-5 text-[#00d2ff]" />
                    <h3 className="text-base font-extrabold">Multi-Model LLM Strategy</h3>
                  </div>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed mb-4 font-semibold">
                    UPSS uses a dynamic Router Agent that switches LLM engines based on task complexity:
                  </p>
                  <ul className="space-y-2 text-xs font-bold">
                    <li className="flex items-center gap-2 text-zinc-700 dark:text-zinc-300">
                      <Check className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                      GPT-4o: Complex Reasoning & Planning
                    </li>
                    <li className="flex items-center gap-2 text-zinc-700 dark:text-zinc-300">
                      <Check className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                      Gemini 1.5 Pro: Huge context RAG files
                    </li>
                    <li className="flex items-center gap-2 text-zinc-700 dark:text-zinc-300">
                      <Check className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                      Claude 3.5 Sonnet: Code blocks generation
                    </li>
                    <li className="flex items-center gap-2 text-zinc-700 dark:text-zinc-300">
                      <Check className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                      Llama 3 Local: Offline developer syncs
                    </li>
                  </ul>
                </div>

                <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-6 shadow-md border-t-[#e056fd]/30">
                  <div className="flex items-center gap-2 mb-3">
                    <Server className="w-5 h-5 text-[#e056fd]" />
                    <h3 className="text-base font-extrabold">Observability Layer</h3>
                  </div>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed font-semibold">
                    Monitors agent trajectories, system errors, API call latency, and memory indexing rates using **LangSmith**, **ELK Stack**, and **Prometheus dashboards**.
                  </p>
                </div>
              </div>

              {/* System Architecture and Tech Stack Diagrams */}
              <div className="lg:col-span-3 grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                <div className="border border-zinc-200 dark:border-zinc-800 rounded-3xl overflow-hidden bg-white dark:bg-[#0d0d12]/90 p-5 shadow-lg">
                  <h4 className="text-xs font-bold mb-3 text-zinc-855 dark:text-zinc-300 flex items-center gap-2 uppercase tracking-wider">
                    <Layers className="w-4 h-4 text-[#e056fd]" />
                    System Architecture & Internal Connectivity Mapping
                  </h4>
                  <img 
                    src="/images/System Architecture.jpeg" 
                    alt="UPSS System Architecture" 
                    className="w-full rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-xl hover:scale-[1.01] transition-transform duration-500"
                  />
                </div>

                <div className="border border-zinc-200 dark:border-zinc-800 rounded-3xl overflow-hidden bg-white dark:bg-[#0d0d12]/90 p-5 shadow-lg">
                  <h4 className="text-xs font-bold mb-3 text-zinc-855 dark:text-zinc-300 flex items-center gap-2 uppercase tracking-wider">
                    <Cpu className="w-4 h-4 text-[#00d2ff]" />
                    Technical System Architecture & Recommended Tech Stack
                  </h4>
                  <img 
                    src="/images/Techstack.jpeg" 
                    alt="UPSS Technical System Architecture & Recommended Tech Stack" 
                    className="w-full rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-xl hover:scale-[1.01] transition-transform duration-500"
                  />
                </div>
              </div>

            </motion.div>
          )}

          {/* TAB 3: PIPELINE WORKFLOW */}
          {activeTab === "workflow" && (
            <motion.div 
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-8 shadow-lg">
                <div className="flex items-center gap-2.5 mb-6">
                  <Globe className="w-5 h-5 text-[#e056fd]" />
                  <h3 className="text-xl font-extrabold tracking-tight">End-to-End Workflow Pipeline</h3>
                </div>

                {/* Timeline Grid */}
                <div className="relative border-l border-zinc-200 dark:border-zinc-800 pl-6 ml-4 space-y-8">
                  {[
                    { step: "01", title: "User Input Processing", desc: "User submits queries (voice, text, or file attachment). System parses input formats (PDF data extractor, OCR, speech-to-text)." },
                    { step: "02", title: "Intent & Domain Detection", desc: "Detector evaluates the query and classifies it under specific feature domains (Coding, Research, Travel, Data Science)." },
                    { step: "03", title: "Complexity & Task Decomposing", desc: "Planner decomposes the query goal into sequential executable steps and creates a formal task list plan." },
                    { step: "04", title: "Dynamic Agent team allocation", desc: "LangGraph coordinates specialized agents (Research Agent, Data Agent, Validation Agent) needed to execute the plan." },
                    { step: "05", title: "Tool selection & sandbox run", desc: "Agents select the correct tools (scrapers, SQL databases, email, weather API) and run them inside isolated Docker containers." },
                    { step: "06", title: "Human-in-the-Loop approval gate", desc: "If the task plan includes high-risk write/SMTP operations, the process halts until the user approves or rejects the action." },
                    { step: "07", title: "Validation & Output presentation", desc: "Outputs are checked for syntax consistency and errors. The formatted text response streams onto the workspace console." }
                  ].map((item) => (
                    <div key={item.step} className="relative">
                      {/* Timeline dot */}
                      <span className="absolute -left-[35px] top-0.5 h-4.5 w-4.5 rounded-full bg-gradient-to-tr from-[#e056fd] to-blue-500 border border-white dark:border-[#050508]" />
                      <div className="flex items-start gap-4">
                        <span className="text-xs font-black text-[#e056fd] dark:text-[#f2a2ff]">{item.step}</span>
                        <div>
                          <h4 className="text-sm font-extrabold text-zinc-900 dark:text-zinc-200 mb-1">{item.title}</h4>
                          <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed font-semibold">{item.desc}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* End-to-End Workflow Diagram */}
              <div className="border border-zinc-200 dark:border-zinc-800 rounded-3xl overflow-hidden bg-white dark:bg-[#0d0d12]/90 p-5 shadow-lg">
                <h4 className="text-xs font-bold mb-3 text-zinc-855 dark:text-zinc-300 flex items-center gap-2 uppercase tracking-wider">
                  <Globe className="w-4 h-4 text-[#e056fd]" />
                  End-to-End Execution Flow Pipeline Diagram
                </h4>
                <img 
                  src="/images/workflow.jpeg" 
                  alt="UPSS End-to-End Workflow" 
                  className="w-full rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-xl hover:scale-[1.01] transition-transform duration-500"
                />
              </div>

            </motion.div>
          )}

          {/* TAB 4: SETUP COMMANDS, ENV & ROADMAP */}
          {activeTab === "commands" && (
            <motion.div 
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className="grid grid-cols-1 lg:grid-cols-2 gap-8"
            >
              {/* Left Column: Prerequisites & Setup Commands */}
              <div className="space-y-6">
                <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-6 shadow-md">
                  <h3 className="text-base font-extrabold text-[#e056fd] mb-3">1. Prerequisites</h3>
                  <ul className="space-y-2.5 text-xs font-bold text-zinc-600 dark:text-zinc-400">
                    <li className="flex items-center gap-2">
                      <Check className="w-4 h-4 text-emerald-500 shrink-0" />
                      <span>Python 3.10+</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="w-4 h-4 text-emerald-500 shrink-0" />
                      <span>PostgreSQL Database</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="w-4 h-4 text-emerald-500 shrink-0" />
                      <span>Qdrant Vector Database (via Docker or Qdrant Cloud)</span>
                    </li>
                  </ul>
                </div>

                <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-6 shadow-md">
                  <h3 className="text-base font-extrabold text-[#00d2ff] mb-3">2. Backend Installation</h3>
                  <div className="p-4 rounded-2xl bg-zinc-900 text-zinc-200 text-xs font-mono space-y-1 block border border-zinc-800 overflow-x-auto">
                    <p className="text-zinc-500"># Navigate and install dependencies</p>
                    <p className="text-[#00d2ff]">cd backend</p>
                    <p className="text-[#00d2ff]">pip install -r requirements.txt</p>
                    <br />
                    <p className="text-zinc-500"># Run database migrations for OTP</p>
                    <p className="text-[#00d2ff]">python database/add_verification_columns.py</p>
                    <br />
                    <p className="text-zinc-500"># Start local uvicorn host server</p>
                    <p className="text-[#00d2ff]">uvicorn main:app --reload --port 8000</p>
                  </div>
                </div>

                <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-6 shadow-md">
                  <h3 className="text-base font-extrabold text-[#e056fd] mb-3">3. Frontend Client Installation</h3>
                  <div className="p-4 rounded-2xl bg-zinc-900 text-zinc-200 text-xs font-mono space-y-1 block border border-zinc-800 overflow-x-auto">
                    <p className="text-zinc-500"># Navigate and install packages</p>
                    <p className="text-[#e056fd]">cd frontend</p>
                    <p className="text-[#e056fd]">npm install</p>
                    <br />
                    <p className="text-zinc-500"># Start local Next.js client</p>
                    <p className="text-[#e056fd]">npm run dev</p>
                  </div>
                </div>
              </div>

              {/* Right Column: Env variables, DB models & Roadmap */}
              <div className="space-y-6">
                <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-6 shadow-md">
                  <h3 className="text-base font-extrabold text-[#00d2ff] mb-3">Environment Variables (.env)</h3>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-3 font-semibold">
                    Create a `.env` file in the `backend/` directory:
                  </p>
                  <div className="p-4 rounded-2xl bg-zinc-905 text-zinc-300 text-[10px] font-mono space-y-0.5 block border border-zinc-800 bg-zinc-950 overflow-x-auto">
                    <p className="text-zinc-500"># Database Settings</p>
                    <p className="text-emerald-400">DATABASE_URL=postgresql://&lt;username&gt;:&lt;password&gt;@localhost:5432/upss</p>
                    <br />
                    <p className="text-zinc-500"># LLM Providers</p>
                    <p className="text-emerald-400">GEMINI_API_KEY=your_gemini_api_key</p>
                    <p className="text-emerald-400">OPENAI_API_KEY=your_openai_api_key</p>
                    <p className="text-emerald-400">CLAUDE_API_KEY=your_anthropic_api_key</p>
                    <br />
                    <p className="text-zinc-500"># Qdrant Vector Settings</p>
                    <p className="text-emerald-400">QDRANT_HOST=127.0.0.1</p>
                    <p className="text-emerald-400">QDRANT_PORT=6333</p>
                    <br />
                    <p className="text-zinc-500"># JWT Authentication</p>
                    <p className="text-emerald-400">SECRET_KEY=your_jwt_secret_key</p>
                    <p className="text-emerald-400">ACCESS_TOKEN_EXPIRE_MINUTES=60</p>
                  </div>
                </div>

                <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-6 shadow-md border-t-[#e056fd]/30">
                  <h3 className="text-base font-extrabold text-[#e056fd] mb-3">Future Roadmap</h3>
                  <ul className="space-y-3.5 text-xs font-bold text-zinc-600 dark:text-zinc-400">
                    <li className="flex items-start gap-2.5">
                      <Sparkles className="w-4 h-4 text-[#e056fd] shrink-0 mt-0.5" />
                      <span>Real-world API payment gateway integrations.</span>
                    </li>
                    <li className="flex items-start gap-2.5">
                      <Sparkles className="w-4 h-4 text-[#e056fd] shrink-0 mt-0.5" />
                      <span>Distributed agent clusters running on Kubernetes.</span>
                    </li>
                    <li className="flex items-start gap-2.5">
                      <Sparkles className="w-4 h-4 text-[#e056fd] shrink-0 mt-0.5" />
                      <span>Model Context Protocol (MCP) support.</span>
                    </li>
                    <li className="flex items-start gap-2.5">
                      <Sparkles className="w-4 h-4 text-[#e056fd] shrink-0 mt-0.5" />
                      <span>Reinforcement learning feedback loops from validation outputs.</span>
                    </li>
                    <li className="flex items-start gap-2.5">
                      <Sparkles className="w-4 h-4 text-[#e056fd] shrink-0 mt-0.5" />
                      <span>Enterprise-grade OAuth authentication.</span>
                    </li>
                  </ul>
                </div>
              </div>
            </motion.div>
          )}

          {/* TAB 5: THE TEAM */}
          {activeTab === "team" && (
            <motion.div 
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              {/* Author 1: Vansh Pratap Singh Jadon */}
              <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-8 shadow-lg relative overflow-hidden group">
                <div className="absolute top-[-10%] right-[-10%] w-60 h-60 rounded-full bg-gradient-to-br from-[#e056fd]/5 to-transparent blur-3xl pointer-events-none group-hover:scale-110 transition-transform duration-500" />
                
                <div className="flex flex-col md:flex-row gap-6 items-start relative z-10">
                  <div className="h-16 w-16 rounded-2xl bg-gradient-to-tr from-[#e056fd] to-blue-500 flex items-center justify-center font-extrabold text-2xl text-white shadow-xl shrink-0">
                    VP
                  </div>
                  <div>
                    <h3 className="text-xl font-extrabold text-zinc-900 dark:text-zinc-100 mb-1">Vansh Pratap Singh Jadon</h3>
                    <p className="text-xs text-[#e056fd] font-bold tracking-wider uppercase mb-4">Founder, Lead System Architect, AI Developer</p>
                    
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed font-semibold">
                      Vansh Pratap Singh Jadon, a Computer Science Engineering student passionate about Artificial Intelligence, Machine Learning, Agentic AI, Large Language Models (LLMs), System Design, and Full-Stack Development. With a strong curiosity for emerging technologies, he enjoys designing scalable software systems, building intelligent applications, and applying modern engineering practices to solve real-world problems while continuously expanding his expertise across AI and software engineering.
                    </p>
                  </div>
                </div>
              </div>

              {/* Author 2: Kanika Jain */}
              <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12]/90 p-8 shadow-lg relative overflow-hidden group">
                <div className="absolute top-[-10%] right-[-10%] w-60 h-60 rounded-full bg-gradient-to-br from-blue-500/5 to-transparent blur-3xl pointer-events-none group-hover:scale-110 transition-transform duration-500" />
                
                <div className="flex flex-col md:flex-row gap-6 items-start relative z-10">
                  <div className="h-16 w-16 rounded-2xl bg-gradient-to-tr from-blue-500 to-indigo-500 flex items-center justify-center font-extrabold text-2xl text-white shadow-xl shrink-0">
                    KJ
                  </div>
                  <div className="w-full">
                    <h3 className="text-xl font-extrabold text-zinc-900 dark:text-zinc-100 mb-1">Kanika Jain</h3>
                    <p className="text-xs text-blue-400 font-bold tracking-wider uppercase mb-4">Co-Founder, UI/UX Designer, APP Developer</p>
                    
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed font-semibold">
                      Kanika Jain, a Computer Science Engineering student and passionate about an  Application Developer with a strong interest in Flutter, cross-platform mobile development, and modern UI/UX design. Passionate about creating intuitive, visually appealing, and high-performance mobile applications, she enjoys exploring emerging technologies, crafting seamless user experiences, and continuously enhancing her expertise in contemporary app development.
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

        </div>
      </div>
    </div>
  );
}
