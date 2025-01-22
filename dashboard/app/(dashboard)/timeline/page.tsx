"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useApi } from "@/hooks/use-api";
import type { Detection } from "@/types/detection";
import { AlertCircle, Clock } from "lucide-react";

export default function TimelinePage() {
  const api = useApi();
  const [detections, setDetections] = useState<Detection[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.get("/detections", { params: { limit: 50 } });
        setDetections(res.data);
      } catch (err) {
        console.error("Failed to load timeline:", err);
      }
    };
    load();
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5" />
            Incident Timeline
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {detections.map((detection, idx) => (
              <div key={detection.id} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
                    <AlertCircle className="h-5 w-5 text-primary-foreground" />
                  </div>
                  {idx < detections.length - 1 && (
                    <div className="w-1 h-16 bg-border mt-2" />
                  )}
                </div>
                <div className="flex-1 pb-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold">{detection.title}</h3>
                      <p className="text-sm text-muted-foreground mt-1">
                        {detection.description}
                      </p>
                      <div className="flex gap-2 mt-2">
                        <span className="text-xs bg-muted px-2 py-1 rounded">
                          {detection.severity.toUpperCase()}
                        </span>
                        <span className="text-xs bg-muted px-2 py-1 rounded">
                          {detection.source}
                        </span>
                      </div>
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {new Date(detection.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
