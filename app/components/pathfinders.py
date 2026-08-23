import reflex as rx

from app.states.pathfinder_state import (
    PathfinderLink,
    PathfinderNode,
    PathfinderState,
)


def _health_pill(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        rx.match(
            status,
            ("critical", "CRITICAL"),
            ("watch", "DEGRADED"),
            "HEALTHY",
        ),
        class_name=rx.match(
            status,
            (
                "critical",
                "w-fit rounded-sm border border-red-500/40 bg-red-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-red-400",
            ),
            (
                "watch",
                "w-fit rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-amber-400",
            ),
            "w-fit rounded-sm border border-cyan-500/40 bg-cyan-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-cyan-300",
        ),
    )


def _health_dot(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        class_name=rx.match(
            status,
            (
                "critical",
                "block h-2 w-2 shrink-0 animate-pulse rounded-full bg-red-500 ring-4 ring-red-500/20",
            ),
            (
                "watch",
                "block h-2 w-2 shrink-0 rounded-full bg-amber-400 ring-4 ring-amber-400/20",
            ),
            "block h-2 w-2 shrink-0 rounded-full bg-cyan-400 ring-4 ring-cyan-400/20",
        )
    )


def _legend(color: str, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(class_name=f"h-1.5 w-1.5 rounded-full {color}"),
        rx.el.span(
            label,
            class_name="text-[10px] uppercase tracking-widest text-zinc-500",
        ),
        class_name="flex items-center gap-1.5",
    )


def _link(link: PathfinderLink, **props) -> rx.Component:
    return rx.el.line(
        x1=f"{link['x1']}",
        y1=f"{link['y1']}",
        x2=f"{link['x2']}",
        y2=f"{link['y2']}",
        stroke=rx.match(
            link["status"],
            ("critical", "#ef4444"),
            ("watch", "#fbbf24"),
            "#22d3ee",
        ),
        stroke_width="0.35",
        stroke_dasharray=rx.cond(link["status"] == "critical", "1.5 1.2", "0"),
        stroke_opacity="0.6",
        **props,
    )


def _map_node(node: PathfinderNode, **props) -> rx.Component:
    return rx.el.button(
        _health_dot(node["status"]),
        rx.el.span(
            node["name"],
            class_name="whitespace-nowrap font-mono text-[9px] uppercase tracking-widest text-zinc-300",
        ),
        rx.el.span(
            node["customer"],
            class_name="hidden whitespace-nowrap text-[8px] uppercase tracking-widest text-zinc-500 sm:block",
        ),
        type="button",
        on_click=lambda: PathfinderState.select_node(node["name"]),
        style={"left": f"{node['left']}%", "top": f"{node['top']}%"},
        class_name=rx.cond(
            PathfinderState.selected_node == node["name"],
            "absolute flex -translate-x-1/2 -translate-y-1/2 cursor-pointer flex-col items-center gap-1 rounded-lg border border-cyan-400/70 bg-slate-900/90 px-2 py-1.5",
            "absolute flex -translate-x-1/2 -translate-y-1/2 cursor-pointer flex-col items-center gap-1 rounded-lg border border-transparent px-2 py-1.5 transition-colors hover:border-slate-700 hover:bg-slate-900/80",
        ),
        **props,
    )


def _node_card(node: PathfinderNode, **props) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                _health_dot(node["status"]),
                rx.el.span(
                    node["name"],
                    class_name="truncate font-mono text-[11px] font-bold uppercase tracking-[0.14em] text-zinc-100",
                ),
                class_name="flex min-w-0 items-center gap-2",
            ),
            _health_pill(node["status"]),
            class_name="flex w-full items-center justify-between gap-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("building-2", class_name="h-3 w-3 text-cyan-400/80"),
                rx.el.span(
                    "Customer",
                    class_name="text-[9px] font-bold uppercase tracking-[0.18em] text-zinc-600",
                ),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.p(
                node["customer"],
                class_name="text-left text-[11px] font-semibold leading-snug text-zinc-200",
            ),
            class_name="flex w-full flex-col gap-0.5",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("map-pin", class_name="h-3 w-3 text-amber-400/80"),
                rx.el.span(
                    "Location",
                    class_name="text-[9px] font-bold uppercase tracking-[0.18em] text-zinc-600",
                ),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.p(
                node["location"],
                class_name="text-left text-[11px] leading-snug text-zinc-400",
            ),
            class_name="flex w-full flex-col gap-0.5",
        ),
        rx.el.div(
            rx.el.span(
                node["latency"],
                class_name="font-mono text-[10px] text-zinc-300",
            ),
            rx.el.span(
                node["uptime"],
                class_name="font-mono text-[10px] text-zinc-500",
            ),
            class_name="flex w-full items-center justify-between gap-2 border-t border-slate-800 pt-2",
        ),
        rx.el.p(
            node["tunnel"],
            class_name="text-left font-mono text-[9px] uppercase tracking-widest text-zinc-600",
        ),
        rx.el.div(
            rx.el.div(
                style={"width": f"{node['load']}%"},
                class_name=rx.match(
                    node["status"],
                    ("critical", "h-1 rounded-sm bg-red-500"),
                    ("watch", "h-1 rounded-sm bg-amber-400"),
                    "h-1 rounded-sm bg-cyan-400",
                ),
            ),
            class_name="mt-auto h-1 w-full overflow-hidden rounded-sm bg-slate-800",
        ),
        type="button",
        on_click=lambda: PathfinderState.select_node(node["name"]),
        class_name=rx.cond(
            PathfinderState.selected_node == node["name"],
            "flex h-full w-full cursor-pointer flex-col items-start gap-2 rounded-2xl border border-cyan-400/70 bg-cyan-400/5 p-3 text-left transition-all",
            "flex h-full w-full cursor-pointer flex-col items-start gap-2 rounded-2xl border border-slate-800 bg-slate-900/50 p-3 text-left transition-all hover:-translate-y-0.5 hover:border-cyan-500/50 hover:bg-slate-900/80",
        ),
        **props,
    )


