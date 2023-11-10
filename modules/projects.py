from datetime import datetime
from typing import List
from modules.base import Base
from fyle_accounting_mappings.models import DestinationAttribute


class Project(Base):
    """
    Class for Projects module
    """
    def __init__(self, workspace_id: int, destination_field: str, sync_after: datetime,  sdk_connection, destination_sync_method: str = None, is_auto_sync_enabled: bool = False):
        super().__init__(
            workspace_id=workspace_id,
            source_field='PROJECT',
            destination_field=destination_field,
            platform_class_name='projects',
            sync_after=sync_after,
            sdk_connection=sdk_connection,
            destination_sync_method=destination_sync_method,
            is_auto_sync_enabled=is_auto_sync_enabled
        )

    def trigger_import(self):
        """
        Trigger import for Projects module
        """
        self.check_import_log_and_start_import()

    def construct_fyle_payload(
        self,
        paginated_destination_attributes: List[DestinationAttribute],
        existing_fyle_attributes_map: object
    ):
        """
        Construct Fyle payload for Projects module
        :param paginated_destination_attributes: List of paginated destination attributes
        :param existing_fyle_attributes_map: Existing Fyle attributes map
        :param is_auto_sync_status_allowed: Is auto sync status allowed
        :return: Fyle payload
        """
        payload = []

        for attribute in paginated_destination_attributes:
            project = {
                'name': attribute.value,
                'code': attribute.destination_id,
                'description': 'Sage Intacct Project - {0}, Id - {1}'.format(
                    attribute.value,
                    attribute.destination_id
                ),
                'is_enabled': True if attribute.active is None else attribute.active
            }

            # Create a new project if it does not exist in Fyle
            if attribute.value.lower() not in existing_fyle_attributes_map:
                payload.append(project)
            # Disable the existing project in Fyle if auto-sync status is allowed and the destination_attributes is inactive
            elif self.is_auto_sync_status_allowed and not attribute.active:
                project['id'] = existing_fyle_attributes_map[attribute.value.lower()]
                payload.append(project)

        return payload
