from typing import TypedDict

import reflex as rx


class SystemStatus(TypedDict):
    id: str
    tab: str
    name: str
    icon: str
    status: str
    detail: str
    value: str
    load: int


class LogEntry(TypedDict):
    id: str
    tab: str
    time: str
    source: str
    severity: str
    message: str
    ref: str


SEVERITY_RANK: dict[str, int] = {"critical": 0, "warning": 1, "info": 2}


class SharedStatusState(rx.State):
    active_tab: str = "operations"
    log_scope: str = "workspace"
    sort_key: str = "time"
    sort_desc: bool = True

    systems: list[SystemStatus] = [
        {
            "id": "s-ops",
            "tab": "operations",
            "name": "Operations",
            "icon": "radar",
            "status": "watch",
            "detail": "Condition amber · 3 active incidents",
            "value": "87%",
            "load": 87,
        },
        {
            "id": "s-net",
            "tab": "pathfinders",
            "name": "Pathfinders",
            "icon": "route",
            "status": "critical",
            "detail": "pathfinder-5 uplink loss 12%",
            "value": "94.2%",
            "load": 94,
        },
        {
            "id": "s-sys",
            "tab": "systems",
            "name": "Systems",
            "icon": "cpu",
            "status": "nominal",
            "detail": "Compute pool 68% · CR-2291 T-42m",
            "value": "99.94%",
            "load": 68,
        },
        {
            "id": "s-gla",
            "tab": "gladius",
            "name": "Gladius AI",
            "icon": "brain-circuit",
            "status": "nominal",
            "detail": "Routing model v18 · 4 advisories",
            "value": "0.94 F1",
            "load": 94,
        },
        {
            "id": "s-dsk",
            "tab": "desktop",
            "name": "Desktop",
            "icon": "monitor",
            "status": "watch",
            "detail": "19 endpoints offline · ring 2 at 61%",
            "value": "1,284",
            "load": 61,
        },
        {
            "id": "s-cal",
            "tab": "calendar",
            "name": "Calendar",
            "icon": "calendar",
            "status": "watch",
            "detail": "CR-2291 / CR-2297 overlap 06:00 Z",
            "value": "6 events",
            "load": 55,
        },
        {
            "id": "s-cht",
            "tab": "chat",
            "name": "Chat",
            "icon": "message-square",
            "status": "watch",
            "detail": "2 escalations awaiting duty officer",
            "value": "14 rooms",
            "load": 58,
        },
        {
            "id": "s-eml",
            "tab": "email",
            "name": "Email",
            "icon": "mail",
            "status": "critical",
            "detail": "2 SLA replies breach in under 30m",
            "value": "41 unread",
            "load": 49,
        },
    ]

    log: list[LogEntry] = [
        {
            "id": "l1",
            "tab": "pathfinders",
            "time": "04:19",
            "source": "Telemetry",
            "severity": "critical",
            "message": "pathfinder-5 packet loss crossed 10% threshold",
            "ref": "INC-2291",
        },
        {
            "id": "l2",
            "tab": "operations",
            "time": "04:21",
            "source": "Duty Officer",
            "severity": "critical",
            "message": "Condition amber declared for southbound edge",
            "ref": "OPS-4411",
        },
        {
            "id": "l3",
            "tab": "operations",
            "time": "04:16",
            "source": "Automation",
            "severity": "warning",
            "message": "Playbook OPS-REROUTE staged for approval",
            "ref": "PB-118",
        },
        {
            "id": "l4",
            "tab": "gladius",
            "time": "04:07",
            "source": "Gladius AI",
            "severity": "info",
            "message": "Routing model retrained to v18",
            "ref": "MDL-18",
        },
        {
            "id": "l5",
            "tab": "systems",
            "time": "04:05",
            "source": "CAB Board",
            "severity": "warning",
            "message": "CR-2291 approved for the 06:00 window",
            "ref": "CR-2291",
        },
        {
            "id": "l6",
            "tab": "calendar",
            "time": "04:00",
            "source": "Scheduler",
            "severity": "critical",
            "message": "Overlap detected between CR-2291 and CR-2297",
            "ref": "CAL-77",
        },
        {
            "id": "l7",
            "tab": "desktop",
            "time": "04:12",
            "source": "Endpoint Agent",
            "severity": "warning",
            "message": "19 endpoints offline beyond 24h",
            "ref": "EP-940",
        },
        {
            "id": "l8",
            "tab": "pathfinders",
            "time": "03:58",
            "source": "NetOps",
            "severity": "warning",
            "message": "Applied shaping policy BULK-SYNC throttle",
            "ref": "POL-12",
        },
        {
            "id": "l9",
            "tab": "systems",
            "time": "03:40",
            "source": "Autoscaler",
            "severity": "info",
            "message": "zone-b scaled out by 2 nodes",
            "ref": "SCL-31",
        },
        {
            "id": "l10",
            "tab": "chat",
            "time": "03:12",
            "source": "#incident-2291",
            "severity": "warning",
            "message": "Thread escalated to duty officer",
            "ref": "CHT-204",
        },
        {
            "id": "l11",
            "tab": "email",
            "time": "02:58",
            "source": "Cirrus Telecom",
            "severity": "info",
            "message": "Vendor SLA report delivered",
            "ref": "TCK-8842",
        },
        {
            "id": "l12",
            "tab": "email",
            "time": "02:10",
            "source": "Mail Security",
            "severity": "warning",
            "message": "Phishing heuristics tightened",
            "ref": "SEC-59",
        },
        {
            "id": "l13",
            "tab": "gladius",
            "time": "03:20",
            "source": "Guardrail",
            "severity": "info",
            "message": "Tier-1 action held for dual approval",
            "ref": "GRD-7",
        },
        {
            "id": "l14",
            "tab": "desktop",
            "time": "03:50",
            "source": "Crew A",
            "severity": "info",
            "message": "Remote session OPS-114 opened",
            "ref": "OPS-114",
        },
        {
            "id": "l15",
            "tab": "calendar",
            "time": "03:31",
            "source": "Command",
            "severity": "info",
            "message": "Ops sync briefing moved to Bridge 2",
            "ref": "CAL-71",
        },
        {
            "id": "l16",
            "tab": "chat",
            "time": "03:04",
            "source": "#network-ops",
            "severity": "info",
            "message": "Crew C confirmed on-site arrival",
            "ref": "CHT-198",
        },
    ]

    @rx.event
    def set_scope(self, scope: str):
        self.log_scope = scope

    @rx.event
    def sort_by(self, key: str):
        if self.sort_key == key:
            self.sort_desc = not self.sort_desc
        else:
            self.sort_key = key
            self.sort_desc = key == "time"

    def _sort(self, rows: list[LogEntry]) -> list[LogEntry]:
        key = self.sort_key
        if key == "severity":
            return sorted(
                rows,
                key=lambda r: (SEVERITY_RANK.get(r["severity"], 3), r["time"]),
                reverse=self.sort_desc,
            )
        if key == "source":
            return sorted(
                rows, key=lambda r: r["source"].lower(), reverse=self.sort_desc
            )
        return sorted(rows, key=lambda r: r["time"], reverse=self.sort_desc)

    @rx.event
    def sync_tab(self, tab_id: str):
        self.active_tab = tab_id

    @rx.var
    def visible_log(self) -> list[LogEntry]:
        tab = self.active_tab
        rows = (
            self.log
            if self.log_scope == "all"
            else [r for r in self.log if r["tab"] == tab]
        )
        return self._sort(rows)

    @rx.var
    def visible_count(self) -> int:
        return len(self.visible_log)

    @rx.var
    def critical_count(self) -> int:
        return len([s for s in self.systems if s["status"] == "critical"])

    @rx.var
    def watch_count(self) -> int:
        return len([s for s in self.systems if s["status"] == "watch"])

    @rx.var
    def nominal_count(self) -> int:
        return len([s for s in self.systems if s["status"] == "nominal"])

    @rx.var
    def active_system(self) -> str:
        tab = self.active_tab
        for s in self.systems:
            if s["tab"] == tab:
                return s["status"]
        return "nominal"
