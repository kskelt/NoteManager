from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.notes import NoteCreate, NoteModel
from app.services.notes import NoteService
from app.utils.logger import log_action
from app.models.users import BaseUser
from app.core.roles_permissions import Permission, require_permission

note_router = APIRouter(prefix="/notes", tags=["notes"])




@note_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note_data: NoteCreate,
    note_service: NoteService = Depends(),
    user: BaseUser = Depends(require_permission(Permission.CREATE_NOTE)),
):
    note_id = note_service.create_note(note_data, user)
    log_action(user.username, user.role, "create_note", note_id)
    return {"detail": "Note created"}

@note_router.get("/", response_model=list[NoteModel])
def get_my_notes(
    user: BaseUser = Depends(require_permission(Permission.READ_OWN_NOTE)),
    note_service: NoteService = Depends(NoteService),
):
    notes = note_service.list_user_notes(user)
    log_action(user.username, user.role, "get_user_notes")
    return notes

@note_router.get("/all", response_model=list[NoteModel])
def get_all_notes(
    note_service: NoteService = Depends(),
    user: BaseUser = Depends(require_permission(Permission.READ_ALL_NOTES)),
):
    notes = note_service.list_all_notes()
    log_action(user.username, user.role, "get_all_notes")
    return notes

@note_router.get("/{note_id}", response_model=NoteModel)
def get_note_by_id(
    note_id: str,
    user: BaseUser = Depends(require_permission(Permission.READ_OWN_NOTE)),
    note_service: NoteService = Depends(),
):
    note = note_service.get_note(note_id, user)
    log_action(user.username, user.role, "get_user_note", note_id)
    return note


@note_router.patch("/{note_id}", response_model=dict)
def update_note(
    note_id: str,
    note_data: NoteCreate,
    note_service: NoteService = Depends(),
    user: BaseUser = Depends(require_permission(Permission.UPDATE_OWN_NOTE)),
):
    note_service.update_note(note_id, user, note_data)

    log_action(user.username, user.role, "update_note", note_id)
    return {"detail": "Note updated"}


@note_router.delete("/{note_id}", response_model=dict)
def delete_note(
    note_id: str,
    note_service: NoteService = Depends(),
    user: BaseUser = Depends(require_permission(Permission.DELETE_NOTE)),
):
    success = note_service.delete_note(note_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found or not allowed")
    log_action(user.username, user.role, "delete_note", note_id)
    return {"detail": "Note deleted"}


@note_router.get("/user/{user_id}", response_model=List[NoteModel])
def get_notes_by_user(
    user_id: str,
    note_service: NoteService = Depends(),
    user: BaseUser = Depends(require_permission(Permission.READ_ALL_NOTES)),
):
    notes = note_service.list_user_notes_admin(user_id)
    log_action(user.username, user.role, "get_user_notes_admin", user_id)
    return notes


@note_router.post("/restore/{note_id}", response_model=dict)
def restore_note(
    note_id: str,
    note_service: NoteService = Depends(),
    user: BaseUser = Depends(require_permission(Permission.RESTORE_NOTE)),
):
    note_service.restore_note(note_id)
    return {"detail": "Note restored"}
