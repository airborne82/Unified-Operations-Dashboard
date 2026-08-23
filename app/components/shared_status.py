import reflex as rx

from app.components.tab_events import select_tab_events
from app.states.dashboard_state import DashboardState, Tab
from app.states.shared_status_state import (
    LogEntry,
    SharedStatusState,
    SystemStatus,
)


def _switcher_tab(tab: Tab, **props) -> rx.Component:
    return rx.el.button(
        rx.icon(tab["icon"], class_name="h-3.5 w-3.5 shrink-0"),
        rx.el.span(tab["label"], class_name="truncate"),
        type="button",
        on_click=select_tab_events(tab["id"]),
        class_name=rx.cond(
            DashboardState.active_tab == tab["id"],
            "flex min-w-0 items-center justify-center gap-1.5 rounded-sm border border-cyan-500/60 bg-cyan-500/10 px-2.5 py-1.5 text-[10px] font-bold uppercase tracking-[0.14em] text-cyan-300",
            "flex min-w-0 items-center justify-center gap-1.5 rounded-sm border border-zinc-800 bg-zinc-900/40 px-2.5 py-1.5 text-[10px] font-semibold uppercase tracking-[0.14em] text-zinc-500 transition-colors hover:border-zinc-600 hover:text-zinc-200",
        ),
        **props,
    )


def responsive_tabs() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.span(
                "Responsive tab switcher",
                class_name="text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-500",
            ),
            rx.el.span(
                DashboardState.active_label,
                class_name="w-fit rounded-sm border border-cyan-500/40 bg-cyan-500/10 px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest text-cyan-300",
            ),
            class_name="flex shrink-0 items-center justify-between gap-2 sm:justify-start",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    DashboardState.tabs,
                    lambda t: rx.el.option(t["label"], value=t["id"]),
                ),
                value=DashboardState.active_tab,
                on_change=lambda value: select_tab_events(value),
                class_name="w-full appearance-none rounded-sm border border-zinc-700 bg-zinc-900/70 px-3 py-2 text-[11px] font-semibold uppercase tracking-widest text-zinc-200 focus:border-cyan-500/70 focus:outline-hidden",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-zinc-500",
            ),
            class_name="relative w-full sm:hidden",
        ),
        rx.el.div(
            rx.foreach(
                DashboardState.tabs, lambda t: _switcher_tab(t, key=t["id"])
            ),
            class_name="hidden w-full min-w-0 gap-1.5 sm:grid sm:grid-cols-4 lg:flex lg:flex-1 lg:flex-wrap lg:justify-end",
        ),
        id="responsive-tabs",
        class_name="col-span-12 lg:col-start-1 lg:col-span-12 lg:row-start-1 lg:row-span-1 flex w-full min-w-0 flex-col gap-2 rounded-2xl border border-slate-800/80 bg-slate-900/80 p-3 shadow-lg shadow-black/20 sm:flex-row sm:items-center sm:gap-3",
    )


