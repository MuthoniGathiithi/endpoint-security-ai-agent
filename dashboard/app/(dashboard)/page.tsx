"use client";

import { useEffect, useState } from "react";
import { useWebSocket } from "@/hooks/use-websocket";
import { useApi } from "@/hooks/use-api";
import type { Detection, DetectionStats } from "@/types/detection";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Terminal, ShieldAlert, AlertCircle, Info } from "lucide-react";

export default function DashboardPage() {
  const api = useApi();
  const { isConnected } = useWebSocket(
    process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws?client_id=dashboard"
  );

  const [detections, setDetections] = useState<Detection[]>([]);
  const [stats, setStats] = useState<DetectionStats | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [detRes, statsRes] = await Promise.all([
          api.get("/detections", { params: { limit: 20 } }),
          api.get("/detections/stats/summary"),
        ]);
        setDetections(detRes.data);
        setStats(statsRes.data);
      } catch (e) {
        console.error("Failed to load dashboard data", e);
      }
    };
    load();
  }, []);

  const total = stats?.total ?? 0;
  const critical = stats?.by_severity?.critical ?? 0;
  const high = stats?.by_severity?.high ?? 0;
  const medLow = (stats?.by_severity?.medium ?? 0) + (stats?.by_severity?.low ?? 0);

  return (
    <div className="container mx-auto px-4 py-8 space-y-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Alerts</CardTitle>
            <Terminal className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical</CardTitle>
            <ShieldAlert className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-500">{critical}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">High</CardTitle>
            <AlertCircle className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-500">{high}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Medium / Low</CardTitle>
            <Info className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-500">{medLow}</div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="col-span-2">
          <CardHeader>
            <CardTitle>Recent Alerts</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {detections.length === 0 ? (
                <p className="text-muted-foreground text-center py-8">
                  {isConnected
                    ? "No recent alerts. Everything looks quiet."
                    : "Connecting to backend..."}
                </p>
              ) : (
                detections.map((d) => (
                  <Alert
                    key={d.id}
                    className="border-l-4"
                    style={{
                      borderLeftColor:
                        d.severity === "critical"
                          ? "#ef4444"
                          : d.severity === "high"
                          ? "#f97316"
                          : d.severity === "medium"
                          ? "#eab308"
                          : "#3b82f6",
                    }}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <AlertTitle className="font-semibold">{d.title}</AlertTitle>
                        <AlertDescription className="mt-1 text-sm">
                          <p>{d.description}</p>
                          <p className="text-xs text-muted-foreground mt-1">
                            Source: {d.source} • Severity: {d.severity.toUpperCase()}
                          </p>
                        </AlertDescription>
                      </div>
                      <Button size="sm" variant="outline" className="shrink-0">
                        View
                      </Button>
                    </div>
                  </Alert>
                ))
              )}
            </div>
          </CardContent>
        </Card>

        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full justify-start">
                View All Detections
              </Button>
              <Button variant="outline" className="w-full justify-start">
                Run Demo Attack
              </Button>
              <Button variant="outline" className="w-full justify-start">
                Open AI Analyst Chat
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>System Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Backend API</span>
                  <span className={isConnected ? "text-green-500" : "text-red-500"}>
                    {isConnected ? "Connected" : "Disconnected"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Database</span>
                  <span className="text-green-500">Online</span>
                </div>
                <div className="flex justify-between">
                  <span>AI Models</span>
                  <span className="text-green-500">Ready</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
