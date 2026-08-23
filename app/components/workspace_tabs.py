import reflex as rx

from app.components.tab_events import select_tab_events
from app.states.dashboard_state import DashboardState, Tab


def _tab(tab: Tab, **props) -> rx.Component:
    return rx.el.button(
        rx.icon(tab["icon"], class_name="h-3.5 w-3.5"),
        rx.el.span(tab["label"], class_name="whitespace-nowrap"),
        rx.cond(
            (tab["id"] == "desktop") | (tab["id"] == "pathfinders"),
            rx.icon(
                "chevron-right",
                class_name="ml-auto hidden h-3 w-3 text-cyan-300/70 lg:block",
            ),
            rx.fragment(),
        ),
        type="button",
        on_click=select_tab_events(tab["id"]),
        class_name=rx.cond(
            DashboardState.active_tab == tab["id"],
            "flex shrink-0 cursor-pointer items-center gap-2 rounded-lg border border-cyan-400/60 bg-cyan-400/10 px-3 py-2 text-[11px] font-bold uppercase tracking-[0.14em] text-cyan-200 shadow-[0_0_18px_rgba(34,211,238,0.08)]",
            "flex shrink-0 cursor-pointer items-center gap-2 rounded-lg border border-transparent px-3 py-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 transition-all hover:border-slate-700 hover:bg-slate-800/70 hover:text-zinc-100",
        ),
        **props,
    )


def workspace_tabs() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.icon("layers-3", class_name="h-3.5 w-3.5 text-amber-400"),
            rx.el.span(
                "Workspace routing",
                class_name="text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-500",
            ),
            class_name="flex shrink-0 items-center gap-2 border-b border-zinc-800 px-2 pb-2 lg:mb-2 lg:border-b lg:pb-3",
        ),
        rx.foreach(DashboardState.tabs, lambda t: _tab(t, key=t["id"])),
        id="workspace-tabs",
        class_name="flex min-h-[42px] w-full min-w-0 shrink-0 items-center justify-start gap-1 overflow-x-auto whitespace-nowrap rounded-2xl border border-slate-800/80 bg-slate-950/90 px-3 py-2 shadow-xl shadow-black/20 [scrollbar-width:thin] lg:h-full lg:w-72 lg:flex-col lg:items-stretch lg:justify-start lg:gap-1.5 lg:overflow-y-auto lg:overflow-x-hidden lg:px-3 lg:py-4",
    )
