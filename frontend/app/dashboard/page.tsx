"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { 
  FaRobot, FaRegCompass, FaRegLightbulb, FaHistory, 
  FaSlidersH, FaPaperPlane, FaSignOutAlt, FaBrain, 
  FaTicketAlt, FaRoute, FaChartBar, FaUserCircle 
} from "react-icons/fa";

import {
  sendChatMessage
} from "@/services/chat/chatService";

interface Message {
  sender: "user" | "sahayak";
  text: string;
  timestamp: string;
}

export default function Dashboard() {
  const router = useRouter();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Runtime UX State variables
  const [profile, setProfile] = useState<any>(null);
  const [input, setInput] = useState("");
  const [chatHistory, setChatHistory] = useState<Message[]>([]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentDomain, setCurrentDomain] = useState("");

  // Load user session profile data out of LocalStorage
  useEffect(() => {
    const cachedProfile = localStorage.getItem("sahayak_profile");
    if (!cachedProfile) {
      // Graceful fallback redirect if accessed unauthenticated
      router.push("/dashboard");
    } else {
      setProfile(JSON.parse(cachedProfile));
    }
  }, [router]);

  // Keep chat container scrolled to latest response stream
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory, isProcessing]);

  // Hardcoded Agent Responses mapping to task actions
  // const executeAgentTask = (promptText: string) => {
  //   if (!promptText.trim()) return;

  //   const userMessage: Message = {
  //     sender: "user",
  //     text: promptText,
  //     timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  //   };

  //   setChatHistory(prev => [...prev, userMessage]);
  //   setInput("");
  //   setIsProcessing(true);

  //   // Simulate Agentic Thought Chain Processing Delay
  //   setTimeout(() => {
  //     let agentReply = "I have received your instruction. Compiling autonomous execution strategy across available node clusters...";
  //     const normalized = promptText.toLowerCase();

  //     if (normalized.includes("ticket") || normalized.includes("book")) {
  //       agentReply = "✈️ [Autonomous Ticket Node Active]: Locating optimal travel parameters. Scraping schedules, validating baseline pricing configurations, and matching your profile parameters. Seat confirmation payload pending operator clearance.";
  //     } else if (normalized.includes("itinerary") || normalized.includes("trip") || normalized.includes("travel")) {
  //       agentReply = "🗺️ [Strategic Planner Engine Active]: Generating a multi-day trip framework down to the hour. Mapping structural geolocation vectors, matching lodging nodes, and calculating route times. Framework ready for review.";
  //     } else if (normalized.includes("analyze") || normalized.includes("data") || normalized.includes("insights")) {
  //       agentReply = "📊 [Cognitive Analytics Kernel Active]: Ingesting file stream arrays. Parsing dataset metrics, running anomaly models, and building variable correlations. Statistical breakthroughs compiled successfully.";
  //     }

  //     const sahayakMessage: Message = {
  //       sender: "sahayak",
  //       text: agentReply,
  //       timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  //     };

  //     setChatHistory(prev => [...prev, sahayakMessage]);
  //     setIsProcessing(false);
  //   }, 1500);
  // };

  const executeAgentTask = async (
    promptText: string
  ) => {

    if (!promptText.trim())
      return;

    const userMessage: Message = {

      sender: "user",

      text: promptText,

      timestamp:
        new Date()
        .toLocaleTimeString(
          [],
          {
            hour: "2-digit",
            minute: "2-digit"
          }
        )

    };

    setChatHistory(
      prev => [
        ...prev,
        userMessage
      ]
    );

    setInput("");

    setIsProcessing(true);

    try {

      const result =
        await sendChatMessage(
          promptText
        );

      console.log(
        result
      );

      if (
        result.domain
      ) {

        setCurrentDomain(
          result.domain
        );

      }

      const sahayakMessage: Message = {

        sender:
          "sahayak",

        text:

          result.response ||

          result.final_response ||

          "No response received",

        timestamp:
          new Date()
          .toLocaleTimeString(
            [],
            {
              hour:
                "2-digit",
              minute:
                "2-digit"
            }
          )

      };

      setChatHistory(
        prev => [
          ...prev,
          sahayakMessage
        ]
      );

    }

    catch (error) {

      console.error(
        error
      );

      setChatHistory(
        prev => [

          ...prev,

          {

            sender:
              "sahayak",

            text:
              "Backend connection failed.",

            timestamp:
              new Date()
              .toLocaleTimeString(
                [],
                {
                  hour:
                    "2-digit",
                  minute:
                    "2-digit"
                }
              )

          }

        ]
      );

    }

    finally {

      setIsProcessing(
        false
      );

    }

  };

  const handleLogout = () => {
    localStorage.clear();
    router.push("/");
  };

  return (
    <div className="min-h-screen bg-[#131314] text-[#e3e3e3] flex overflow-hidden font-sans selection:bg-violet-500/30">
      
      {/* ── SIDEBAR (GEMINI MINIMALIST DRAWER) ── */}
      <aside 
        className={`bg-[#1e1e1f] h-screen transition-all duration-300 flex flex-col justify-between border-r border-[#2d2d2e] z-30 ${
          isSidebarOpen ? "w-68 p-4" : "w-0 p-0 overflow-hidden opacity-0 border-none"
        }`}
      >
        <div className="space-y-6">
          {/* Brand Engine Logo */}
          <div className="flex items-center gap-3 px-2 py-1.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-violet-600 to-fuchsia-500 flex items-center justify-center shadow-md shadow-violet-500/20">
              <FaBrain className="text-white text-sm" />
            </div>
            <span className="font-black text-sm tracking-[0.2em] bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">SAHAYAK AI</span>
          </div>

          {/* New Prompt Button Toggle */}
          <button 
            onClick={() => setChatHistory([])}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-full bg-[#1a1a1a]/40 border border-white/5 hover:bg-[#28292a] text-xs font-semibold tracking-wider transition duration-200"
          >
            <span className="text-sm text-violet-400">+</span> New Session
          </button>

          {/* Dynamic Navigation Node Stack */}
          <nav className="space-y-1 text-xs">
            <div className="text-[10px] uppercase tracking-widest text-white/30 font-mono font-bold px-4 py-2">System Anchors</div>
            <button className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl hover:bg-[#28292a] text-white/70 hover:text-white transition"><FaRegCompass /> Explore Matrix</button>
            <button className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl hover:bg-[#28292a] text-white/70 hover:text-white transition"><FaRegLightbulb /> Core Extensions</button>
            <button className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl hover:bg-[#28292a] text-white/70 hover:text-white transition"><FaHistory /> Session History</button>
            <button className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl hover:bg-[#28292a] text-white/70 hover:text-white transition"><FaSlidersH /> Tuning Settings</button>
          </nav>
        </div>

        {/* User Session Profile Card Matrix */}
        {profile && (
          <div className="p-3 bg-[#181819] rounded-2xl border border-white/5 space-y-3">
            <div className="flex items-center gap-3">
              <FaUserCircle className="text-2xl text-violet-400" />
              <div className="min-w-0 flex-1">
                <p className="text-xs font-bold text-white truncate">{profile.name}</p>
                <p className="text-[10px] font-mono text-white/40 uppercase tracking-wider">{profile.role}</p>
              </div>
            </div>
            <button 
              onClick={handleLogout}
              className="w-full flex items-center justify-center gap-2 py-2 rounded-xl bg-red-500/10 border border-red-500/10 text-red-400 hover:bg-red-500/20 text-[11px] font-bold transition duration-200"
            >
              <FaSignOutAlt /> TERMINATE LINK
            </button>
          </div>
        )}
      </aside>

      {/* ── MAIN WORKSPACE PLATFORM ── */}
      <main className="flex-1 flex flex-col h-screen relative bg-[#131314]">
        
        {/* Header Ribbon Row */}
        <header className="h-14 px-6 flex items-center justify-between border-b border-[#2d2d2e] bg-[#131314]/50 backdrop-blur-md z-20">
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2 rounded-xl hover:bg-[#202124] text-white/60 hover:text-white transition"
            title="Toggle Console Sidebar"
          >
            ☰
          </button>
          <div className="flex items-center gap-4 text-xs font-mono">
            <span className="flex items-center gap-1.5 text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-md border border-emerald-500/10">
              <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" /> NODE STREAM ACTIVE
            </span>
            {profile && (
              <span className="text-white/30 hidden sm:inline">QUOTA: <span className="text-violet-400 font-bold">{profile.computeQuota || "100 TFLOPS"}</span></span>
            )}
          </div>
        </header>

        {/* Dynamic Frame Context Display Panel */}
        <div className="flex-1 overflow-y-auto px-4 md:px-0 py-8 custom-scrollbar">
          <div className="max-w-3xl mx-auto h-full flex flex-col">
            
            {chatHistory.length === 0 ? (
              /* GEMINI EMPTY STATE WELCOME LAYOUT */
              <div className="my-auto space-y-10 animate-fadeIn">
                <div>
                  <h1 className="text-4xl md:text-5xl font-medium tracking-tight bg-gradient-to-r from-[#4285f4] via-[#9b51e0] to-[#ec4899] bg-clip-text text-transparent">
                    Hello, {profile ? profile.name.split(" ")[0] : "Operator"}.
                  </h1>
                  <h2 className="text-4xl md:text-5xl font-medium tracking-tight text-[#444746] mt-2">
                    How can Sahayak assist your workflow today?
                  </h2>
                </div>

                {/* TASK ACTION COMPASS SUITE */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div 
                    onClick={() => executeAgentTask("Book a business class ticket to San Francisco next Tuesday")}
                    className="p-5 rounded-2xl bg-[#1e1e1f] border border-white/5 hover:bg-[#28292a] cursor-pointer transition duration-200 group relative flex flex-col justify-between h-36"
                  >
                    <p className="text-xs text-[#c4c7c5] leading-relaxed group-hover:text-white transition">Book a ticket seamlessly across global transit layers...</p>
                    <div className="p-2.5 self-end rounded-xl bg-black/40 border border-white/5 text-violet-400 group-hover:scale-110 transition"><FaTicketAlt /></div>
                  </div>

                  <div 
                    onClick={() => executeAgentTask("Create a detailed 4-day Tokyo travel itinerary exploring tech and culture hubs")}
                    className="p-5 rounded-2xl bg-[#1e1e1f] border border-white/5 hover:bg-[#28292a] cursor-pointer transition duration-200 group relative flex flex-col justify-between h-36"
                  >
                    <p className="text-xs text-[#c4c7c5] leading-relaxed group-hover:text-white transition">Create a balanced, comprehensive trip itinerary...</p>
                    <div className="p-2.5 self-end rounded-xl bg-black/40 border border-white/5 text-fuchsia-400 group-hover:scale-110 transition"><FaRoute /></div>
                  </div>

                  <div 
                    onClick={() => executeAgentTask("Analyze our Q1 marketing dataset for operational insights and breakthroughs")}
                    className="p-5 rounded-2xl bg-[#1e1e1f] border border-white/5 hover:bg-[#28292a] cursor-pointer transition duration-200 group relative flex flex-col justify-between h-36"
                  >
                    <p className="text-xs text-[#c4c7c5] leading-relaxed group-hover:text-white transition">Analyze enterprise system data matrices for structural insights...</p>
                    <div className="p-2.5 self-end rounded-xl bg-black/40 border border-white/5 text-cyan-400 group-hover:scale-110 transition"><FaChartBar /></div>
                  </div>
                </div>
              </div>
            ) : (
              /* ACTIVE CONVERSATION CONTEXT TIMELINE */
              <div className="space-y-6 flex-1 pb-12 font-sans text-sm md:text-base">
                {chatHistory.map((msg, index) => (
                  <div 
                    key={index} 
                    className={`flex gap-4 p-4 rounded-2xl border ${
                      msg.sender === "user" 
                        ? "bg-[#282a2c]/30 border-white/5 ml-auto max-w-[85%]" 
                        : "bg-transparent border-transparent mr-auto w-full"
                    }`}
                  >
                    {/* Message Node Avatar Element */}
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-xs font-bold border ${
                      msg.sender === "user" 
                        ? "bg-violet-600 border-violet-500 text-white order-2" 
                        : "bg-[#1e1e1f] border-[#2d2d2e] text-fuchsia-400"
                    }`}>
                      {msg.sender === "user" ? <FaUserCircle className="text-lg" /> : <FaRobot />}
                    </div>

                    {/* Chat Text Matrix Body */}
                    <div className={`flex flex-col space-y-1.5 ${msg.sender === "user" ? "order-1 text-right" : "text-left"}`}>
                      <span className="text-[10px] font-mono font-bold tracking-wider text-white/20 uppercase">{msg.sender} • {msg.timestamp}</span>
                      <p className="text-[#e3e3e3] leading-relaxed whitespace-pre-wrap text-sm">{msg.text}</p>
                    </div>
                  </div>
                ))}

                {/* THOUGHT STREAM LIVE LOADING PIN */}
                {isProcessing && (
                  <div className="flex gap-4 p-4 mr-auto w-full animate-pulse">
                    <div className="w-8 h-8 rounded-full bg-[#1e1e1f] border border-[#2d2d2e] text-fuchsia-400 flex items-center justify-center text-xs">
                      <FaRobot className="animate-spin" />
                    </div>
                    <div className="flex flex-col space-y-2 w-full">
                      <span className="text-[10px] font-mono tracking-wider text-white/20">SAHAYAK INTEGRATING WORKFLOW ARRAY...</span>
                      <div className="h-4 bg-white/5 rounded-md w-3/4 animate-pulse" />
                      <div className="h-4 bg-white/5 rounded-md w-1/2 animate-pulse" />
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
        </div>

        {/* ── CONSOLE COMMAND ENTRY PORTAL ── */}
        <footer className="p-4 bg-[#131314] border-t border-white/[0.03]">
          <div className="max-w-3xl mx-auto relative group">
            
            {/* Input Bar Structure Wrapper */}
            <div className="w-full flex items-center bg-[#1e1e1f] border border-transparent focus-within:border-white/10 rounded-full px-6 py-3.5 transition shadow-inner">
              <input 
                type="text" 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && executeAgentTask(input)}
                placeholder="Ask Sahayak to execute workflows..."
                className="flex-1 bg-transparent border-none text-[#e3e3e3] placeholder:text-[#747775] text-sm focus:outline-none focus:ring-0 pr-4"
                disabled={isProcessing}
              />
              <button 
                onClick={() => executeAgentTask(input)}
                disabled={!input.trim() || isProcessing}
                className={`p-2.5 rounded-full transition ${
                  input.trim() && !isProcessing
                    ? "bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white shadow-lg cursor-pointer transform hover:scale-105 active:scale-95" 
                    : "text-white/20 bg-white/5 cursor-not-allowed"
                }`}
                title="Send instruction payload"
              >
                <FaPaperPlane className="text-xs" />
              </button>
            </div>

            {/* Sub-label Legal disclaimer footprint */}
            <p className="text-[10px] text-center text-[#747775] font-mono mt-2 tracking-wide">
              Sahayak Kernel Node OS v2.0.26 • Agent executions require monitoring parameters.
            </p>
          </div>
        </footer>

      </main>
    </div>
  );
}