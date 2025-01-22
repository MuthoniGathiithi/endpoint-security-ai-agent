"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useApi } from "@/hooks/use-api";
import { Search, Zap } from "lucide-react";

export default function HuntingPage() {
  const api = useApi();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const res = await api.get("/detections", {
        params: { search: query, limit: 20 },
      });
      setResults(res.data);
    } catch (err) {
      console.error("Search error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const quickQueries = [
    "Ransomware activity",
    "C2 beaconing",
    "PowerShell execution",
    "Process injection",
  ];

  return (
    <div className="container mx-auto px-4 py-8 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5" />
            Threat Hunting
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for threats, IOCs, or behaviors..."
              className="flex-1 rounded-lg border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <Button type="submit" disabled={isLoading}>
              <Zap className="h-4 w-4 mr-2" />
              Hunt
            </Button>
          </form>

          <div className="space-y-2">
            <p className="text-sm text-muted-foreground">Quick queries:</p>
            <div className="flex flex-wrap gap-2">
              {quickQueries.map((q) => (
                <Button
                  key={q}
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setQuery(q);
                    // Auto-search
                  }}
                >
                  {q}
                </Button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Results ({results.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {results.map((r) => (
                <div
                  key={r.id}
                  className="p-3 border rounded-lg hover:bg-muted/50"
                >
                  <p className="font-medium">{r.title}</p>
                  <p className="text-sm text-muted-foreground">{r.description}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
