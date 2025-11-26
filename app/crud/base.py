from typing import Generic, TypeVar, Type, Optional, List, Dict, Any, Union
from pydantic import BaseModel
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.base_class import BaseModel as DBBaseModls
from app.exceptions.base import NotFoundException

ModelType = TypeVar("ModelType", bound="DBBaseModls")
CreateSchemas = TypeVar("CreateSchemas", bound="BaseModel")
UpdateSchemas = TypeVar("UpdateSchemas", bound="BaseModel")

class BaseCrud(Generic[ModelType, CreateSchemas, UpdateSchemas]):

    def __init__(self, model: Type[ModelType], db: AsyncSession) -> None:
        self.model = model
        self.db = db


    async def get_by_id(
            self, id: UUID,
            include_deleted: bool = False
    ) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)

        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))

        result = await self.db.execute(query)
        
        return result.scalar_one_or_none()
    
    async def get_multi_data(
            self,
            skip: int = 0,
            limit: int = 100,
            include_deleted: bool = False,
            filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        
        query = select(self.model)

        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))

        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)

        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)

        return list(result.scalars().all())
    
    async def create(
            self,
            obj_in: Union[CreateSchemas, Dict[str, Any]]
    ) -> ModelType:
        
        if hasattr(obj_in, "model_dump"):
            obj_data = obj_in.model_dump()
        else:
            obj_data = obj_in

        db_obj = self.model(**obj_data)

        self.db.add(db_obj)

        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj
    
    async def update(
            self,
            id: UUID,
            obj_in: Union[UpdateSchemas, Dict[str, Any]]
    ) -> Optional[ModelType]:
        
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None # TODO i need added some exceptions for return data
        
        if hasattr(obj_in, "model_dump"):
            update_data = await obj_in.model_dump(exclude_unset=True)
        else:
            update_data = obj_in

            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    getattr(db_obj, field, value)

        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj


