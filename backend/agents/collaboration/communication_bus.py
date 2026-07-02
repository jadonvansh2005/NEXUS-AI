"""
Communication Bus

Responsibilities

- Agent-to-Agent communication
- Message routing
- Event publishing
- Event subscription

Future

- RabbitMQ
- Kafka
- Redis Streams
- Remote Agents
"""

from __future__ import annotations

from collections import defaultdict

from typing import Any
from typing import Callable
from typing import DefaultDict
from typing import Dict
from typing import List


class CommunicationBus:

    """
    Internal event bus for
    multi-agent collaboration.
    """

    def __init__(

        self,

    ):

        #
        # Event Subscribers
        #

        self._subscribers: DefaultDict[

            str,

            List[Callable[[Any], None]]

        ] = defaultdict(

            list

        )

        #
        # Message History
        #

        self._history: List[

            Dict[str, Any]

        ] = []

    # =====================================================
    # Subscribe
    # =====================================================

    def subscribe(

        self,

        event: str,

        handler: Callable[[Any], None],

    ) -> None:

        if handler not in self._subscribers[

            event

        ]:

            self._subscribers[

                event

            ].append(

                handler

            )

    # =====================================================
    # Unsubscribe
    # =====================================================

    def unsubscribe(

        self,

        event: str,

        handler: Callable[[Any], None],

    ) -> None:

        if handler in self._subscribers.get(

            event,

            [],

        ):

            self._subscribers[

                event

            ].remove(

                handler

            )

    # =====================================================
    # Publish
    # =====================================================

    def publish(

        self,

        event: str,

        payload: Any,

    ) -> None:

        #
        # Save History
        #

        self._history.append(

            {

                "event": event,

                "payload": payload,

            }

        )

        #
        # Notify Subscribers
        #

        for handler in self._subscribers.get(

            event,

            [],

        ):

            handler(

                payload

            )

    # =====================================================
    # Subscribers
    # =====================================================

    def subscribers(

        self,

        event: str,

    ) -> List[Callable]:

        return list(

            self._subscribers.get(

                event,

                [],

            )

        )

    # =====================================================
    # History
    # =====================================================

    def history(

        self,

    ) -> List[Dict[str, Any]]:

        return list(

            self._history

        )

    # =====================================================
    # Clear
    # =====================================================

    def clear(

        self,

    ) -> None:

        self._subscribers.clear()

        self._history.clear()