def _system_card(system: SystemStatus, **props) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    system["icon"],
                    class_name=rx.match(
                        system["status"],
                        ("critical", "h-4 w-4 text-red-400"),
                        ("watch", "h-4 w-4 text-amber-400"),
                        "h-4 w-4 text-cyan-400",
                    ),
                ),
                rx.el.span(
                    system["name"],
                    class_name="truncate text-[11px] font-bold uppercase tracking-[0.16em] text-zinc-200",
                ),
                class_name="flex min-w-0 items-center gap-2",
            ),
            rx.el.span(
                rx.match(
                    system["status"],
                    ("critical", "CRITICAL"),
                    ("watch", "WATCH"),
                    "NOMINAL",
                ),
                class_name=rx.match(
                    system["status"],
                    (
                        "critical",
                        "w-fit shrink-0 rounded-sm border border-red-500/40 bg-red-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-red-400",
                    ),
                    (
                        "watch",
                        "w-fit shrink-0 rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-amber-400",
                    ),
                    "w-fit shrink-0 rounded-sm border border-cyan-500/40 bg-cyan-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-cyan-300",
                ),
            ),
            class_name="flex w-full items-center justify-between gap-2",
        ),
        rx.el.p(
            system["value"],
            class_name="font-mono text-base text-zinc-100",
        ),
        rx.el.p(
            system["detail"],
            class_name="text-left text-[10px] leading-snug text-zinc-500",
        ),
        rx.el.div(
            rx.el.div(
                style={"width": f"{system['load']}%"},
                class_name=rx.match(
                    system["status"],
                    ("critical", "h-1 rounded-sm bg-red-500"),
                    ("watch", "h-1 rounded-sm bg-amber-400"),
                    "h-1 rounded-sm bg-cyan-400",
                ),
            ),
            class_name="mt-auto h-1 w-full overflow-hidden rounded-sm bg-zinc-800",
        ),
        type="button",
        on_click=select_tab_events(system["tab"]),
        class_name=rx.cond(
            DashboardState.active_tab == system["tab"],
            "flex h-full w-full flex-col items-start gap-1.5 rounded-sm border border-cyan-500/60 bg-cyan-500/5 p-3 text-left transition-colors",
            "flex h-full w-full flex-col items-start gap-1.5 rounded-sm border border-zinc-800 bg-zinc-900/40 p-3 text-left transition-colors hover:border-cyan-500/40",
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
        class_name="flex items-center gap-1.5 rounded-sm border border-zinc-800 bg-zinc-900/50 px-2 py-1",
    )


def shared_status() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Shared system status",
                    class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
                ),
                rx.el.p(
                    "Cross-tab indicators · select a system to switch workspace",
                    class_name="text-[10px] uppercase tracking-[0.16em] text-zinc-600",
                ),
                class_name="flex min-w-0 flex-col gap-0.5",
            ),
            rx.el.div(
                _tally(
                    "critical", SharedStatusState.critical_count, "bg-red-500"
                ),
                _tally("watch", SharedStatusState.watch_count, "bg-amber-400"),
                _tally(
                    "nominal", SharedStatusState.nominal_count, "bg-cyan-400"
                ),
                class_name="flex flex-wrap items-center gap-2",
            ),
            class_name="flex flex-wrap items-start justify-between gap-2 border-b border-zinc-800 px-4 py-2.5",
        ),
        rx.el.div(
            rx.foreach(
                SharedStatusState.systems,
                lambda s: _system_card(s, key=s["id"]),
            ),
            class_name="grid w-full flex-1 grid-cols-1 gap-3 p-4 sm:grid-cols-2 lg:grid-cols-4",
        ),
        id="shared-status",
        class_name="col-span-12 lg:col-start-1 lg:col-span-12 lg:row-start-2 lg:row-span-3 flex w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )


def _sort_header(label: str, key: str, icon: str, extra: str) -> rx.Component:
    return rx.el.th(
        rx.el.button(
            rx.icon(icon, class_name="h-3 w-3 text-zinc-500"),
            rx.el.span(label),
            rx.cond(
                SharedStatusState.sort_key == key,
                rx.icon(
                    rx.cond(
                        SharedStatusState.sort_desc, "arrow-down", "arrow-up"
                    ),
                    class_name="h-3 w-3 text-cyan-400",
                ),
                rx.icon("chevrons-up-down", class_name="h-3 w-3 text-zinc-700"),
            ),
            type="button",
            on_click=lambda: SharedStatusState.sort_by(key),
            class_name="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-[0.16em] text-zinc-400 transition-colors hover:text-cyan-300",
        ),
        class_name=f"px-3 py-2 text-left {extra}",
    )


