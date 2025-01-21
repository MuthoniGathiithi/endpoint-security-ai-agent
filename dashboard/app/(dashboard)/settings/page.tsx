"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Settings, Save } from "lucide-react";
import { useState } from "react";

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    alertThreshold: 0.7,
    autoRespond: true,
    notificationsEnabled: true,
    darkMode: true,
  });

  const handleSave = () => {
    console.log("Settings saved:", settings);
  };

  return (
    <div className="container mx-auto px-4 py-8 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            System Settings
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">
              Alert Confidence Threshold
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={settings.alertThreshold}
              onChange={(e) =>
                setSettings({
                  ...settings,
                  alertThreshold: parseFloat(e.target.value),
                })
              }
              className="w-full"
            />
            <p className="text-xs text-muted-foreground mt-1">
              Current: {(settings.alertThreshold * 100).toFixed(0)}%
            </p>
          </div>

          <div>
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={settings.autoRespond}
                onChange={(e) =>
                  setSettings({ ...settings, autoRespond: e.target.checked })
                }
              />
              <span className="text-sm font-medium">Auto-respond to threats</span>
            </label>
          </div>

          <div>
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={settings.notificationsEnabled}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    notificationsEnabled: e.target.checked,
                  })
                }
              />
              <span className="text-sm font-medium">Enable notifications</span>
            </label>
          </div>

          <Button onClick={handleSave}>
            <Save className="h-4 w-4 mr-2" />
            Save Settings
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Response Playbooks</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="p-3 border rounded-lg">
            <h4 className="font-medium">Ransomware Response</h4>
            <p className="text-sm text-muted-foreground">
              Kill process → Isolate host → Alert security team
            </p>
          </div>
          <div className="p-3 border rounded-lg">
            <h4 className="font-medium">C2 Beaconing</h4>
            <p className="text-sm text-muted-foreground">
              Block network → Quarantine file → Investigate
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
