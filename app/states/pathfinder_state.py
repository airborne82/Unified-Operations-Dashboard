from typing import TypedDict

import reflex as rx


class PathfinderNode(TypedDict):
    id: str
    name: str
    customer: str
    location: str
    status: str
    latency: str
    uptime: str
    tunnel: str
    left: int
    top: int
    load: int


class PathfinderLink(TypedDict):
    id: str
    source: str
    target: str
    x1: int
    y1: int
    x2: int
    y2: int
    status: str


class PathfinderState(rx.State):
    selected_node: str = ""

    nodes: list[PathfinderNode] = [
        {
            "id": "pf-1",
            "name": "pathfinder-1",
            "customer": "Northwind Logistics",
            "location": "Rotterdam, NL · AMS-IX Edge",
            "status": "nominal",
            "latency": "18 ms",
            "uptime": "99.98%",
            "tunnel": "wg0 · AES-256",
            "left": 20,
            "top": 22,
            "load": 41,
        },
        {
            "id": "pf-2",
            "name": "pathfinder-2",
            "customer": "Meridian Health Group",
            "location": "Ashburn, VA, US · Equinix DC11",
            "status": "nominal",
            "latency": "26 ms",
            "uptime": "99.95%",
            "tunnel": "wg0 · AES-256",
            "left": 50,
            "top": 12,
            "load": 57,
        },
        {
            "id": "pf-3",
            "name": "pathfinder-3",
            "customer": "Cirrus Telecom",
            "location": "Frankfurt, DE · Interxion FRA6",
            "status": "watch",
            "latency": "48 ms",
            "uptime": "99.71%",
            "tunnel": "wg1 · rekey pending",
            "left": 78,
            "top": 24,
            "load": 74,
        },
        {
            "id": "pf-4",
            "name": "pathfinder-4",
            "customer": "Halden Maritime",
            "location": "Singapore, SG · Equinix SG3",
            "status": "nominal",
            "latency": "94 ms",
            "uptime": "99.92%",
            "tunnel": "wg0 · AES-256",
            "left": 86,
            "top": 58,
            "load": 38,
        },
        {
            "id": "pf-5",
            "name": "pathfinder-5",
            "customer": "Andes Mining Consortium",
            "location": "Santiago, CL · VPS-SCL-02",
            "status": "critical",
            "latency": "412 ms",
            "uptime": "97.10%",
            "tunnel": "wg1 · flapping",
            "left": 62,
            "top": 78,
            "load": 96,
        },
        {
            "id": "pf-6",
            "name": "pathfinder-6",
            "customer": "Sable Energy Partners",
            "location": "Aberdeen, UK · Offshore relay",
            "status": "watch",
            "latency": "77 ms",
            "uptime": "99.44%",
            "tunnel": "wg0 · satellite backup",
            "left": 30,
            "top": 62,
            "load": 68,
        },
        {
            "id": "pf-7",
            "name": "pathfinder-7",
            "customer": "Kestrel Financial",
            "location": "Toronto, CA · Cologix TOR1",
            "status": "nominal",
            "latency": "31 ms",
            "uptime": "99.99%",
            "tunnel": "wg0 · AES-256",
            "left": 12,
            "top": 46,
            "load": 29,
        },
        {
            "id": "pf-8",
            "name": "pathfinder-8",
            "customer": "Sakura Robotics",
            "location": "Osaka, JP · IDC KIX-1",
            "status": "nominal",
            "latency": "112 ms",
            "uptime": "99.90%",
            "tunnel": "wg0 · AES-256",
            "left": 46,
            "top": 44,
            "load": 52,
        },
        {
            "id": "pf-9",
            "name": "pathfinder-9",
            "customer": "Highveld Agritech",
            "location": "Johannesburg, ZA · Teraco JB1",
            "status": "watch",
            "latency": "138 ms",
            "uptime": "99.20%",
            "tunnel": "wg1 · degraded uplink",
            "left": 70,
            "top": 46,
            "load": 81,
        },
        {
            "id": "pf-10",
            "name": "pathfinder-10",
            "customer": "Aurora Retail Group",
            "location": "Sydney, AU · NextDC S2",
            "status": "nominal",
            "latency": "146 ms",
            "uptime": "99.87%",
            "tunnel": "wg0 · AES-256",
            "left": 38,
            "top": 86,
            "load": 44,
        },
    ]

    links: list[PathfinderLink] = [
        {
            "id": "lk-1",
            "source": "pathfinder-8",
            "target": "pathfinder-1",
            "x1": 46,
            "y1": 44,
            "x2": 20,
            "y2": 22,
            "status": "nominal",
        },
        {
            "id": "lk-2",
            "source": "pathfinder-8",
            "target": "pathfinder-2",
            "x1": 46,
            "y1": 44,
            "x2": 50,
            "y2": 12,
            "status": "nominal",
        },
        {
            "id": "lk-3",
            "source": "pathfinder-8",
            "target": "pathfinder-3",
            "x1": 46,
            "y1": 44,
            "x2": 78,
            "y2": 24,
            "status": "watch",
        },
        {
            "id": "lk-4",
            "source": "pathfinder-8",
            "target": "pathfinder-7",
            "x1": 46,
            "y1": 44,
            "x2": 12,
            "y2": 46,
            "status": "nominal",
        },
        {
            "id": "lk-5",
            "source": "pathfinder-8",
            "target": "pathfinder-6",
            "x1": 46,
            "y1": 44,
            "x2": 30,
            "y2": 62,
            "status": "watch",
        },
        {
            "id": "lk-6",
            "source": "pathfinder-8",
            "target": "pathfinder-9",
            "x1": 46,
            "y1": 44,
            "x2": 70,
            "y2": 46,
            "status": "watch",
        },
        {
            "id": "lk-7",
            "source": "pathfinder-9",
            "target": "pathfinder-4",
            "x1": 70,
            "y1": 46,
            "x2": 86,
            "y2": 58,
            "status": "nominal",
        },
        {
            "id": "lk-8",
            "source": "pathfinder-9",
            "target": "pathfinder-5",
            "x1": 70,
            "y1": 46,
            "x2": 62,
            "y2": 78,
            "status": "critical",
        },
        {
            "id": "lk-9",
            "source": "pathfinder-6",
            "target": "pathfinder-10",
            "x1": 30,
            "y1": 62,
            "x2": 38,
            "y2": 86,
            "status": "nominal",
        },
        {
            "id": "lk-10",
            "source": "pathfinder-2",
            "target": "pathfinder-3",
            "x1": 50,
            "y1": 12,
            "x2": 78,
            "y2": 24,
            "status": "nominal",
        },
    ]

    @rx.event
    def select_node(self, name: str):
        self.selected_node = "" if self.selected_node == name else name

    @rx.event
    def clear_node(self):
        self.selected_node = ""

    @rx.var
    def node_count(self) -> int:
        return len(self.nodes)

    @rx.var
    def nominal_count(self) -> int:
        return len([n for n in self.nodes if n["status"] == "nominal"])

    @rx.var
    def watch_count(self) -> int:
        return len([n for n in self.nodes if n["status"] == "watch"])

    @rx.var
    def critical_count(self) -> int:
        return len([n for n in self.nodes if n["status"] == "critical"])

    @rx.var
    def selected_detail(self) -> str:
        for n in self.nodes:
            if n["name"] == self.selected_node:
                return f"{n['customer']} · {n['location']} · {n['latency']}"
        return ""
