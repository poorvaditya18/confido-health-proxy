from services.epic_source_service import EpicSourceService

class SourceFactory:
    @staticmethod
    def get_source_service(source_type: str):
        source_type = source_type.lower()
        if source_type == "epic":
            return EpicSourceService()
        else:
            raise ValueError(f"unknown source type: {source_type} not supported")