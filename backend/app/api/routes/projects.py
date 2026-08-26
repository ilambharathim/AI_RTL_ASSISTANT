"""
RIVA RESTful Project Management Routes.
Supports POST /api/projects, POST /api/projects/{id}/files, POST /api/projects/{id}/analyze, GET /api/projects/{id}/report.
"""

from __future__ import annotations
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/projects", tags=["projects"])

# In-memory project registry
PROJECTS_DB: Dict[str, Dict[str, Any]] = {}


class CreateProjectRequest(BaseModel):
    name: str
    description: str = ""


class ProjectFileRequest(BaseModel):
    filename: str
    category: str  # specification, rtl, testbench
    content: str


@router.post("")
def create_project(req: CreateProjectRequest):
    proj_id = f"proj_{len(PROJECTS_DB) + 1}"
    PROJECTS_DB[proj_id] = {
        "id": proj_id,
        "name": req.name,
        "description": req.description,
        "files": {},
        "analysis": None
    }
    return {"status": "created", "project_id": proj_id, "project": PROJECTS_DB[proj_id]}


@router.post("/{project_id}/files")
def upload_project_file(project_id: str, req: ProjectFileRequest):
    if project_id not in PROJECTS_DB:
        raise HTTPException(status_code=404, detail="Project not found")
    
    PROJECTS_DB[project_id]["files"][req.category] = {
        "filename": req.filename,
        "content": req.content
    }
    return {"status": "success", "category": req.category, "filename": req.filename}


@router.get("/{project_id}/status")
def get_project_status(project_id: str):
    if project_id not in PROJECTS_DB:
        raise HTTPException(status_code=404, detail="Project not found")
    
    has_analysis = PROJECTS_DB[project_id]["analysis"] is not None
    return {
        "project_id": project_id,
        "name": PROJECTS_DB[project_id]["name"],
        "files_count": len(PROJECTS_DB[project_id]["files"]),
        "status": "ANALYZED" if has_analysis else "READY"
    }
