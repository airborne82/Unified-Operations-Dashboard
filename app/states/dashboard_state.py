import reflex as rx
from typing import TypedDict


class Tab(TypedDict):
    id: str
    label: str
    icon: str


class FlowPoint(TypedDict):
    t: str
    throughput: int
    latency: int


class Kpi(TypedDict):
    label: str
    value: str
    delta: str
    tone: str
    icon: str


class Event(TypedDict):
    id: str
    time: str
    title: str
    source: str
    severity: str


class Node(TypedDict):
    id: str
    name: str
    left: int
    top: int
    status: str


class DashboardState(rx.State):
    active_tab: str = "operations"
    mission_clock: str = "04:21:07 ZULU"
    posture: str = "CONDITION AMBER"

    tabs: list[Tab] = [
        {"id": "operations", "label": "Operations", "icon": "radar"},
        {"id": "pathfinders", "label": "Pathfinders", "icon": "route"},
        {"id": "systems", "label": "Systems", "icon": "cpu"},
        {"id": "gladius", "label": "Gladius AI", "icon": "brain-circuit"},
        {"id": "desktop", "label": "Desktop", "icon": "monitor"},
        {"id": "calendar", "label": "Calendar", "icon": "calendar"},
        {"id": "chat", "label": "Chat", "icon": "message-square"},
        {"id": "email", "label": "Email", "icon": "mail"},
    ]

    flow: list[FlowPoint] = [
        {"t": "00:00", "throughput": 320, "latency": 120},
        {"t": "02:00", "throughput": 412, "latency": 108},
        {"t": "04:00", "throughput": 388, "latency": 141},
        {"t": "06:00", "throughput": 501, "latency": 96},
        {"t": "08:00", "throughput": 642, "latency": 132},
        {"t": "10:00", "throughput": 588, "latency": 118},
        {"t": "12:00", "throughput": 730, "latency": 104},
        {"t": "14:00", "throughput": 694, "latency": 149},
        {"t": "16:00", "throughput": 812, "latency": 111},
    ]

    nodes: list[Node] = [
        {
            "id": "n1",
            "name": "ALPHA-1",
            "left": 14,
            "top": 24,
            "status": "nominal",
        },
        {
            "id": "n2",
            "name": "BRAVO-7",
            "left": 38,
            "top": 58,
            "status": "warning",
        },
        {
            "id": "n3",
            "name": "CIRRUS",
            "left": 61,
            "top": 31,
            "status": "nominal",
        },
        {
            "id": "n4",
            "name": "DELTA-9",
            "left": 79,
            "top": 66,
            "status": "critical",
        },
        {
            "id": "n5",
            "name": "ECHO-3",
            "left": 27,
            "top": 78,
            "status": "nominal",
        },
        {
            "id": "n6",
            "name": "GLADIUS",
            "left": 52,
            "top": 15,
            "status": "warning",
        },
    ]

    kpis: list[Kpi] = [
        {
            "label": "Active Ops",
            "value": "27",
            "delta": "+3",
            "tone": "cyan",
            "icon": "activity",
        },
        {
            "label": "Open Alerts",
            "value": "6",
            "delta": "+2",
            "tone": "amber",
            "icon": "triangle-alert",
        },
        {
            "label": "Uptime",
            "value": "99.94%",
            "delta": "stable",
            "tone": "cyan",
            "icon": "shield-check",
        },
        {
            "label": "Queue Depth",
            "value": "1.2k",
            "delta": "-8%",
            "tone": "amber",
            "icon": "layers",
        },
    ]

    events: list[Event] = [
        {
            "id": "e1",
            "time": "04:19",
            "title": "pathfinder-5 packet loss 12% · Andes Mining",
            "source": "Pathfinders",
            "severity": "critical",
        },
        {
            "id": "e2",
            "time": "04:07",
            "title": "Gladius AI retrained routing model",
            "source": "Gladius AI",
            "severity": "info",
        },
        {
            "id": "e3",
            "time": "03:52",
            "title": "Change window CR-2291 approved",
            "source": "Systems",
            "severity": "warning",
        },
        {
            "id": "e4",
            "time": "03:31",
            "title": "Ops sync briefing in 30 minutes",
            "source": "Calendar",
            "severity": "info",
        },
        {
            "id": "e5",
            "time": "03:12",
            "title": "Thread #incident-2291 escalated",
            "source": "Chat",
            "severity": "warning",
        },
        {
            "id": "e6",
            "time": "02:58",
            "title": "Vendor SLA report delivered",
            "source": "Email",
            "severity": "info",
        },
    ]

    @rx.event
    def select_tab(self, tab_id: str):
        if tab_id == self.active_tab:
            return
        self.active_tab = tab_id

    @rx.var
    def active_label(self) -> str:
        for t in self.tabs:
            if t["id"] == self.active_tab:
                return t["label"]
        return "Operations"
