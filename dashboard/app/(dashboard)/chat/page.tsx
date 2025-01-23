"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Bot, Send, User } from "lucide-react";
import { useApi } from "@/hooks/use-api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function ChatPage() {
  const api = useApi();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await api.post("/ai/chat", {
        message: input,
        conversation_id: "default",
      });
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: res.data.response,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error("Chat error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="h-[calc(100vh-200px)] flex flex-col">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            AI Security Analyst
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto mb-4 space-y-4 pr-4">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
                <Bot className="h-12 w-12 mb-4 opacity-50" />
                <p className="text-center max-w-md">
                  Ask me about security events, detections, or get help with incident response.
                </p>
              </div>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-2xl rounded-lg px-4 py-2 ${
                      msg.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted"
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      {msg.role === "assistant" ? (
                        <Bot className="h-4 w-4" />
                      ) : (
                        <User className="h-4 w-4" />
                      )}
                      <span className="text-xs opacity-70">
                        {msg.role === "assistant" ? "AI Analyst" : "You"}
                      </span>
                    </div>
                    <p className="whitespace-pre-wrap text-sm">{msg.content}</p>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-muted rounded-lg px-4 py-2">
                  <div className="flex items-center gap-2">
                    <Bot className="h-4 w-4 animate-pulse" />
                    <span className="text-xs">Analyzing...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about security events..."
              disabled={isLoading}
              className="flex-1 rounded-lg border border-input bg-background px-3 py-2 text-sm placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <Button type="submit" disabled={isLoading || !input.trim()}>
              <Send className="h-4 w-4 mr-2" />
              Send
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
