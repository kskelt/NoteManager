
from fastapi import Depends, HTTPException, status
from app.models.notes import NoteCreate, NoteModel
from app.models.users import BaseUser
from app.repository.notes import NoteRepository
from app.repository.users import UserRepository


class NoteService:
    def __init__(
        self, 
        note_repo: NoteRepository = Depends(), 
        user_repo: UserRepository = Depends()
    ):
        self._note_repo = note_repo
        self._user_repo = user_repo

    def _get_user_id(self, username: str) -> str:
        user = self._user_repo.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return str(user["_id"])

    def create_note(self, note_create: NoteCreate, user: BaseUser) -> str:
        user_id = self._get_user_id(user.username)
        
        note = NoteModel(
            title=note_create.title,
            body=note_create.body,
            user_id=user_id,
        )
        
        inserted_id = self._note_repo.create_note(note.model_dump())
        if not inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create note"
            )
            

    def get_note(self, note_id: str, user: BaseUser) -> NoteModel:
        user_id = self._get_user_id(user.username)
        is_admin = user.role == "admin"
        note = self._note_repo.get_note_by_id(note_id, user_id, is_admin)
        
        if not note or str(note["user_id"]) != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return note

    def update_note(self, note_id: str, user: BaseUser, note_create: NoteCreate) -> bool:
        user_id = self._get_user_id(user.username)
        result = self._note_repo.update_note(note_id, user_id, note_create.model_dump())
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found or not allowed"
            )
            
        return True

    def delete_note(self, note_id: str, user: BaseUser) -> bool:
        user_id = self._get_user_id(user.username)
        if not self._note_repo.delete_note(note_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found or not allowed"
            )
        return True

    def restore_note(self, note_id: str, user: BaseUser) -> bool:
        user_id = self._get_user_id(user.username)
        if not self._note_repo.restore_note(note_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found or not allowed"
            )
        return True

    def list_user_notes(self, user: BaseUser) -> list[NoteModel]:
        user_id = self._get_user_id(user.username)
        notes = self._note_repo.get_user_notes(user_id)
        return notes
    def list_user_notes_admin(self, user_id: str) -> list[NoteModel]:
        notes = self._note_repo.get_user_notes(user_id)
        if notes is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return notes

    def list_all_notes(self) -> list[NoteModel]:
        notes = self._note_repo.get_all_notes()
        return notes