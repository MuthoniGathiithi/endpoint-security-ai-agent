"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useApi } from "@/hooks/use-api";
import { Server, AlertTriangle, CheckCircle } from "lucide-react";

interface Endpoint {
  id: string;
  hostname: string;
  ip_address: string;
  os: string;
  status: "online" | "offline";
  last_seen: string;
  threat_count: number;
}

export default function EndpointsPage() {
  const api = useApi();
  const [endpoints, setEndpoints] = useState<Endpoint[]>([]);

  useEffect(() => {
    // Mock endpoints data - in production, fetch from API
    setEndpoints([
      {
        id: "ep-001",
        hostname: "workstation-01",
        ip_address: "192.168.1.100",
        os: "Windows 11",
        status: "online",
        last_seen: new Date().toISOString(),
        threat_count: 3,
      },
      {
        id: "ep-002",
        hostname: "server-03",
        ip_address: "192.168.1.50",
        os: "Ubuntu 22.04",
        status: "online",
        last_seen: new Date().toISOString(),
        threat_count: 1,
      },
      {
        id: "ep-003",
        hostname: "laptop-07",
        ip_address: "192.168.1.75",
        os: "macOS 14",
        status: "online",
        last_seen: new Date().toISOString(),
        threat_count: 0,
      },
    ]);
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Server className="h-5 w-5" />
            Managed Endpoints
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2 px-4">Hostname</th>
                  <th className="text-left py-2 px-4">IP Address</th>
                  <th className="text-left py-2 px-4">OS</th>
                  <th className="text-left py-2 px-4">Status</th>
                  <th className="text-left py-2 px-4">Threats</th>
                  <th className="text-left py-2 px-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                {endpoints.map((ep) => (
                  <tr key={ep.id} className="border-b hover:bg-muted/50">
                    <td className="py-3 px-4 font-medium">{ep.hostname}</td>
                    <td className="py-3 px-4">{ep.ip_address}</td>
                    <td className="py-3 px-4">{ep.os}</td>
                    <td className="py-3 px-4">
                      <span className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500" />
                        {ep.status}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      {ep.threat_count > 0 ? (
                        <span className="flex items-center gap-2 text-red-500">
                          <AlertTriangle className="h-4 w-4" />
                          {ep.threat_count}
                        </span>
                      ) : (
                        <span className="text-green-500">0</span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline">
                          Isolate
                        </Button>
                        <Button size="sm" variant="outline">
                          Scan
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
