import reflex as rx

from app.states.dashboard_state import DashboardState
from app.states.shared_status_state import SharedStatusState
from app.states.workspace_state import WorkspaceState


def select_tab_events(tab_id: str | rx.Var[str]) -> list:
    """Events fired when a workspace tab is selected.

    Each state keeps its own copy of the active tab so no state depends on
    another state's computed vars.
    """
    return [
        DashboardState.select_tab(tab_id),
        WorkspaceState.switch_tab(tab_id),
        SharedStatusState.sync_tab(tab_id),
    ]
