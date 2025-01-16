"use client";

import axios from "axios";

const baseURL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export function useApi() {
  const client = axios.create({
    baseURL,
    headers: { "Content-Type": "application/json" },
  });

  return client;
}