def _tally(label: str, count: rx.Var[int], tone: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(class_name=f"h-1.5 w-1.5 rounded-full {tone}"),
        rx.el.span(
            f"{count} {label}",
            class_name="font-mono text-[10px] uppercase tracking-widest text-zinc-400",
        ),
        class_name="flex items-center gap-1.5 rounded-sm border border-slate-800 bg-slate-900/50 px-2 py-1",
    )


def pathfinder_topology() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("route", class_name="h-4 w-4 text-cyan-400"),
                    rx.el.h2(
                        "Pathfinders · distributed micro server topology",
                        class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
                    ),
                    class_name="flex min-w-0 items-center gap-2",
                ),
                rx.el.p(
                    f"{PathfinderState.node_count} remote nodes · mesh overlay via wireguard",
                    class_name="text-[10px] uppercase tracking-[0.16em] text-zinc-600",
                ),
                class_name="flex min-w-0 flex-col gap-0.5",
            ),
            rx.el.div(
                _tally(
                    "critical", PathfinderState.critical_count, "bg-red-500"
                ),
                _tally("degraded", PathfinderState.watch_count, "bg-amber-400"),
                _tally("healthy", PathfinderState.nominal_count, "bg-cyan-400"),
                class_name="flex flex-wrap items-center gap-2",
            ),
            class_name="flex flex-wrap items-start justify-between gap-3 border-b border-zinc-800 px-4 py-2.5",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    class_name="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:32px_32px]"
                ),
                rx.el.div(
                    class_name="absolute left-1/2 top-1/2 h-72 w-72 -translate-x-1/2 -translate-y-1/2 rounded-full border border-cyan-500/15"
                ),
                rx.el.div(
                    class_name="absolute left-1/2 top-1/2 h-48 w-48 -translate-x-1/2 -translate-y-1/2 rounded-full border border-cyan-500/20"
                ),
                rx.el.div(
                    class_name="absolute left-1/2 top-1/2 h-24 w-24 -translate-x-1/2 -translate-y-1/2 rounded-full border border-cyan-500/25"
                ),
                rx.el.svg(
                    rx.foreach(
                        PathfinderState.links,
                        lambda lk: _link(lk, key=lk["id"]),
                    ),
                    view_box="0 0 100 100",
                    preserve_aspect_ratio="none",
                    class_name="absolute inset-0 h-full w-full",
                ),
                rx.foreach(
                    PathfinderState.nodes,
                    lambda n: _map_node(n, key=n["id"]),
                ),
                class_name="relative h-[360px] w-full overflow-hidden rounded-xl border border-cyan-500/20 bg-slate-950 shadow-inner shadow-cyan-950/20",
            ),
            rx.el.div(
                _legend("bg-cyan-400", "Healthy link"),
                _legend("bg-amber-400", "Degraded link"),
                _legend("bg-red-500", "Critical link"),
                rx.cond(
                    PathfinderState.selected_node != "",
                    rx.el.div(
                        rx.el.span(
                            PathfinderState.selected_node,
                            class_name="font-mono text-[10px] font-bold uppercase tracking-widest text-cyan-300",
                        ),
                        rx.el.span(
                            PathfinderState.selected_detail,
                            class_name="font-mono text-[10px] text-zinc-500",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-3 w-3"),
                            type="button",
                            on_click=PathfinderState.clear_node,
                            class_name="flex h-5 w-5 items-center justify-center rounded-sm border border-zinc-700 text-zinc-400 transition-colors hover:border-red-500/60 hover:text-red-400",
                        ),
                        class_name="ml-auto flex flex-wrap items-center gap-2 rounded-xl border border-cyan-500/40 bg-cyan-500/5 px-3 py-1.5",
                    ),
                    rx.el.span(
                        "Select a node to inspect",
                        class_name="ml-auto w-fit rounded-xl border border-zinc-700 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-widest text-zinc-500",
                    ),
                ),
                class_name="flex flex-wrap items-center gap-3",
            ),
            class_name="flex flex-1 flex-col gap-3 p-4",
        ),
        id="pathfinder-topology",
        class_name="flex w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-cyan-950/10",
    )


def pathfinder_grid() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.icon("server", class_name="h-4 w-4 text-cyan-400"),
                rx.el.h2(
                    "Pathfinder nodes · health, customer, location",
                    class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
                ),
                class_name="flex min-w-0 items-center gap-2",
            ),
            rx.el.p(
                "Connected grid mirrors the topology overlay",
                class_name="text-[10px] uppercase tracking-[0.16em] text-zinc-600",
            ),
            class_name="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 px-4 py-2.5",
        ),
        rx.el.div(
            rx.foreach(
                PathfinderState.nodes,
                lambda n: _node_card(n, key=n["id"]),
            ),
            class_name="grid w-full grid-cols-1 gap-3 p-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5",
        ),
        id="pathfinder-grid",
        class_name="mt-3 flex w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )


def pathfinders_view() -> rx.Component:
    return rx.el.div(
        pathfinder_topology(),
        pathfinder_grid(),
        class_name="flex w-full min-w-0 flex-col",
    )
