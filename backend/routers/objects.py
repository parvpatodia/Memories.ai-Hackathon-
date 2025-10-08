from fastapi import APIRouter, HTTPException, Query
from database import get_db
from models import TrackedObjectCreate, TrackedObject, APIResponse
from typing import List, Optional

router = APIRouter(prefix="/api/objects", tags=["objects"])

@router.post("/", response_model=TrackedObject)
async def create_tracked_object(obj: TrackedObjectCreate):
    """
    Teach the system about a new object to track
    
    - **name**: Object name (e.g., "keys", "wallet", "phone")
    - **alias**: Detailed description with aliases (e.g., "car keys, house keys, blue keychain")
    """
    try:
        # Validate input
        if not obj.name.strip():
            raise HTTPException(status_code=400, detail="Object name cannot be empty")
        
        if not obj.alias.strip():
            raise HTTPException(status_code=400, detail="Object description cannot be empty")
        
        # Create object in database
        db = get_db()
        new_object = await db.create_tracked_object(obj)
        return new_object
        
    except ValueError as e:
        # Object already exists or validation error
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        print(f"Error creating tracked object: {e}")
        raise HTTPException(status_code=500, detail="Failed to create tracked object")

@router.get("/", response_model=List[TrackedObject])
async def get_tracked_objects(
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit number of results"),
    search: Optional[str] = Query(None, description="Search objects by name or alias")
):
    """
    Get all tracked objects or search for specific ones
    
    - **limit**: Maximum number of objects to return (default: all)
    - **search**: Search term to filter objects by name or alias
    """
    try:
        db = get_db()
        if search:
            objects = await db.find_matching_objects(search.strip())
        else:
            objects = await db.get_tracked_objects()
        
        # Apply limit if specified
        if limit and len(objects) > limit:
            objects = objects[:limit]
            
        return objects
        
    except Exception as e:
        print(f"Error fetching tracked objects: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tracked objects")

@router.get("/{object_id}", response_model=TrackedObject)
async def get_tracked_object(object_id: int):
    """Get details for a specific tracked object"""
    try:
        db = get_db()
        objects = await db.get_tracked_objects()
        obj = next((o for o in objects if o.id == object_id), None)
        
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        
        return obj
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching object {object_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch object")

@router.delete("/{object_id}", response_model=APIResponse)
async def delete_tracked_object(object_id: int):
    """Delete a tracked object"""
    try:
        db = get_db()
        success = await db.delete_tracked_object(object_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Object not found")
        
        return APIResponse(
            success=True,
            message=f"Object {object_id} deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting object {object_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete object")

@router.get("/suggestions/common")
async def get_common_objects():
    """Get suggestions for commonly tracked objects"""
    return {
        "common_objects": [
            {"name": "keys", "alias": "car keys, house keys, office keys, keychain, key ring"},
            {"name": "wallet", "alias": "leather wallet, purse, billfold, money clip"},
            {"name": "phone", "alias": "iPhone, smartphone, mobile phone, cell phone"},
            {"name": "glasses", "alias": "reading glasses, sunglasses, eyeglasses, spectacles"},
            {"name": "airpods", "alias": "AirPods, earbuds, wireless earphones, headphones"},
            {"name": "remote", "alias": "TV remote, remote control, controller"},
            {"name": "charger", "alias": "phone charger, USB cable, charging cable, power cord"},
            {"name": "watch", "alias": "wristwatch, smartwatch, Apple Watch, fitness tracker"}
        ],
        "tips": [
            "Use specific descriptions in the alias field",
            "Include colors, brands, or distinguishing features",
            "Add multiple ways you might refer to the object",
            "Be descriptive but concise"
        ]
    }
