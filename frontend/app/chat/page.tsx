"use client";

import React, { useState, useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Search, Paperclip, Send, Mic, Settings, Sun, Moon, 
  ChevronDown, Copy, ThumbsUp, ThumbsDown, Plus, 
  PanelLeftClose, User, MessageSquare, Sparkles, Check, X, FileText, Trash2
} from "lucide-react";
import Link from "next/link";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  time: string;
  status?: "read" | "sent";
}

interface ChatThread {
  id: string;
  title: string;
  time: string;
}

interface UserProfile {
  name: string;
  email: string;
  plan: string;
}

function ChatPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [messageInput, setMessageInput] = useState("");
  
  // Dynamic AI Models state
  const [selectedModel, setSelectedModel] = useState("OpenAI (GPT-4o)");
  const [modelDropdownOpen, setModelDropdownOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);

  // Popover menu state matching screenshot
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);

  // User Profile configuration state
  const [profileModalOpen, setProfileModalOpen] = useState(false);
  const [profile, setProfile] = useState<UserProfile>({
    name: "User",
    email: "",
    plan: "Nexus Pro"
  });
  // Modal intermediate form inputs
  const [inputName, setInputName] = useState("User");
  const [inputEmail, setInputEmail] = useState("");
  const [inputPlan, setInputPlan] = useState("Nexus Pro");

  // RAG File Upload states
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isFileUploading, setIsFileUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Threads & Conversations state
  const [activeThreadId, setActiveThreadId] = useState<string>("");
  const [threads, setThreads] = useState<ChatThread[]>([]);

  // Dynamic state representation of conversations map - starts empty
  const [conversations, setConversations] = useState<Record<string, Message[]>>({});

  // Initial Theme load verification
  useEffect(() => {
    const html = document.documentElement;
    if (isDarkMode) {
      html.classList.add("dark");
    } else {
      html.classList.remove("dark");
    }
  }, [isDarkMode]);

  // Load User Data & Conversations on Mount
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      // Guard redirect to login if not authenticated
      window.location.href = "/login";
      return;
    }

    // Fetch Profile details
    fetchUserProfile(token);

    // Fetch User Conversations list from DB
    fetchConversations(token);
  }, []);

  // Fetch past messages when active thread changes
  useEffect(() => {
    if (!activeThreadId) return;
    
    // Skip fetching if it is a local unsaved thread
    if (activeThreadId.startsWith("t_")) return;

    const token = localStorage.getItem("access_token");
    if (token) {
      fetchConversationMessages(token, activeThreadId);
    }
  }, [activeThreadId]);

  const toggleTheme = () => {
    setIsDarkMode(prev => !prev);
  };

  const fetchUserProfile = async (token: string) => {
    try {
      const res = await fetch("http://127.0.0.1:8000/me", {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setProfile({
          name: data.name || "Vansh pratap Singh Jadon",
          email: data.email || "vansh@nexusai.com",
          plan: "Nexus Pro"
        });
        setInputName(data.name || "Vansh pratap Singh Jadon");
        setInputEmail(data.email || "vansh@nexusai.com");
      }
    } catch (err) {
      console.error("Error fetching user profile:", err);
    }
  };

  const fetchConversations = async (token: string) => {
    try {
      const res = await fetch("http://127.0.0.1:8000/conversations/", {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        const formattedThreads = data.map((c: any) => ({
          id: String(c.id),
          title: c.title || "Untitled Conversation",
          time: new Date(c.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }));
        setThreads(formattedThreads);

        // Auto select first thread if available
        if (formattedThreads.length > 0) {
          setActiveThreadId(formattedThreads[0].id);
        } else {
          startNewChat();
        }
      }
    } catch (err) {
      console.error("Error fetching user conversations:", err);
    }
  };

  const fetchConversationMessages = async (token: string, convId: string) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/conversations/${convId}`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        const formattedMessages = data.messages.map((m: any, idx: number) => ({
          id: String(idx),
          role: m.role as "user" | "assistant",
          content: m.content,
          time: new Date(m.created_at || Date.now()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          status: "read" as const
        }));
        setConversations(prev => ({
          ...prev,
          [convId]: formattedMessages
        }));
      }
    } catch (err) {
      console.error("Error fetching conversation messages:", err);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setIsFileUploading(true);
      setUploadError(null);

      const token = localStorage.getItem("access_token");
      if (!token) {
        setUploadError("User session not found.");
        setIsFileUploading(false);
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      try {
        console.log(`[RAG Upload] Indexing file '${file.name}' directly via backend...`);
        const res = await fetch("http://127.0.0.1:8000/rag/upload", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`
          },
          body: formData
        });

        if (res.ok) {
          const data = await res.json();
          console.log("[RAG Upload] Indexing successful:", data);
        } else {
          const errData = await res.json();
          setUploadError(errData.detail || "Ingestion failed.");
          console.error("[RAG Upload] Error response:", errData);
        }
      } catch (err: any) {
        setUploadError(err.message || "Connection error.");
        console.error("[RAG Upload] Connection failed:", err);
      } finally {
        setIsFileUploading(false);
      }
    }
  };

  const triggerFileSelect = () => {
    fileInputRef.current?.click();
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // Streaming states
  const [isStreaming, setIsStreaming] = useState(false);
  const [pendingApproval, setPendingApproval] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversations, activeThreadId]);

  const handleApprove = () => {
    if (!pendingApproval) return;
    const origQuery = pendingApproval.parameters.raw_query;
    setPendingApproval(null);
    handleSendMessage(`Approve: ${origQuery}`);
  };

  const handleReject = () => {
    if (!pendingApproval) return;
    const origQuery = pendingApproval.parameters.raw_query;
    setPendingApproval(null);
    handleSendMessage(`Reject: ${origQuery}`);
  };

  const handleSendMessage = async (overridePrompt?: any) => {
    const rawPrompt = typeof overridePrompt === "string" ? overridePrompt.trim() : messageInput.trim();
    if ((!rawPrompt && !selectedFile) || isStreaming || isFileUploading) return;

    const token = localStorage.getItem("access_token");
    if (!token) {
      window.location.href = "/login";
      return;
    }

    const userPrompt = rawPrompt || (selectedFile ? `Analyze attached file: ${selectedFile.name}` : "");
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Show attachment text prefix if a file is uploaded
    const displayMsg = selectedFile 
      ? (rawPrompt ? `[Attachment: ${selectedFile.name}] ${rawPrompt}` : `[Attachment: ${selectedFile.name}]`)
      : userPrompt;

    const newUserMsg: Message = {
      id: Math.random().toString(),
      role: "user",
      content: displayMsg,
      time: timeStr,
      status: "sent"
    };

    // Temporarily add User Message in local UI state
    setConversations(prev => ({
      ...prev,
      [activeThreadId]: [...(prev[activeThreadId] || []), newUserMsg]
    }));
    
    if (overridePrompt === undefined) {
      setMessageInput("");
    }
    setIsStreaming(true);

    // Call actual backend chat endpoint using Form-Data format
    try {
      const formData = new FormData();
      formData.append("message", userPrompt);
      
      // File has already been pre-uploaded to /rag/upload directly.
      // We do not append the file here to prevent duplicate uploads.

      // If active thread is already saved on backend database, pass its id
      if (activeThreadId && !activeThreadId.startsWith("t_")) {
        formData.append("conversation_id", activeThreadId);
      }

       // Log payload parameters to browser console to verify file binary inclusion
       console.log("Selected File =", selectedFile);
      for (const [key, value] of formData.entries()) {
        console.log(`[FormData Payload] ${key}:`, value);
      }

      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`
        },
        body: formData
      });

      // Clear local file selector inputs after triggering the request
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      const data = await res.json();
      if (!res.ok) {
        console.error("[ChatAPI Error Detail]", data.detail);
        const errMsg = typeof data.detail === "object" 
          ? JSON.stringify(data.detail, null, 2) 
          : (data.detail || "Chat endpoint failed.");
        throw new Error(errMsg);
      }

      // Mark user message as read
      setConversations(prev => {
        const list = prev[activeThreadId] || [];
        return {
          ...prev,
          [activeThreadId]: list.map(m => m.id === newUserMsg.id ? { ...m, status: "read" as const } : m)
        };
      });

      const backendConvId = String(data.conversation_id);

      // Prepare empty assistant message for typewriter streaming animation
      const streamId = Math.random().toString();
      const newAssistantMsg: Message = {
        id: streamId,
        role: "assistant",
        content: "",
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      // Set conversation list for the active conversation key
      setConversations(prev => {
        const currentList = prev[activeThreadId] || [];
        return {
          ...prev,
          [backendConvId]: [...currentList, newAssistantMsg]
        };
      });

      // -----------------------------------------------------------------
      // Dynamic Model UI Swapping based on Response Domain returned from backend
      // -----------------------------------------------------------------
      const domain = data.domain ? String(data.domain).toLowerCase() : "general";
      let matchedModel = "OpenAI (GPT-4o)"; // Default fallback

      if (domain.includes("code") || domain.includes("program")) {
        matchedModel = "Claude (Claude 3.5 Sonnet)";
      } else if (domain.includes("data") || domain.includes("file") || domain.includes("rag") || domain.includes("science")) {
        matchedModel = "Gemini (Gemini 1.5 Pro)";
      } else if (domain.includes("local") || domain.includes("terminal") || domain.includes("system")) {
        matchedModel = "Ollama (Llama 3 Local)";
      } else {
        matchedModel = "OpenAI (GPT-4o)";
      }
      setSelectedModel(matchedModel);

      // Update active thread context immediately if it was a new conversation to sync UI view
      if (activeThreadId.startsWith("t_")) {
        setActiveThreadId(backendConvId);
        fetchConversations(token);
      }

      // Stream generation tokens from backend response value
      const fullResponseText = data.response || "No response received.";
      const words = fullResponseText.split(" ");
      let currentWordIndex = 0;
      let currentContent = "";

      const interval = setInterval(() => {
        if (currentWordIndex < words.length) {
          currentContent += (currentWordIndex === 0 ? "" : " ") + words[currentWordIndex];
          setConversations(prev => {
            const list = prev[backendConvId] || [];
            return {
              ...prev,
              [backendConvId]: list.map(m => m.id === streamId ? { ...m, content: currentContent } : m)
            };
          });
          currentWordIndex++;
        } else {
          clearInterval(interval);
          setIsStreaming(false);
          if (data.pending_approval) {
            setPendingApproval(data.pending_approval);
          }
        }
      }, 50);

    } catch (err: any) {
      console.error(err);
      setIsStreaming(false);
      
      // Fallback message insertion if API breaks
      const errorAssistantMsg: Message = {
        id: Math.random().toString(),
        role: "assistant",
        content: `Error connecting to FastAPI host: ${err.message}. Ensure uvicorn server is running on http://127.0.0.1:8000.`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setConversations(prev => ({
        ...prev,
        [activeThreadId]: [...(prev[activeThreadId] || []), errorAssistantMsg]
      }));
    }
  };

  const handleDeleteConversation = async (convId: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Avoid selecting the thread when clicking delete
    
    // If it's a temporary local-only thread
    if (convId.startsWith("t_")) {
      setThreads(prev => prev.filter(t => t.id !== convId));
      if (activeThreadId === convId) {
        startNewChat();
      }
      return;
    }

    const token = localStorage.getItem("access_token");
    if (!token) return;

    // Delete from backend database
    try {
      const res = await fetch(`http://127.0.0.1:8000/conversations/${convId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (res.ok) {
        setThreads(prev => prev.filter(t => t.id !== convId));
        if (activeThreadId === convId) {
          startNewChat();
        }
      } else {
        console.error("Failed to delete conversation");
      }
    } catch (err) {
      console.error("Error deleting conversation:", err);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const startNewChat = () => {
    const newId = `t_${Math.random()}`;
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const newThread: ChatThread = {
      id: newId,
      title: "New Conversation",
      time: now
    };

    setThreads(prev => [newThread, ...prev]);
    setConversations(prev => ({
      ...prev,
      [newId]: [{ id: Math.random().toString(), role: "assistant", content: `Hello! I am ready. How can I help you using ${selectedModel}?`, time: now }]
    }));
    setActiveThreadId(newId);
  };

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfile({
      name: inputName,
      email: inputEmail,
      plan: inputPlan
    });
    setProfileModalOpen(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_email");
    window.location.href = "/login";
  };

  const activeMessages = conversations[activeThreadId] || [];
  const filteredThreads = threads.filter(t => t.title.toLowerCase().includes(searchQuery.toLowerCase()));

  return (
    <div className="flex h-screen bg-zinc-100 text-zinc-800 dark:bg-[#07070d] dark:text-white transition-colors duration-300 font-sans overflow-hidden relative">
      {/* Hidden File Input for RAG uploads */}
      <input 
        type="file" 
        ref={fileInputRef} 
        onChange={handleFileChange} 
        className="hidden" 
        accept=".pdf,.csv,.txt,.json,.xlsx,.doc,.docx"
      />

      {/* Background gradients */}
      <div className="absolute inset-0 z-0 pointer-events-none opacity-40 dark:opacity-40 opacity-10">
        <div className="absolute top-[20%] right-[-10%] w-[40%] h-[40%] rounded-full bg-[#e056fd]/15 blur-[130px] animate-pulse-slow" />
        <div className="absolute bottom-[10%] left-[10%] w-[35%] h-[35%] rounded-full bg-blue-500/10 blur-[120px]" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff02_1px,transparent_1px),linear-gradient(to_bottom,#ffffff02_1px,transparent_1px)] bg-[size:32px_32px] dark:block hidden" />
      </div>

      {/* -------------------------------------------------------------
          LEFT SIDEBAR
          ------------------------------------------------------------- */}
      <AnimatePresence initial={false}>
        {sidebarOpen && (
          <motion.aside
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 285, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="relative h-full bg-white border-r border-zinc-200 dark:bg-[#0a0a10] dark:border-[#1a1a24] flex flex-col z-10 shrink-0 select-none text-zinc-700 dark:text-zinc-300"
          >
            {/* Header branding */}
            <div className="p-4 flex items-center justify-between border-b border-zinc-200 dark:border-[#1a1a24]">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-[#e056fd] to-blue-500 flex items-center justify-center shadow-[0_0_15px_rgba(224,86,253,0.3)]">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h2 className="font-extrabold text-sm tracking-wide text-zinc-900 dark:text-zinc-100">Nexus-AI</h2>
                  <p className="text-[9px] text-zinc-500 font-bold tracking-wider uppercase">Multi-Agent</p>
                </div>
              </div>
              
              <button 
                onClick={() => setSidebarOpen(false)}
                className="p-2 rounded-lg text-zinc-500 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:text-white dark:hover:bg-zinc-800/40 transition-colors"
              >
                <PanelLeftClose className="w-4 h-4" />
              </button>
            </div>

            {/* New Chat Button */}
            <div className="p-4">
              <button 
                onClick={startNewChat}
                className="w-full flex items-center justify-center gap-2 py-3.5 rounded-xl font-bold text-white bg-gradient-to-r from-[#e056fd] to-[#be2edd] transition-transform hover:scale-[1.01] active:scale-[0.99] shadow-[0_0_15px_rgba(224,86,253,0.25)]"
              >
                <Plus className="w-4 h-4" />
                New Chat
              </button>
            </div>

            {/* Search thread list */}
            <div className="px-4 mb-4">
              <div className="relative flex items-center bg-zinc-100 dark:bg-[#11111a] border border-zinc-200 dark:border-[#1a1a24] rounded-xl px-3 py-2 text-zinc-500 dark:text-zinc-400 focus-within:border-[#e056fd]/50 transition-colors">
                <Search className="w-4 h-4 mr-2 text-zinc-400 dark:text-zinc-500" />
                <input 
                  type="text" 
                  placeholder="Search chats" 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="bg-transparent border-none outline-none text-xs w-full text-zinc-900 dark:text-zinc-200 placeholder-zinc-400 dark:placeholder-zinc-500"
                />
              </div>
            </div>

            {/* Scroll Threads */}
            <div className="flex-1 overflow-y-auto px-2 space-y-4">
              {filteredThreads.length > 0 ? (
                <div>
                  <span className="px-3 text-[10px] uppercase font-bold tracking-widest text-zinc-400 dark:text-zinc-500">Conversations</span>
                  <div className="mt-2 space-y-1">
                    {filteredThreads.map(t => (
                      <div 
                        key={t.id}
                        onClick={() => setActiveThreadId(t.id)}
                        className={`flex items-center justify-between p-3.5 rounded-xl cursor-pointer transition-all border group relative ${t.id === activeThreadId ? "bg-[#e056fd]/10 border-[#e056fd]/40 text-[#e056fd] dark:text-white" : "border-transparent hover:bg-zinc-100 dark:hover:bg-zinc-800/20 text-zinc-500 dark:text-zinc-400 hover:text-[#e056fd] dark:hover:text-white"}`}
                      >
                        <div className="flex items-center gap-3 truncate max-w-[75%]">
                          <MessageSquare className="w-4 h-4 shrink-0 text-[#e056fd]" />
                          <span className="text-xs font-semibold truncate">{t.title}</span>
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
                          <span className="text-[9px] font-semibold text-zinc-400 dark:text-zinc-650 group-hover:hidden">{t.time}</span>
                          <button
                            onClick={(e) => handleDeleteConversation(t.id, e)}
                            className="hidden group-hover:flex p-1 rounded-md text-zinc-400 hover:text-red-500 hover:bg-zinc-200 dark:hover:bg-zinc-800/60 transition-colors"
                            title="Delete Conversation"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 text-xs text-zinc-400 dark:text-zinc-600 font-semibold">No active sessions</div>
              )}
            </div>

            {/* Popover Menu matching screenshot */}
            <AnimatePresence>
              {profileMenuOpen && (
                <motion.div 
                  initial={{ opacity: 0, y: 10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 10, scale: 0.95 }}
                  className="absolute bottom-16 left-4 w-64 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#181820] text-zinc-800 dark:text-white shadow-2xl p-2.5 z-30 font-sans"
                >
                  {/* Profile Header */}
                  <Link href="/profile">
                    <div className="flex items-center justify-between p-2 rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800/60 transition-colors cursor-pointer group">
                      <div className="flex items-center gap-3">
                        <div className="h-9 w-9 rounded-full bg-gradient-to-tr from-rose-400 to-[#e056fd] flex items-center justify-center font-bold text-xs text-white">
                          {profile.name.split(" ").map(n => n[0]).join("").substring(0, 2).toUpperCase()}
                        </div>
                        <div className="truncate max-w-[140px]">
                          <h4 className="text-xs font-bold text-zinc-900 dark:text-zinc-100 truncate">{profile.name}</h4>
                          <span className="text-[10px] text-zinc-500 font-semibold group-hover:text-[#e056fd] transition-colors">Go</span>
                        </div>
                      </div>
                      <svg className="w-3.5 h-3.5 text-zinc-500 group-hover:text-zinc-900 dark:group-hover:text-white transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </Link>

                  <div className="h-[1px] bg-zinc-200 dark:bg-zinc-850 my-1.5" />

                  {/* Options */}
                  <div className="space-y-0.5">
                    <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-semibold hover:bg-zinc-100 dark:hover:bg-zinc-800/60 text-zinc-600 dark:text-zinc-300 hover:text-zinc-900 dark:hover:text-white transition-colors">
                      <Sparkles className="w-4 h-4 text-zinc-400" />
                      Upgrade plan
                    </button>
                    
                    <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-semibold hover:bg-zinc-100 dark:hover:bg-zinc-800/60 text-zinc-600 dark:text-zinc-300 hover:text-zinc-900 dark:hover:text-white transition-colors">
                      <svg className="w-4 h-4 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Personalization
                    </button>

                    <Link href="/profile" className="block">
                      <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-semibold hover:bg-zinc-100 dark:hover:bg-zinc-800/60 text-zinc-600 dark:text-zinc-300 hover:text-zinc-900 dark:hover:text-white transition-colors">
                        <User className="w-4 h-4 text-zinc-400" />
                        Profile
                      </button>
                    </Link>

                    <button 
                      onClick={() => {
                        setProfileMenuOpen(false);
                        setProfileModalOpen(true);
                      }}
                      className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-semibold hover:bg-zinc-100 dark:hover:bg-zinc-800/60 text-zinc-600 dark:text-zinc-300 hover:text-zinc-900 dark:hover:text-white transition-colors"
                    >
                      <Settings className="w-4 h-4 text-zinc-400" />
                      Settings
                    </button>
                  </div>

                  <div className="h-[1px] bg-zinc-200 dark:bg-zinc-850 my-1.5" />

                  <div className="space-y-0.5">
                    <button className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold hover:bg-zinc-100 dark:hover:bg-zinc-800/60 text-zinc-600 dark:text-zinc-300 hover:text-zinc-900 dark:hover:text-white transition-colors">
                      <div className="flex items-center gap-3">
                        <svg className="w-4 h-4 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Help
                      </div>
                      <svg className="w-3 h-3 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                      </svg>
                    </button>

                    <button 
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-3 py-2.5 mt-1 rounded-xl text-xs font-bold bg-zinc-100 hover:bg-red-500/10 dark:bg-[#252530] dark:hover:bg-red-500/10 dark:text-zinc-300 hover:text-red-500 transition-all"
                    >
                      <svg className="w-4 h-4 rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Log out
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Profile Bar */}
            <div className="p-4 border-t border-zinc-200 dark:border-[#1a1a24] bg-zinc-50/50 dark:bg-[#07070b]/60 flex items-center justify-between">
              <div 
                onClick={() => setProfileMenuOpen(!profileMenuOpen)}
                className="flex items-center gap-3 cursor-pointer group hover:opacity-85 transition-opacity"
              >
                <div className="h-9 w-9 rounded-full bg-gradient-to-tr from-rose-400 to-[#e056fd] flex items-center justify-center font-bold text-sm text-white group-hover:scale-105 transition-transform animate-pulse-slow">
                  {profile.name.split(" ").map(n => n[0]).join("").substring(0, 2).toUpperCase()}
                </div>
                <div className="truncate max-w-[125px]">
                  <h3 className="text-xs font-bold text-zinc-800 dark:text-zinc-200 truncate">{profile.name}</h3>
                  <p className="text-[9px] font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wide truncate">{profile.plan}</p>
                </div>
              </div>

              <div className="flex gap-2">
                <button 
                  onClick={(e) => {
                    e.stopPropagation(); // Avoid opening popover
                    toggleTheme();
                  }}
                  className="p-2 rounded-lg text-zinc-500 hover:text-zinc-900 hover:bg-zinc-200 dark:text-zinc-400 dark:hover:text-white dark:hover:bg-zinc-800/40 transition-colors"
                  title="Toggle Light/Dark Theme"
                >
                  {isDarkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4 text-zinc-700" />}
                </button>
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    setProfileModalOpen(true);
                  }}
                  className="p-2 rounded-lg text-zinc-500 hover:text-zinc-900 hover:bg-zinc-200 dark:text-zinc-400 dark:hover:text-white dark:hover:bg-zinc-800/40 transition-colors"
                >
                  <Settings className="w-4 h-4" />
                </button>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* -------------------------------------------------------------
          MAIN CHAT CONTENT
          ------------------------------------------------------------- */}
      <main className="flex-1 h-full flex flex-col z-10 bg-zinc-50/95 dark:bg-[#07070c]/95 backdrop-blur-sm relative transition-colors duration-300">
        
        {/* Header toolbar */}
        <header className="px-6 py-4 flex items-center justify-between border-b border-zinc-200 dark:border-[#1a1a24] bg-white/80 dark:bg-[#0a0a10]/80 backdrop-blur-md">
          <div className="flex items-center gap-4">
            {!sidebarOpen && (
              <button 
                onClick={() => setSidebarOpen(true)}
                className="p-2 rounded-lg text-zinc-500 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:text-white dark:hover:bg-zinc-800/40 transition-colors mr-2"
              >
                <PanelLeftClose className="w-4 h-4 rotate-180" />
              </button>
            )}

            <h1 className="text-lg font-bold tracking-wide text-zinc-800 dark:text-zinc-100">
              {threads.find(t => t.id === activeThreadId)?.title || "New Chat"}
            </h1>

            {/* Dynamic AI Models Selector Dropdown */}
            <div className="relative">
              <button 
                onClick={() => setModelDropdownOpen(prev => !prev)}
                className="flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold bg-zinc-100 dark:bg-[#11111a] border border-zinc-200 dark:border-[#1a1a24] text-zinc-700 dark:text-zinc-300 hover:border-zinc-400 dark:hover:border-zinc-700 transition-all"
              >
                <Sparkles className="w-3.5 h-3.5 text-[#e056fd]" />
                <span>{selectedModel}</span>
                <ChevronDown className="w-3 h-3 text-zinc-500" />
              </button>

              {modelDropdownOpen && (
                <div className="absolute top-full mt-2 left-0 w-52 rounded-xl border border-zinc-200 dark:border-[#1a1a24] bg-white dark:bg-[#0c0c12] shadow-2xl p-1.5 z-20 text-zinc-800 dark:text-white">
                  <div className="px-2.5 py-1.5 text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-widest">Select AI Engine</div>
                  {[
                    "OpenAI (GPT-4o)",
                    "Gemini (Gemini 1.5 Pro)",
                    "Claude (Claude 3.5 Sonnet)",
                    "Ollama (Llama 3 Local)",
                    "Mistral (Mistral Large)"
                  ].map(m => (
                    <button
                      key={m}
                      onClick={() => {
                        setSelectedModel(m);
                        setModelDropdownOpen(false);
                      }}
                      className={`w-full text-left px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${m === selectedModel ? "bg-[#e056fd]/15 text-[#e056fd]" : "hover:bg-zinc-100 dark:hover:bg-zinc-800/40 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white"}`}
                    >
                      {m}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button 
              onClick={triggerFileSelect}
              className="p-2 rounded-lg text-zinc-500 hover:text-zinc-950 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800/40 transition-colors"
              title="Upload file for RAG context"
            >
              <Paperclip className="w-4.5 h-4.5" />
            </button>
            <Link 
              href="/" 
              className="px-4.5 py-2.5 rounded-xl text-xs font-bold text-zinc-700 hover:text-zinc-900 bg-zinc-200 hover:bg-zinc-300 dark:bg-zinc-800/60 dark:text-white dark:hover:bg-zinc-850 transition-all border border-zinc-300 dark:border-zinc-700/50 flex items-center justify-center"
            >
              Back to Home
            </Link>
          </div>
        </header>

        {/* Scrollable Message window */}
        <div className="flex-1 overflow-y-auto px-6 py-8 space-y-6 max-w-4xl mx-auto w-full">
          {activeMessages.map((msg) => (
            <div 
              key={msg.id}
              className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}
            >
              {msg.role === "user" ? (
                /* User Bubble */
                <div className="flex flex-col items-end max-w-[80%]">
                  <div className="px-5 py-3.5 rounded-3xl bg-gradient-to-r from-[#e056fd] to-[#be2edd] text-white text-sm font-semibold shadow-[0_4px_15px_rgba(224,86,253,0.2)] text-left">
                    {msg.content}
                  </div>
                  <span className="text-[9px] text-zinc-400 dark:text-zinc-500 font-bold mt-1.5 flex items-center gap-1">
                    {msg.time} {msg.status === "read" && <Check className="w-3.5 h-3.5 text-[#e056fd]" />}
                  </span>
                </div>
              ) : (
                /* Assistant Glow Card */
                <div className="relative group max-w-[85%] p-5 rounded-2xl border border-zinc-200 bg-white dark:border-zinc-800/80 dark:bg-[#0d0d12]/95 shadow-[0_8px_30px_rgba(0,0,0,0.05)] dark:shadow-[0_8px_30px_rgba(0,0,0,0.55)] hover:border-[#e056fd]/30 dark:hover:border-[#e056fd]/30 transition-all duration-300 text-zinc-700 dark:text-zinc-300">
                  <div className="absolute top-0 left-0 h-full w-[3px] bg-gradient-to-b from-[#e056fd] to-blue-500 rounded-l-2xl" />
                  
                  {/* Bubble header */}
                  <div className="flex items-center gap-2.5 mb-3">
                    <div className="h-6 w-6 rounded-lg bg-zinc-100 border border-zinc-200 dark:bg-[#14141d] dark:border-zinc-800 text-[#e056fd] flex items-center justify-center shadow-[0_0_10px_rgba(224,86,253,0.15)]">
                      <Sparkles className="w-3.5 h-3.5" />
                    </div>
                    <div>
                      <h4 className="text-xs font-extrabold text-zinc-800 dark:text-zinc-200">Nexus-AI</h4>
                      <p className="text-[8px] text-zinc-400 dark:text-zinc-500 uppercase tracking-widest font-bold">Engine</p>
                    </div>
                    <span className="text-[9px] text-zinc-400 dark:text-zinc-500 ml-auto">{msg.time}</span>
                  </div>

                  {/* Message content */}
                  <p className="text-sm leading-relaxed mb-4 whitespace-pre-wrap">{msg.content}</p>

                  {/* Controls */}
                  <div className="flex items-center gap-3 pt-3 border-t border-zinc-100 dark:border-zinc-900/60">
                    <button className="p-1 rounded text-zinc-400 hover:text-zinc-900 dark:text-zinc-500 dark:hover:text-white transition-colors" title="Copy reply">
                      <Copy className="w-3.5 h-3.5" />
                    </button>
                    <button className="p-1 rounded text-zinc-400 hover:text-zinc-900 dark:text-zinc-500 dark:hover:text-white transition-colors" title="Like reply">
                      <ThumbsUp className="w-3.5 h-3.5" />
                    </button>
                    <button className="p-1 rounded text-zinc-400 hover:text-zinc-900 dark:text-zinc-500 dark:hover:text-white transition-colors" title="Dislike reply">
                      <ThumbsDown className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* Active typing loader sweep */}
          {isStreaming && (
            <div className="flex items-center gap-1.5 text-[#e056fd] font-semibold text-xs ml-4">
              <span className="h-1.5 w-1.5 rounded-full bg-[#e056fd] animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="h-1.5 w-1.5 rounded-full bg-[#e056fd] animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="h-1.5 w-1.5 rounded-full bg-[#e056fd] animate-bounce" style={{ animationDelay: "300ms" }} />
              <span className="ml-1 text-[10px] text-zinc-500 dark:text-zinc-400 uppercase tracking-widest font-bold animate-pulse">Streaming from {selectedModel}</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Floating Bottom Input */}
        <div className="p-6 border-t border-zinc-200 dark:border-[#1a1a24] bg-white dark:bg-[#0a0a10]/50">
          
          {/* HITL Pending Approval Control Panel */}
          {pendingApproval && (
            <motion.div 
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className="max-w-4xl mx-auto mb-4 p-5 rounded-2xl border border-yellow-500/30 bg-yellow-500/5 dark:bg-yellow-500/10 backdrop-blur-md shadow-lg flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              <div className="flex items-start gap-3">
                <span className="p-2 rounded-xl bg-yellow-500/20 text-yellow-500 animate-pulse">⚠️</span>
                <div>
                  <h4 className="text-xs font-black text-yellow-500 uppercase tracking-widest">Manual Confirmation Required</h4>
                  <p className="text-xs text-zinc-650 dark:text-zinc-400 mt-1 font-semibold leading-relaxed">
                    Tool execution paused. Execute high-risk action: <code className="text-[10px] bg-zinc-200 dark:bg-zinc-800 px-1.5 py-0.5 rounded font-mono font-bold text-yellow-600 dark:text-yellow-400">{pendingApproval.tool_name}</code>?
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 shrink-0 self-end md:self-auto">
                <button 
                  type="button" 
                  onClick={handleReject}
                  className="px-4 py-2.5 rounded-xl border border-rose-500/30 hover:bg-rose-500/10 text-rose-500 font-extrabold text-xs transition-colors"
                >
                  Cancel & Reject
                </button>
                <button 
                  type="button" 
                  onClick={handleApprove}
                  className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:scale-105 active:scale-95 text-white font-extrabold text-xs transition-all shadow-[0_0_15px_rgba(16,185,129,0.3)]"
                >
                  Approve & Execute
                </button>
              </div>
            </motion.div>
          )}

          {/* Selected File Preview Chip */}
          {selectedFile && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`max-w-4xl mx-auto mb-3 flex items-center justify-between p-2.5 px-4 rounded-xl border bg-white dark:bg-[#11111a] text-xs shadow-md ${uploadError ? "border-rose-500/30 text-rose-500" : "border-zinc-200 dark:border-zinc-800 text-zinc-700 dark:text-zinc-300"}`}
            >
              <div className="flex items-center gap-2.5">
                <FileText className={`w-4 h-4 ${uploadError ? "text-rose-500" : "text-[#e056fd]"}`} />
                <span className="font-bold truncate max-w-[250px]">{selectedFile.name}</span>
                {isFileUploading ? (
                  <span className="text-[10px] text-[#e056fd] font-semibold animate-pulse tracking-wide flex items-center gap-1.5">
                    <span className="inline-block w-1.5 h-1.5 rounded-full bg-[#e056fd] animate-ping" />
                    Uploading & Indexing into Qdrant...
                  </span>
                ) : uploadError ? (
                  <span className="text-[10px] text-rose-500 font-bold">{uploadError}</span>
                ) : (
                  <span className="text-[10px] text-emerald-500 font-bold flex items-center gap-1">
                    <Check className="w-3 h-3 text-emerald-500" />
                    Indexed Successfully
                  </span>
                )}
              </div>
              <button 
                type="button" 
                onClick={handleRemoveFile}
                className="p-1 rounded-full hover:bg-zinc-100 dark:hover:bg-zinc-850 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 transition-colors"
                title="Remove attachment"
                disabled={isFileUploading}
              >
                <X className="w-4 h-4" />
              </button>
            </motion.div>
          )}

          <div className="max-w-4xl mx-auto flex items-center bg-zinc-100 dark:bg-[#11111a] border border-zinc-200 dark:border-[#1a1a24] focus-within:border-[#e056fd]/50 rounded-2xl px-4 py-3.5 text-zinc-700 dark:text-zinc-300 transition-colors shadow-[0_10px_30px_rgba(0,0,0,0.03)] dark:shadow-[0_10px_30px_rgba(0,0,0,0.6)]">
            <button 
              onClick={triggerFileSelect}
              className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-700 hover:bg-zinc-200 dark:text-zinc-500 dark:hover:text-white dark:hover:bg-zinc-800/40 transition-colors mr-2"
              title="Attach document"
            >
              <Paperclip className="w-4.5 h-4.5" />
            </button>

            <input 
              type="text" 
              placeholder="Ask anything..." 
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyDown={handleKeyPress}
              className="bg-transparent border-none outline-none text-sm w-full text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 font-semibold"
              disabled={isStreaming}
            />

            <div className="flex items-center gap-2 ml-4">
              <button className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-700 hover:bg-zinc-200 dark:text-zinc-500 dark:hover:text-white dark:hover:bg-zinc-800/40 transition-colors">
                <Mic className="w-4.5 h-4.5" />
              </button>
              
              <button 
                onClick={handleSendMessage}
                disabled={isStreaming}
                className="p-2.5 rounded-xl bg-gradient-to-r from-[#e056fd] to-[#be2edd] text-white hover:scale-105 active:scale-95 disabled:opacity-50 transition-transform shadow-[0_0_15px_rgba(224,86,253,0.3)]"
              >
                <Send className="w-4.5 h-4.5 fill-white" />
              </button>
            </div>
          </div>
        </div>
      </main>

      {/* -------------------------------------------------------------
          DYNAMIC PROFILE SETTINGS MODAL
          ------------------------------------------------------------- */}
      <AnimatePresence>
        {profileModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
            <motion.div 
              initial={{ opacity: 0, scale: 0.95, y: 15 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 15 }}
              className="w-full max-w-md p-6 rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0d0d12] shadow-2xl relative text-zinc-800 dark:text-white"
            >
              {/* Close Button */}
              <button 
                onClick={() => setProfileModalOpen(false)}
                className="absolute top-4 right-4 p-1.5 rounded-lg text-zinc-500 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>

              {/* Title */}
              <div className="flex items-center gap-3 mb-6">
                <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-[#e056fd] to-blue-500 flex items-center justify-center text-white">
                  <User className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-extrabold">Profile Settings</h3>
                  <p className="text-[10px] text-zinc-500 dark:text-zinc-400 font-bold uppercase tracking-wider">Configure your smart workspace parameters</p>
                </div>
              </div>

              {/* Form settings */}
              <form onSubmit={handleSaveProfile} className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest block">Display Name</label>
                  <input 
                    type="text" 
                    value={inputName}
                    onChange={(e) => setInputName(e.target.value)}
                    placeholder="Vansh pratap"
                    className="w-full bg-zinc-100 dark:bg-[#111118] border border-zinc-200 dark:border-zinc-800 rounded-xl px-4 py-3 text-sm font-semibold outline-none focus:border-[#e056fd]/50 transition-colors text-zinc-800 dark:text-white"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest block">Email Address</label>
                  <input 
                    type="email" 
                    value={inputEmail}
                    onChange={(e) => setInputEmail(e.target.value)}
                    placeholder="vansh@nexusai.com"
                    className="w-full bg-zinc-100 dark:bg-[#111118] border border-zinc-200 dark:border-zinc-800 rounded-xl px-4 py-3 text-sm font-semibold outline-none focus:border-[#e056fd]/50 transition-colors text-zinc-800 dark:text-white"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest block">Subscription Plan</label>
                  <select 
                    value={inputPlan}
                    onChange={(e) => setInputPlan(e.target.value)}
                    className="w-full bg-zinc-100 dark:bg-[#111118] border border-zinc-200 dark:border-zinc-800 rounded-xl px-4 py-3 text-sm font-semibold outline-none focus:border-[#e056fd]/50 transition-colors text-zinc-800 dark:text-white cursor-pointer"
                  >
                    <option value="Free Plan">Free Plan (Trial)</option>
                    <option value="Nexus Pro">Nexus Pro ($20/mo)</option>
                    <option value="Nexus Enterprise">Nexus Enterprise (Custom)</option>
                  </select>
                </div>

                <div className="flex gap-3 pt-4 border-t border-zinc-100 dark:border-zinc-900/60 mt-6">
                  <button 
                    type="button"
                    onClick={() => setProfileModalOpen(false)}
                    className="flex-1 py-3 rounded-xl text-xs font-bold bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-850 dark:hover:bg-zinc-700/80 text-zinc-700 dark:text-zinc-200 transition-colors"
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit"
                    className="flex-1 py-3 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-[#e056fd] to-[#be2edd] transition-transform hover:scale-[1.02] active:scale-[0.98]"
                  >
                    Save Changes
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default dynamic(() => Promise.resolve(ChatPage), { ssr: false });
