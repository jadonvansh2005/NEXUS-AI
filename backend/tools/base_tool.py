"""
UPSS Tool SDK - Base Tool

Defines the abstract base class for every tool in UPSS.

Every tool must inherit from BaseTool.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolInput,
    ToolMetadata,
)


class BaseTool(ABC):
    """
    Base class for every UPSS Tool.
    """

    metadata: ToolMetadata

    permission: ToolPermission = ToolPermission()

    input_model = ToolInput

    def __init__(self) -> None:

        self._initialized = False

    async def initialize(self) -> None:
        """
        Optional initialization hook.

        Override if the tool needs to:

        - Load ML models
        - Connect database
        - Initialize API clients
        - Load cache
        """

        self._initialized = True

    async def shutdown(self) -> None:
        """
        Optional cleanup hook.
        """

        pass

    @abstractmethod
    async def execute(
        self,
        context: ToolContext,
        request: ToolInput,
    ) -> ToolResult:
        """
        Execute the tool.

        Must be implemented by every tool.
        """
        raise NotImplementedError

    async def validate(
        self,
        request: ToolInput,
    ) -> None:
        """
        Optional validation.

        Override if additional validation
        is required.
        """

        return

    async def before_execute(
        self,
        context: ToolContext,
    ) -> None:
        """
        Hook executed before execute().
        """

        return

    async def after_execute(
        self,
        context: ToolContext,
        result: ToolResult,
    ) -> None:
        """
        Hook executed after execute().
        """

        return

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def category(self):
        return self.metadata.category

    @property
    def description(self):
        return self.metadata.description
    

    @property
    def domain(self) -> str:
        return getattr(
            self.metadata,
            "domain",
            "general",
        )


    @property
    def capabilities(self) -> list[str]:
        return getattr(
            self.metadata,
            "capabilities",
            [],
        )


    @property
    def providers(self) -> list[str]:
        return getattr(
            self.metadata,
            "providers",
            [],
        )


    @property
    def enabled(self) -> bool:
        return getattr(
            self.metadata,
            "enabled",
            True,
        )

    @property
    def timeout(self):
        return self.metadata.timeout

    def supports(self, tool_name: str) -> bool:
        """
        Returns True if this tool matches the requested tool.
        """

        return self.metadata.name == tool_name

    async def __call__(
        self,
        context: ToolContext,
        request: ToolInput,
    ) -> ToolResult:
        """
        Allows:

            result = await tool(context, request)
        """

        if not self._initialized:
            await self.initialize()

        await self.validate(request)

        await self.before_execute(context)

        start = datetime.utcnow()

        result = await self.execute(
            context=context,
            request=request,
        )

        elapsed = (
            datetime.utcnow() - start
        ).total_seconds()

        result.execution_time = elapsed

        await self.after_execute(
            context=context,
            result=result,
        )

        return result