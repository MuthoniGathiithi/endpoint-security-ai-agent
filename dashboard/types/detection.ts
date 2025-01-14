export type DetectionStatus = "new" | "in_progress" | "resolved" | "false_positive";
export type DetectionSeverity = "low" | "medium" | "high" | "critical";

export interface Detection {
  id: number;
  title: string;
  description: string;
  status: DetectionStatus;
  severity: DetectionSeverity;
  confidence: number;
  source: string;
  endpoint_id?: string | null;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface DetectionStats {
  total: number;
  by_status: Record<string, number>;
  by_severity: Record<string, number>;
  by_source: Record<string, number>;
  recent: Detection[];
}
