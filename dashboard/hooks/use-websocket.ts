"use client";

import { useEffect, useRef, useState, useCallback } from "react";

export interface WebSocketMessage {
  type: string;
  [key: string]: any;
}

export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const ws = useRef<WebSocket | null>(null);

  const sendMessage = useCallback((message: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
      return true;
    }
    return false;
  }, []);

  useEffect(() => {
    if (!url) return;

    const socket = new WebSocket(url);

    socket.onopen = () => {
      setIsConnected(true);
      // default subscribe to detections
      sendMessage({ type: "subscribe", channel: "detections" });
    };

    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        setMessages((prev) => [message, ...prev].slice(0, 200));
      } catch (err) {
        console.error("Error parsing WebSocket message", err);
      }
    };

    socket.onclose = () => {
      setIsConnected(false);
    };

    socket.onerror = (err) => {
      console.error("WebSocket error", err);
    };

    ws.current = socket;

    return () => {
      socket.close();
    };
  }, [url, sendMessage]);

  return { isConnected, messages, sendMessage };
}