def _log_row(row: LogEntry, **props) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            row["time"],
            class_name="whitespace-nowrap px-3 py-2 font-mono text-[11px] text-zinc-400",
        ),
        rx.el.td(
            rx.el.span(
                rx.match(
                    row["severity"],
                    ("critical", "CRITICAL"),
                    ("warning", "WARNING"),
                    "INFO",
                ),
                class_name=rx.match(
                    row["severity"],
                    (
                        "critical",
                        "w-fit rounded-sm border border-red-500/40 bg-red-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-red-400",
                    ),
                    (
                        "warning",
                        "w-fit rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-amber-400",
                    ),
                    "w-fit rounded-sm border border-cyan-500/40 bg-cyan-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-cyan-300",
                ),
            ),
            class_name="px-3 py-2",
        ),
        rx.el.td(
            row["source"],
            class_name="hidden whitespace-nowrap px-3 py-2 text-[11px] font-semibold uppercase tracking-widest text-zinc-500 sm:table-cell",
        ),
        rx.el.td(
            row["message"],
            class_name="px-3 py-2 text-[11px] leading-snug text-zinc-200",
        ),
        rx.el.td(
            row["ref"],
            class_name="hidden whitespace-nowrap px-3 py-2 font-mono text-[10px] uppercase tracking-widest text-zinc-500 md:table-cell",
        ),
        class_name="border-b border-zinc-800/70 transition-colors last:border-0 odd:bg-zinc-900/30 hover:bg-zinc-900/60",
        **props,
    )


def _scope_button(label: str, scope: str) -> rx.Component:
    return rx.el.button(
        label,
        type="button",
        on_click=lambda: SharedStatusState.set_scope(scope),
        class_name=rx.cond(
            SharedStatusState.log_scope == scope,
            "rounded-sm border border-cyan-500/60 bg-cyan-500/10 px-2 py-1 text-[10px] font-bold uppercase tracking-widest text-cyan-300",
            "rounded-sm border border-zinc-700 px-2 py-1 text-[10px] font-semibold uppercase tracking-widest text-zinc-500 transition-colors hover:border-zinc-500 hover:text-zinc-200",
        ),
    )


def unified_log() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Unified activity log",
                    class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
                ),
                rx.el.p(
                    f"{SharedStatusState.visible_count} entries · {DashboardState.active_label} scope",
                    class_name="text-[10px] uppercase tracking-[0.16em] text-zinc-600",
                ),
                class_name="flex min-w-0 flex-col gap-0.5",
            ),
            rx.el.div(
                _scope_button("Workspace", "workspace"),
                _scope_button("All systems", "all"),
                class_name="flex items-center gap-1.5",
            ),
            class_name="flex flex-wrap items-start justify-between gap-2 border-b border-zinc-800 px-4 py-2.5",
        ),
        rx.el.div(
            rx.cond(
                SharedStatusState.visible_log.length() > 0,
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            _sort_header("Time", "time", "clock", ""),
                            _sort_header(
                                "Severity", "severity", "triangle-alert", ""
                            ),
                            _sort_header(
                                "Source",
                                "source",
                                "radio",
                                "hidden sm:table-cell",
                            ),
                            rx.el.th(
                                "Message",
                                class_name="px-3 py-2 text-left text-[10px] font-bold uppercase tracking-[0.16em] text-zinc-400",
                            ),
                            rx.el.th(
                                "Ref",
                                class_name="hidden px-3 py-2 text-left text-[10px] font-bold uppercase tracking-[0.16em] text-zinc-400 md:table-cell",
                            ),
                            class_name="border-b border-zinc-800 bg-zinc-900/50",
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            SharedStatusState.visible_log,
                            lambda r: _log_row(r, key=r["id"]),
                        )
                    ),
                    class_name="table-auto w-full min-w-[420px]",
                ),
                rx.el.div(
                    rx.icon("inbox", class_name="h-5 w-5 text-zinc-600"),
                    rx.el.p(
                        "No log entries for this workspace",
                        class_name="text-[11px] font-bold uppercase tracking-[0.18em] text-zinc-400",
                    ),
                    rx.el.p(
                        "Switch scope to all systems to review the full log.",
                        class_name="text-[11px] text-zinc-600",
                    ),
                    class_name="flex flex-col items-center justify-center gap-2 p-8 text-center",
                ),
            ),
            class_name="w-full flex-1 overflow-auto",
        ),
        id="unified-log",
        class_name="col-span-12 lg:col-start-1 lg:col-span-12 lg:row-start-5 lg:row-span-4 flex min-h-[260px] w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )
