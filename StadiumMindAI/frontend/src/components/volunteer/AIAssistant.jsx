import React, { useState, useRef, useEffect } from 'react';
import { Send, Brain, ChevronDown } from 'lucide-react';
import { useAI } from '../../hooks/useAI';
import Badge from '../ui/Badge';
import Card from '../ui/Card';

export default function AIAssistant({ volunteerId, volunteerName, volunteerZone, language }) {
  const { ask, loading } = useAI();
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Hello ${volunteerName || 'Volunteer'}! I'm your StadiumMind AI assistant. I'm currently monitoring ${volunteerZone || 'your zone'}. How can I help you with your shift today?`,
      timestamp: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (text = input) => {
    if (!text.trim() || loading) return;
    
    const userMsg = { role: 'user', content: text, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    try {
      const res = await ask(text, language, volunteerId, volunteerZone);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.answer,
        confidence: res.confidence,
        sources_used: res.sources_used,
        reasoning_summary: res.reasoning_summary,
        timestamp: new Date().toISOString()
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: "I'm sorry, I encountered an error connecting to the intelligence network. Please try again or contact command.",
        isError: true,
        timestamp: new Date().toISOString()
      }]);
    }
  };

  const suggestions = [
    'Where am I needed?',
    'What to do if Gate C crowds?',
    'Current emergency status?'
  ];

  return (
    <Card className="flex flex-col h-[600px] p-0 overflow-hidden">
      <div className="bg-blue-600/20 border-b border-blue-500/30 p-4 flex items-center gap-3">
        <div className="bg-blue-500 p-2 rounded-lg">
          <Brain className="h-5 w-5 text-white" />
        </div>
        <div>
          <h3 className="font-bold text-lg">AI Co-Pilot</h3>
          <p className="text-xs text-blue-200">Powered by Google Gemini</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4" role="log" aria-live="polite">
        {messages.map((msg, i) => (
          <div key={i} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} animate-slide-up`}>
            <div className={`max-w-[85%] rounded-2xl p-4 ${
              msg.role === 'user' 
                ? 'bg-blue-600 text-white rounded-br-none' 
                : msg.isError 
                  ? 'bg-red-500/20 border border-red-500/50 text-red-200 rounded-bl-none'
                  : 'bg-white/10 border border-white/10 text-gray-100 rounded-bl-none'
            }`}>
              <div className="whitespace-pre-wrap text-sm md:text-base">{msg.content}</div>
              
              {msg.role === 'assistant' && msg.confidence && (
                <div className="mt-3 pt-3 border-t border-white/10 flex flex-wrap gap-2 items-center text-xs">
                  <Badge status={msg.confidence > 0.8 ? 'HIGH' : 'MODERATE'} label={`${Math.round(msg.confidence * 100)}% Confidence`} />
                  {msg.sources_used?.map((src, idx) => (
                    <span key={idx} className="bg-white/5 px-2 py-1 rounded border border-white/10 text-gray-400">
                      {src}
                    </span>
                  ))}
                </div>
              )}
            </div>
            <span className="text-xs text-gray-500 mt-1 mx-1">
              {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
          </div>
        ))}
        
        {loading && (
          <div className="flex items-start animate-fade-in">
            <div className="bg-white/10 border border-white/10 rounded-2xl rounded-bl-none p-4 flex gap-1">
              <div className="h-2 w-2 bg-blue-400 rounded-full typing-dot"></div>
              <div className="h-2 w-2 bg-blue-400 rounded-full typing-dot"></div>
              <div className="h-2 w-2 bg-blue-400 rounded-full typing-dot"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-white/10 bg-black/20">
        <div className="flex gap-2 mb-3 overflow-x-auto scrollbar-hide pb-1">
          {suggestions.map((s, i) => (
            <button 
              key={i} 
              onClick={() => handleSend(s)}
              disabled={loading}
              className="whitespace-nowrap text-xs bg-white/5 hover:bg-white/10 border border-white/10 rounded-full px-3 py-1.5 transition-colors disabled:opacity-50"
            >
              {s}
            </button>
          ))}
        </div>
        <form 
          onSubmit={(e) => { e.preventDefault(); handleSend(); }} 
          className="flex gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your AI Co-Pilot..."
            className="input-field flex-1"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-600/50 text-white p-3 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <Send className="h-5 w-5" />
          </button>
        </form>
      </div>
    </Card>
  );
}
