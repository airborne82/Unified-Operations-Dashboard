import reflex as rx

from app.components.command_header import command_header
from app.components.grafana_panels import grafana_section
from app.components.ops_centerpiece import ops_centerpiece
from app.components.pathfinders import pathfinders_view
from app.components.remote_desktops import remote_desktop_launcher
from app.states.dashboard_state import DashboardState
from app.components.shared_status import (
    responsive_tabs,
    shared_status,
    unified_log,
)
from app.components.status_panels import (
    active_events,
    status_summary,
    tab_content_panels,
)
from app.components.workspace_detail import (
    quick_action_area,
    workspace_activity,
    workspace_header,
    workspace_panels,
)
from app.components.workspace_tabs import workspace_tabs


def _standard_workspace() -> rx.Component:
    return rx.el.div(
        command_header(),
        rx.el.div(
            ops_centerpiece(),
            status_summary(),
            active_events(),
            tab_content_panels(),
            class_name="grid grid-cols-1 gap-3 auto-rows-min lg:grid-cols-12 lg:grid-rows-[repeat(9,minmax(52px,auto))] items-start",
        ),
        rx.el.div(
            workspace_header(),
            workspace_panels(),
            workspace_activity(),
            quick_action_area(),
            class_name="mt-3 grid grid-cols-1 gap-3 auto-rows-min lg:grid-cols-12 lg:grid-rows-[auto_repeat(7,minmax(52px,auto))]",
        ),
        rx.el.div(
            responsive_tabs(),
            shared_status(),
            unified_log(),
            class_name="mt-3 grid grid-cols-1 gap-3 auto-rows-min lg:grid-cols-12 lg:grid-rows-[auto_repeat(7,minmax(52px,auto))]",
        ),
        grafana_section(),
        class_name="flex w-full min-w-0 flex-col",
    )


def _pathfinders_workspace() -> rx.Component:
    return rx.el.div(
        command_header(),
        pathfinders_view(),
        class_name="flex w-full min-w-0 flex-col gap-3",
    )


def dashboard_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            workspace_tabs(),
            rx.el.div(
                rx.match(
                    DashboardState.active_tab,
                    ("desktop", remote_desktop_launcher()),
                    ("pathfinders", _pathfinders_workspace()),
                    _standard_workspace(),
                ),
                class_name="min-w-0 flex-1 rounded-2xl border border-white/5 bg-slate-950/40 p-1",
            ),
            class_name="flex w-full min-w-0 flex-col gap-4 lg:flex-row lg:items-stretch",
        ),
        class_name="min-h-dvh w-full overflow-x-hidden bg-[radial-gradient(circle_at_top_right,rgba(8,145,178,0.12),transparent_34%),#090d14] p-3 font-['Inter'] text-zinc-200 sm:p-4 lg:p-6",
    )
