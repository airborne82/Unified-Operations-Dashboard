import reflex as rx

from app.components.workspace_detail import _status_pill
from app.states.dashboard_state import DashboardState, Event, Kpi
from app.states.workspace_state import TabCard, WorkspaceState


def _kpi(kpi: Kpi, **props) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                kpi["icon"],
                class_name=rx.cond(
                    kpi["tone"] == "amber",
                    "h-3.5 w-3.5 text-amber-400",
                    "h-3.5 w-3.5 text-cyan-400",
                ),
            ),
            rx.el.span(
                kpi["label"],
                class_name="text-[10px] font-semibold uppercase tracking-[0.16em] text-zinc-500",
            ),
            class_name="flex items-center gap-1.5",
        ),
        rx.el.p(kpi["value"], class_name="font-mono text-xl text-zinc-100"),
        rx.el.span(
            kpi["delta"],
            class_name=rx.cond(
                kpi["tone"] == "amber",
                "w-fit text-[10px] font-semibold uppercase tracking-widest text-amber-400",
                "w-fit text-[10px] font-semibold uppercase tracking-widest text-cyan-300",
            ),
        ),
        class_name="flex w-full flex-col gap-1 rounded-xl border border-slate-700/70 bg-slate-800/50 p-3 transition-all hover:border-cyan-500/40 hover:bg-slate-800/80",
        **props,
    )


def status_summary() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Status summary",
                class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
            ),
            rx.el.span(
                "T-15m",
                class_name="font-mono text-[10px] tracking-widest text-zinc-600",
            ),
            class_name="flex items-center justify-between border-b border-zinc-800 px-3 py-2.5",
        ),
        rx.el.div(
            rx.foreach(DashboardState.kpis, lambda k: _kpi(k, key=k["label"])),
            class_name="grid w-full grid-cols-2 gap-2 p-3",
        ),
        id="status-summary",
        class_name="col-span-12 lg:col-start-9 lg:col-span-4 lg:row-start-3 lg:row-span-2 flex w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )


def _event(event: Event, **props) -> rx.Component:
    return rx.el.li(
        rx.el.span(
            class_name=rx.match(
                event["severity"],
                (
                    "critical",
                    "mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-red-500",
                ),
                (
                    "warning",
                    "mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-400",
                ),
                "mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-cyan-400",
            )
        ),
        rx.el.div(
            rx.el.p(
                event["title"],
                class_name="text-[12px] font-medium leading-snug text-zinc-200",
            ),
            rx.el.div(
                rx.el.span(
                    event["source"],
                    class_name="text-[10px] font-semibold uppercase tracking-widest text-zinc-500",
                ),
                rx.el.span("·", class_name="text-zinc-700"),
                rx.el.span(
                    event["time"],
                    class_name="font-mono text-[10px] text-zinc-500",
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name="flex min-w-0 flex-col gap-0.5",
        ),
        class_name="flex items-start gap-2 border-b border-zinc-800/70 px-3 py-2 transition-colors last:border-0 hover:bg-zinc-900/60",
        **props,
    )


def active_events() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Active events",
                class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
            ),
            rx.el.span(
                "6 open",
                class_name="w-fit rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-widest text-amber-400",
            ),
            class_name="flex items-center justify-between border-b border-zinc-800 px-3 py-2.5",
        ),
        rx.el.ul(
            rx.foreach(DashboardState.events, lambda e: _event(e, key=e["id"])),
            class_name="flex-1 divide-zinc-800 overflow-y-auto",
        ),
        id="active-events",
        class_name="col-span-12 lg:col-start-9 lg:col-span-4 lg:row-start-5 lg:row-span-3 flex w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )


def _tab_card(card: TabCard, **props) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    card["icon"],
                    class_name=rx.cond(
                        card["tone"] == "amber",
                        "h-4 w-4 text-amber-400",
                        "h-4 w-4 text-cyan-400",
                    ),
                ),
                rx.el.h3(
                    card["title"],
                    class_name="text-[11px] font-bold uppercase tracking-[0.16em] text-zinc-200",
                ),
                class_name="flex min-w-0 items-center gap-2",
            ),
            _status_pill(card["status"]),
            class_name="flex items-center justify-between gap-2",
        ),
        rx.el.p(card["metric"], class_name="font-mono text-lg text-zinc-100"),
        rx.el.p(
            card["caption"], class_name="text-[11px] leading-snug text-zinc-500"
        ),
        rx.el.div(
            rx.el.span(
                DashboardState.active_label,
                class_name="text-[9px] font-semibold uppercase tracking-[0.18em] text-zinc-600",
            ),
            rx.icon("arrow-right", class_name="h-3 w-3 text-zinc-600"),
            class_name="mt-auto flex items-center justify-between border-t border-zinc-800 pt-2",
        ),
        class_name="flex h-full w-full flex-col gap-1.5 rounded-sm border border-zinc-800 bg-zinc-900/40 p-3 transition-colors hover:border-cyan-500/40",
        **props,
    )


def _card_skeleton() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="h-3 w-1/2 animate-pulse rounded-sm bg-zinc-800/70"
        ),
        rx.el.div(
            class_name="mt-3 h-6 w-2/3 animate-pulse rounded-sm bg-zinc-800/70"
        ),
        rx.el.div(
            class_name="mt-3 h-2 w-full animate-pulse rounded-sm bg-zinc-800/70"
        ),
        class_name="h-full w-full rounded-sm border border-zinc-800 bg-zinc-900/40 p-3",
    )


def tab_content_panels() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Tab content panels",
                    class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
                ),
                rx.el.p(
                    f"Contextual cards · {DashboardState.active_label} workspace",
                    class_name="text-[10px] uppercase tracking-[0.16em] text-zinc-600",
                ),
                class_name="flex flex-col gap-0.5",
            ),
            rx.cond(
                WorkspaceState.is_loading,
                rx.el.span(
                    "Loading context",
                    class_name="w-fit rounded-sm border border-zinc-700 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-zinc-400",
                ),
                rx.el.span(
                    f"{WorkspaceState.current_cards.length()} panels live",
                    class_name="w-fit rounded-sm border border-cyan-500/40 bg-cyan-500/10 px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest text-cyan-300",
                ),
            ),
            class_name="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 px-4 py-2.5",
        ),
        rx.cond(
            WorkspaceState.is_loading,
            rx.el.div(
                _card_skeleton(),
                _card_skeleton(),
                _card_skeleton(),
                _card_skeleton(),
                class_name="grid w-full flex-1 grid-cols-1 gap-3 p-4 sm:grid-cols-2 xl:grid-cols-4",
            ),
            rx.el.div(
                rx.foreach(
                    WorkspaceState.current_cards,
                    lambda c: _tab_card(c, key=c["id"]),
                ),
                class_name="grid w-full flex-1 grid-cols-1 gap-3 p-4 sm:grid-cols-2 xl:grid-cols-4",
            ),
        ),
        id="tab-content-panels",
        class_name="col-span-12 lg:col-start-1 lg:col-span-12 lg:row-start-8 lg:row-span-4 flex min-h-[240px] w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )
