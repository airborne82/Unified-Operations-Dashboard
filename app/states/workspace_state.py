import asyncio
from typing import Any, TypedDict

import reflex as rx


class TabCard(TypedDict):
    id: str
    title: str
    metric: str
    caption: str
    icon: str
    tone: str
    status: str


class DetailPanel(TypedDict):
    id: str
    title: str
    caption: str
    metric: str
    delta: str
    status: str
    icon: str
    load: int
    items: list[str]


class ActivityItem(TypedDict):
    id: str
    time: str
    actor: str
    text: str
    kind: str


class QuickAction(TypedDict):
    id: str
    label: str
    icon: str


class RemoteDesktop(TypedDict):
    id: str
    name: str
    kind: str
    icon: str
    status: str
    sessions: str
    latency: str
    detail: str


class WorkspaceState(rx.State):
    active_tab: str = "operations"
    is_loading: bool = False
    action_target: str = ""
    action_note: str = ""
    last_action: str = ""
    selected_desktop: str = ""
    selected_desktop_detail: str = ""

    remote_desktops: list[RemoteDesktop] = [
        {
            "id": "rd-1",
            "name": "Citrix Desktop",
            "kind": "Citrix VDA · Pool OPS-01",
            "icon": "app-window",
            "status": "available",
            "sessions": "14 / 40 seats",
            "latency": "38 ms",
            "detail": "Published desktop · standard operator image",
        },
        {
            "id": "rd-2",
            "name": "Windows Admin VM",
            "kind": "Hyper-V · WIN-ADM-02",
            "icon": "monitor",
            "status": "available",
            "sessions": "2 / 4 seats",
            "latency": "22 ms",
            "detail": "Tier-2 admin tooling · MFA required",
        },
        {
            "id": "rd-3",
            "name": "Linux Jump Box",
            "kind": "SSH bastion · JMP-LNX-01",
            "icon": "terminal",
            "status": "available",
            "sessions": "5 active shells",
            "latency": "17 ms",
            "detail": "Session recording enabled · keys rotated 03:10 Z",
        },
        {
            "id": "rd-4",
            "name": "SOC Analyst VDI",
            "kind": "Citrix VDI · Pool SOC-03",
            "icon": "shield-check",
            "status": "busy",
            "sessions": "18 / 18 seats",
            "latency": "51 ms",
            "detail": "Pool saturated · queue for next release",
        },
        {
            "id": "rd-5",
            "name": "Database Console",
            "kind": "Jump host · DB-CON-01",
            "icon": "database",
            "status": "restricted",
            "sessions": "1 / 2 seats",
            "latency": "29 ms",
            "detail": "Change ticket required · CR-2291 active",
        },
        {
            "id": "rd-6",
            "name": "Emergency Breakglass Workstation",
            "kind": "Isolated · BG-WS-00",
            "icon": "triangle-alert",
            "status": "sealed",
            "sessions": "0 / 1 seat",
            "latency": "—",
            "detail": "Dual approval · opens audited breakglass session",
        },
    ]

    tab_cards: dict[str, list[TabCard]] = {
        "operations": [
            {
                "id": "op-c1",
                "title": "Dispatch Board",
                "metric": "12 assigned",
                "caption": "Crew tasking queue synced 40s ago",
                "icon": "clipboard-list",
                "tone": "cyan",
                "status": "nominal",
            },
            {
                "id": "op-c2",
                "title": "Open Incidents",
                "metric": "3 active",
                "caption": "1 sev-1 on edge cluster DELTA-9",
                "icon": "triangle-alert",
                "tone": "amber",
                "status": "critical",
            },
            {
                "id": "op-c3",
                "title": "Shift Coverage",
                "metric": "8 / 9",
                "caption": "One relief operator unconfirmed",
                "icon": "users",
                "tone": "amber",
                "status": "watch",
            },
            {
                "id": "op-c4",
                "title": "Playbooks Ready",
                "metric": "24",
                "caption": "Automation runners standing by",
                "icon": "book-open",
                "tone": "cyan",
                "status": "nominal",
            },
        ],
        "pathfinders": [
            {
                "id": "net-c1",
                "title": "Mesh Integrity",
                "metric": "94.2%",
                "caption": "3 pathfinder tunnels degraded",
                "icon": "signal",
                "tone": "amber",
                "status": "watch",
            },
            {
                "id": "net-c2",
                "title": "Egress Throughput",
                "metric": "812 Mb/s",
                "caption": "Peak +11% versus 24h baseline",
                "icon": "arrow-up-right",
                "tone": "cyan",
                "status": "nominal",
            },
            {
                "id": "net-c3",
                "title": "Packet Loss",
                "metric": "0.8%",
                "caption": "Concentrated on pathfinder-5 uplink",
                "icon": "wifi-off",
                "tone": "amber",
                "status": "critical",
            },
            {
                "id": "net-c4",
                "title": "BGP Sessions",
                "metric": "18 up",
                "caption": "All peers reconverged at 03:44",
                "icon": "git-branch",
                "tone": "cyan",
                "status": "nominal",
            },
        ],
        "systems": [
            {
                "id": "sys-c1",
                "title": "Compute Pool",
                "metric": "68% load",
                "caption": "Autoscale headroom nominal",
                "icon": "server",
                "tone": "cyan",
                "status": "nominal",
            },
            {
                "id": "sys-c2",
                "title": "Storage Tier",
                "metric": "77% used",
                "caption": "Cold tier migration scheduled 06:00",
                "icon": "hard-drive",
                "tone": "amber",
                "status": "watch",
            },
            {
                "id": "sys-c3",
                "title": "Patch Level",
                "metric": "96% current",
                "caption": "7 hosts pending kernel rollout",
                "icon": "shield-check",
                "tone": "cyan",
                "status": "nominal",
            },
            {
                "id": "sys-c4",
                "title": "Change Queue",
                "metric": "CR-2291",
                "caption": "Window opens in 42 minutes",
                "icon": "calendar-clock",
                "tone": "amber",
                "status": "watch",
            },
        ],
        "gladius": [
            {
                "id": "gl-c1",
                "title": "Model Health",
                "metric": "0.94 F1",
                "caption": "Routing model v18 retrained 04:07",
                "icon": "brain-circuit",
                "tone": "cyan",
                "status": "nominal",
            },
            {
                "id": "gl-c2",
                "title": "Advisories",
                "metric": "4 new",
                "caption": "Predictive reroute suggestions ready",
                "icon": "sparkles",
                "tone": "amber",
                "status": "watch",
            },
            {
                "id": "gl-c3",
                "title": "Inference Latency",
                "metric": "112 ms",
                "caption": "p95 within command SLA",
                "icon": "gauge",
                "tone": "cyan",
                "status": "nominal",
            },
            {
                "id": "gl-c4",
                "title": "Guardrails",
                "metric": "0 breaches",
                "caption": "Human approval required for tier-1",
                "icon": "lock",
                "tone": "cyan",
                "status": "nominal",
            },
        ],
        "desktop": [
            {
                "id": "dsk-c1",
                "title": "Managed Endpoints",
                "metric": "1,284",
                "caption": "19 offline beyond 24h",
                "icon": "monitor",
                "tone": "cyan",
                "status": "nominal",
            },
            {
                "id": "dsk-c2",
                "title": "Remote Sessions",
                "metric": "7 live",
                "caption": "2 awaiting operator consent",
                "icon": "monitor-play",
                "tone": "amber",
                "status": "watch",
            },
            {
                "id": "dsk-c3",
                "title": "Disk Encryption",
                "metric": "98.4%",
                "caption": "21 endpoints non-compliant",
                "icon": "shield",
                "tone": "amber",
                "status": "watch",
            },
            {
                "id": "dsk-c4",
                "title": "Software Rollout",
                "metric": "Ring 2",
                "caption": "Agent 5.2.1 at 61% deployed",
                "icon": "package",
                "tone": "cyan",
                "status": "nominal",
            },
        ],
        "calendar": [
            {
                "id": "cal-c1",
                "title": "Next Briefing",
                "metric": "04:51 Z",
                "caption": "Ops sync · Bridge 2 · 9 invited",
                "icon": "calendar",
                "tone": "cyan",
                "status": "nominal",
            },
            {
                "id": "cal-c2",
                "title": "Change Windows",
                "metric": "2 today",
                "caption": "CR-2291 and CR-2297 overlap 06:00",
                "icon": "calendar-clock",
                "tone": "amber",
                "status": "watch",
            },
            {
                "id": "cal-c3",
                "title": "On-call Handover",
                "metric": "08:00 Z",
                "caption": "Runbook acknowledgement pending",
                "icon": "repeat",
                "tone": "amber",
                "status": "watch",
            },
            {
                "id": "cal-c4",
                "title": "Availability",
                "metric": "6 free",
                "caption": "Command staff open 05:30 - 06:15",
                "icon": "users",
                "tone": "cyan",
                "status": "nominal",
            },
        ],
        "chat": [
            {
                "id": "cht-c1",
                "title": "Active Channels",
                "metric": "14",
                "caption": "#incident-2291 highest traffic",
                "icon": "message-square",
                "tone": "cyan",
                "status": "nominal",
            },
            {
                "id": "cht-c2",
                "title": "Escalations",
                "metric": "2",
                "caption": "Awaiting duty officer response",
                "icon": "megaphone",
                "tone": "amber",
                "status": "critical",
            },
            {
                "id": "cht-c3",
                "title": "Mentions",
                "metric": "9 unread",
                "caption": "3 flagged for command review",
                "icon": "at-sign",
                "tone": "amber",
                "status": "watch",
            },
            {
                "id": "cht-c4",
                "title": "Bridge Rooms",
                "metric": "3 open",
                "caption": "Voice bridge 2 recording",
                "icon": "headphones",
                "tone": "cyan",
                "status": "nominal",
            },
        ],
        "email": [
            {
                "id": "eml-c1",
                "title": "Inbox Queue",
                "metric": "41 unread",
                "caption": "12 tagged operational priority",
                "icon": "mail",
                "tone": "cyan",
                "status": "nominal",
            },
            {
                "id": "eml-c2",
                "title": "SLA Replies Due",
                "metric": "5",
                "caption": "2 breach in under 30 minutes",
                "icon": "timer",
                "tone": "amber",
                "status": "critical",
            },
            {
                "id": "eml-c3",
                "title": "Quarantined",
                "metric": "18",
                "caption": "Phishing heuristics tightened 02:10",
                "icon": "shield-alert",
                "tone": "amber",
                "status": "watch",
            },
            {
                "id": "eml-c4",
                "title": "Distribution Lists",
                "metric": "32",
                "caption": "Command roster synced from HR",
                "icon": "list",
                "tone": "cyan",
                "status": "nominal",
            },
        ],
    }

    tab_panels: dict[str, list[DetailPanel]] = {
        "operations": [
            {
                "id": "op-p1",
                "title": "Mission Tasking",
                "caption": "Crew assignments for the current watch",
                "metric": "12 tasks",
                "delta": "+3 queued",
                "status": "nominal",
                "icon": "clipboard-list",
                "load": 62,
                "items": [
                    "TASK-4411 · Reroute BRAVO-7 traffic · Crew A",
                    "TASK-4412 · Verify DELTA-9 optics · Crew C",
                    "TASK-4415 · Stage failover config · Automation",
                ],
            },
            {
                "id": "op-p2",
                "title": "Incident Bridge",
                "caption": "Sev-1 INC-2291 · packet loss on edge",
                "metric": "00:47:12",
                "delta": "mitigating",
                "status": "critical",
                "icon": "siren",
                "load": 78,
                "items": [
                    "Comms: bridge 2 active · 11 participants",
                    "Impact: 4% of southbound sessions",
                    "Next update due 04:35 Z",
                ],
            },
            {
                "id": "op-p3",
                "title": "Readiness Posture",
                "caption": "Condition amber sustained for 3h 12m",
                "metric": "87%",
                "delta": "-4%",
                "status": "watch",
                "icon": "shield-check",
                "load": 87,
                "items": [
                    "Reserve capacity engaged in region EU-2",
                    "Two playbooks awaiting command sign-off",
                ],
            },
        ],
        "pathfinders": [
            {
                "id": "net-p1",
                "title": "Pathfinder Matrix",
                "caption": "Uplink health across 10 customer sites",
                "metric": "94.2%",
                "delta": "-1.8%",
                "status": "watch",
                "icon": "network",
                "load": 94,
                "items": [
                    "pathfinder-1 · Northwind Logistics · 0.1% loss · 18 ms",
                    "pathfinder-3 · Cirrus Telecom · 0.6% loss · 48 ms",
                    "pathfinder-5 · Andes Mining · 12% loss · 412 ms",
                ],
            },
            {
                "id": "net-p2",
                "title": "Traffic Shaping",
                "caption": "Active policies and queue pressure",
                "metric": "1.2k queued",
                "delta": "-8%",
                "status": "nominal",
                "icon": "sliders-horizontal",
                "load": 54,
                "items": [
                    "Policy OPS-PRIORITY · 40% reserved",
                    "Policy BULK-SYNC · throttled to 120 Mb/s",
                ],
            },
            {
                "id": "net-p3",
                "title": "Perimeter Events",
                "caption": "Blocked flows in the last hour",
                "metric": "318",
                "delta": "+62",
                "status": "watch",
                "icon": "shield-alert",
                "load": 41,
                "items": [
                    "Scan burst from 203.0.113.0/24 blocked",
                    "Geo rule triggered 41 times",
                ],
            },
        ],
        "systems": [
            {
                "id": "sys-p1",
                "title": "Cluster Utilisation",
                "caption": "Compute pool across 3 zones",
                "metric": "68%",
                "delta": "+6%",
                "status": "nominal",
                "icon": "cpu",
                "load": 68,
                "items": [
                    "zone-a · 24 nodes · 61% cpu · 58% mem",
                    "zone-b · 22 nodes · 72% cpu · 64% mem",
                    "zone-c · 18 nodes · 70% cpu · 71% mem",
                ],
            },
            {
                "id": "sys-p2",
                "title": "Change Control",
                "caption": "Approved windows and blockers",
                "metric": "CR-2291",
                "delta": "T-42m",
                "status": "watch",
                "icon": "git-pull-request",
                "load": 35,
                "items": [
                    "CR-2291 · kernel rollout · approved",
                    "CR-2297 · storage migration · pending CAB",
                ],
            },
            {
                "id": "sys-p3",
                "title": "Service Health",
                "caption": "Golden signals per core service",
                "metric": "99.94%",
                "delta": "stable",
                "status": "nominal",
                "icon": "activity",
                "load": 99,
                "items": [
                    "api-gateway · p95 118 ms · 0.02% errors",
                    "task-runner · p95 204 ms · 0.11% errors",
                ],
            },
        ],
        "gladius": [
            {
                "id": "gl-p1",
                "title": "Advisory Queue",
                "caption": "Model recommendations awaiting review",
                "metric": "4 pending",
                "delta": "2 high",
                "status": "watch",
                "icon": "sparkles",
                "load": 44,
                "items": [
                    "Reroute DELTA-9 to CIRRUS · confidence 0.91",
                    "Pre-scale zone-b by 4 nodes · confidence 0.84",
                    "Suppress duplicate alert group · confidence 0.79",
                ],
            },
            {
                "id": "gl-p2",
                "title": "Training Pipeline",
                "caption": "Routing model v18 · retrained 04:07 Z",
                "metric": "0.94 F1",
                "delta": "+0.02",
                "status": "nominal",
                "icon": "brain-circuit",
                "load": 94,
                "items": [
                    "Dataset: 2.1M labelled flow samples",
                    "Drift check passed · next run 10:00 Z",
                ],
            },
            {
                "id": "gl-p3",
                "title": "Autonomy Guardrails",
                "caption": "Command approval policy enforced",
                "metric": "0 breaches",
                "delta": "7d clean",
                "status": "nominal",
                "icon": "lock",
                "load": 100,
                "items": [
                    "Tier-1 actions require dual approval",
                    "All decisions written to audit ledger",
                ],
            },
        ],
        "desktop": [
            {
                "id": "dsk-p1",
                "title": "Endpoint Fleet",
                "caption": "Managed workstations by posture",
                "metric": "1,284",
                "delta": "19 offline",
                "status": "nominal",
                "icon": "monitor",
                "load": 92,
                "items": [
                    "Compliant · 1,178 endpoints",
                    "Needs attention · 87 endpoints",
                    "Quarantined · 19 endpoints",
                ],
            },
            {
                "id": "dsk-p2",
                "title": "Remote Assist",
                "caption": "Live operator sessions",
                "metric": "7 live",
                "delta": "2 waiting",
                "status": "watch",
                "icon": "monitor-play",
                "load": 47,
                "items": [
                    "OPS-114 · Crew A · 12m elapsed",
                    "OPS-118 · Crew C · consent pending",
                ],
            },
            {
                "id": "dsk-p3",
                "title": "Rollout Rings",
                "caption": "Agent 5.2.1 deployment progress",
                "metric": "61%",
                "delta": "ring 2",
                "status": "nominal",
                "icon": "package",
                "load": 61,
                "items": [
                    "Ring 1 · complete · 0 rollbacks",
                    "Ring 2 · 61% · 3 retries",
                ],
            },
        ],
        "calendar": [
            {
                "id": "cal-p1",
                "title": "Watch Schedule",
                "caption": "Next 12 hours of command events",
                "metric": "6 events",
                "delta": "1 conflict",
                "status": "watch",
                "icon": "calendar",
                "load": 55,
                "items": [
                    "04:51 Z · Ops sync briefing · Bridge 2",
                    "06:00 Z · CR-2291 change window",
                    "08:00 Z · On-call handover",
                ],
            },
            {
                "id": "cal-p2",
                "title": "Conflict Review",
                "caption": "Overlapping windows requiring a call",
                "metric": "1",
                "delta": "needs decision",
                "status": "critical",
                "icon": "calendar-x",
                "load": 20,
                "items": [
                    "CR-2291 and CR-2297 both start 06:00 Z",
                    "Recommend sequencing storage migration",
                ],
            },
            {
                "id": "cal-p3",
                "title": "Attendance",
                "caption": "Command staff availability",
                "metric": "9 invited",
                "delta": "6 accepted",
                "status": "nominal",
                "icon": "users",
                "load": 66,
                "items": [
                    "Accepted · 6 · Tentative · 2 · Declined · 1",
                ],
            },
        ],
        "chat": [
            {
                "id": "cht-p1",
                "title": "Priority Channels",
                "caption": "Rooms flagged by the incident router",
                "metric": "14 active",
                "delta": "2 escalated",
                "status": "watch",
                "icon": "message-square",
                "load": 58,
                "items": [
                    "#incident-2291 · 214 msgs/h · escalated",
                    "#network-ops · 88 msgs/h",
                    "#gladius-advisory · 31 msgs/h",
                ],
            },
            {
                "id": "cht-p2",
                "title": "Bridge Transcript",
                "caption": "Voice bridge 2 · live transcription",
                "metric": "11 on call",
                "delta": "recording",
                "status": "nominal",
                "icon": "headphones",
                "load": 73,
                "items": [
                    "04:19 Duty officer: confirm optics swap window",
                    "04:20 Crew C: spare module staged on site",
                ],
            },
            {
                "id": "cht-p3",
                "title": "Response Times",
                "caption": "Median acknowledgement per channel",
                "metric": "1m 42s",
                "delta": "-18s",
                "status": "nominal",
                "icon": "timer",
                "load": 80,
                "items": [
                    "Escalated rooms · 42s median",
                    "Standard rooms · 3m 10s median",
                ],
            },
        ],
        "email": [
            {
                "id": "eml-p1",
                "title": "Operational Inbox",
                "caption": "Priority-tagged correspondence",
                "metric": "41 unread",
                "delta": "12 priority",
                "status": "watch",
                "icon": "mail",
                "load": 49,
                "items": [
                    "Vendor SLA report · Cirrus Telecom · 02:58",
                    "Change approval · CAB board · 03:52",
                    "Escalation summary · Duty officer · 04:11",
                ],
            },
            {
                "id": "eml-p2",
                "title": "SLA Watchlist",
                "caption": "Replies approaching their deadline",
                "metric": "5 due",
                "delta": "2 critical",
                "status": "critical",
                "icon": "timer",
                "load": 30,
                "items": [
                    "TCK-8842 · 22m remaining · vendor escalation",
                    "TCK-8851 · 28m remaining · customer comms",
                ],
            },
            {
                "id": "eml-p3",
                "title": "Threat Filtering",
                "caption": "Quarantine and heuristics summary",
                "metric": "18 held",
                "delta": "+6",
                "status": "watch",
                "icon": "shield-alert",
                "load": 38,
                "items": [
                    "Phishing heuristics tightened at 02:10 Z",
                    "0 released to recipients in last 6h",
                ],
            },
        ],
    }

    tab_activity: dict[str, list[ActivityItem]] = {
        "operations": [
            {
                "id": "op-a1",
                "time": "04:21",
                "actor": "Duty Officer",
                "text": "Declared condition amber for southbound edge",
                "kind": "critical",
            },
            {
                "id": "op-a2",
                "time": "04:16",
                "actor": "Automation",
                "text": "Playbook OPS-REROUTE staged for approval",
                "kind": "warning",
            },
            {
                "id": "op-a3",
                "time": "04:02",
                "actor": "Crew C",
                "text": "Optics spare module staged at DELTA-9",
                "kind": "info",
            },
            {
                "id": "op-a4",
                "time": "03:48",
                "actor": "Command",
                "text": "Watch handover checklist completed",
                "kind": "info",
            },
        ],
        "pathfinders": [
            {
                "id": "net-a1",
                "time": "04:19",
                "actor": "Telemetry",
                "text": "pathfinder-5 packet loss crossed 10% threshold",
                "kind": "critical",
            },
            {
                "id": "net-a2",
                "time": "03:58",
                "actor": "NetOps",
                "text": "Applied shaping policy BULK-SYNC throttle",
                "kind": "warning",
            },
            {
                "id": "net-a3",
                "time": "03:44",
                "actor": "Routing",
                "text": "All BGP peers reconverged after flap",
                "kind": "info",
            },
        ],
        "systems": [
            {
                "id": "sys-a1",
                "time": "04:05",
                "actor": "CAB Board",
                "text": "CR-2291 approved for the 06:00 window",
                "kind": "warning",
            },
            {
                "id": "sys-a2",
                "time": "03:40",
                "actor": "Autoscaler",
                "text": "zone-b scaled out by 2 nodes",
                "kind": "info",
            },
            {
                "id": "sys-a3",
                "time": "03:11",
                "actor": "Patch Service",
                "text": "7 hosts deferred kernel rollout",
                "kind": "warning",
            },
        ],
        "gladius": [
            {
                "id": "gl-a1",
                "time": "04:07",
                "actor": "Gladius AI",
                "text": "Retrained routing model to v18",
                "kind": "info",
            },
            {
                "id": "gl-a2",
                "time": "03:55",
                "actor": "Gladius AI",
                "text": "Recommended reroute of DELTA-9 traffic",
                "kind": "warning",
            },
            {
                "id": "gl-a3",
                "time": "03:20",
                "actor": "Guardrail",
                "text": "Tier-1 action held for dual approval",
                "kind": "info",
            },
        ],
        "desktop": [
            {
                "id": "dsk-a1",
                "time": "04:12",
                "actor": "Endpoint Agent",
                "text": "19 endpoints reported offline beyond 24h",
                "kind": "warning",
            },
            {
                "id": "dsk-a2",
                "time": "03:50",
                "actor": "Crew A",
                "text": "Remote session OPS-114 opened",
                "kind": "info",
            },
        ],
        "calendar": [
            {
                "id": "cal-a1",
                "time": "04:00",
                "actor": "Scheduler",
                "text": "Detected overlap between CR-2291 and CR-2297",
                "kind": "critical",
            },
            {
                "id": "cal-a2",
                "time": "03:31",
                "actor": "Command",
                "text": "Ops sync briefing moved to Bridge 2",
                "kind": "info",
            },
        ],
        "chat": [
            {
                "id": "cht-a1",
                "time": "03:12",
                "actor": "#incident-2291",
                "text": "Thread escalated to duty officer",
                "kind": "warning",
            },
            {
                "id": "cht-a2",
                "time": "03:04",
                "actor": "#network-ops",
                "text": "Crew C confirmed on-site arrival",
                "kind": "info",
            },
        ],
        "email": [
            {
                "id": "eml-a1",
                "time": "02:58",
                "actor": "Cirrus Telecom",
                "text": "Vendor SLA report delivered",
                "kind": "info",
            },
            {
                "id": "eml-a2",
                "time": "02:10",
                "actor": "Mail Security",
                "text": "Phishing heuristics tightened",
                "kind": "warning",
            },
        ],
    }

    tab_actions: dict[str, list[QuickAction]] = {
        "operations": [
            {"id": "op-q1", "label": "Open Incident", "icon": "siren"},
            {"id": "op-q2", "label": "Assign Crew", "icon": "users"},
            {"id": "op-q3", "label": "Run Playbook", "icon": "play"},
        ],
        "pathfinders": [
            {
                "id": "net-q1",
                "label": "Reroute Pathfinder",
                "icon": "git-branch",
            },
            {
                "id": "net-q2",
                "label": "Throttle Policy",
                "icon": "sliders-horizontal",
            },
            {"id": "net-q3", "label": "Trace Path", "icon": "route"},
        ],
        "systems": [
            {
                "id": "sys-q1",
                "label": "Raise Change",
                "icon": "git-pull-request",
            },
            {"id": "sys-q2", "label": "Scale Pool", "icon": "server"},
            {"id": "sys-q3", "label": "Drain Node", "icon": "power"},
        ],
        "gladius": [
            {"id": "gl-q1", "label": "Approve Advisory", "icon": "check"},
            {"id": "gl-q2", "label": "Request Forecast", "icon": "sparkles"},
            {"id": "gl-q3", "label": "Retrain Model", "icon": "refresh-cw"},
        ],
        "desktop": [
            {"id": "dsk-q1", "label": "Start Remote", "icon": "monitor-play"},
            {"id": "dsk-q2", "label": "Push Package", "icon": "package"},
            {"id": "dsk-q3", "label": "Isolate Host", "icon": "shield"},
        ],
        "calendar": [
            {
                "id": "cal-q1",
                "label": "Schedule Briefing",
                "icon": "calendar-plus",
            },
            {"id": "cal-q2", "label": "Resolve Conflict", "icon": "calendar-x"},
            {"id": "cal-q3", "label": "Set Handover", "icon": "repeat"},
        ],
        "chat": [
            {"id": "cht-q1", "label": "Broadcast", "icon": "megaphone"},
            {"id": "cht-q2", "label": "Open Bridge", "icon": "headphones"},
            {
                "id": "cht-q3",
                "label": "Escalate Thread",
                "icon": "arrow-up-right",
            },
        ],
        "email": [
            {"id": "eml-q1", "label": "Draft Reply", "icon": "reply"},
            {"id": "eml-q2", "label": "Release Held", "icon": "mail-check"},
            {"id": "eml-q3", "label": "Flag Priority", "icon": "flag"},
        ],
    }

    @rx.var
    def current_tab(self) -> str:
        return self.active_tab

    @rx.var
    def current_cards(self) -> list[TabCard]:
        return self.tab_cards.get(self.active_tab, [])

    @rx.var
    def current_panels(self) -> list[DetailPanel]:
        return self.tab_panels.get(self.active_tab, [])

    @rx.var
    def current_activity(self) -> list[ActivityItem]:
        return self.tab_activity.get(self.active_tab, [])

    @rx.var
    def current_actions(self) -> list[QuickAction]:
        return self.tab_actions.get(self.active_tab, [])

    @rx.var
    def activity_count(self) -> int:
        return len(self.tab_activity.get(self.active_tab, []))

    @rx.event
    async def load_workspace(self):
        self.is_loading = True
        self.last_action = ""
        yield
        await asyncio.sleep(0.45)
        self.is_loading = False

    @rx.event
    async def switch_tab(self, tab_id: str):
        if tab_id == self.active_tab:
            return
        self.active_tab = tab_id
        self.is_loading = True
        self.last_action = ""
        yield
        await asyncio.sleep(0.45)
        self.is_loading = False

    @rx.event
    def set_action_target(self, value: str):
        self.action_target = value

    @rx.event
    def set_action_note(self, value: str):
        self.action_note = value

    @rx.event
    def run_action(self, label: str):
        self.last_action = f"{label} dispatched"
        return rx.toast(
            f"{label} dispatched to the active workspace", duration=3000
        )

    @rx.event
    def launch_desktop(self, desktop_id: str):
        for d in self.remote_desktops:
            if d["id"] == desktop_id:
                self.selected_desktop = d["name"]
                self.selected_desktop_detail = f"{d['kind']} · {d['sessions']}"
                self.last_action = f"{d['name']} session requested"
                if d["status"] == "sealed":
                    return rx.toast(
                        f"{d['name']} requires dual approval · request logged",
                        duration=3500,
                    )
                if d["status"] == "busy":
                    return rx.toast(
                        f"{d['name']} pool is saturated · you are queued",
                        duration=3500,
                    )
                if d["status"] == "restricted":
                    return rx.toast(
                        f"{d['name']} requires an active change ticket",
                        duration=3500,
                    )
                return rx.toast(
                    f"Launching {d['name']} · {d['latency']} round trip",
                    duration=3000,
                )
        return rx.toast("Remote desktop not found", duration=3000)

    @rx.event
    def clear_desktop(self):
        self.selected_desktop = ""
        self.selected_desktop_detail = ""

    @rx.event
    def submit_action(self, form_data: dict[str, Any]):
        target = str(form_data.get("target", "")).strip()
        note = str(form_data.get("note", "")).strip()
        if not target:
            return rx.toast("Enter a target before dispatching", duration=3000)
        self.action_target = ""
        self.action_note = ""
        self.last_action = f"Dispatched to {target}"
        detail = note if note else "no operator note"
        return rx.toast(f"Action queued for {target} · {detail}", duration=3500)
